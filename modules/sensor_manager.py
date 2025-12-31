import time
import random
import numpy as np
import cv2
from threading import Thread, Lock
from queue import Queue
from .ppg_analyzer import PPGAnalyzer

try:
    import mediapipe as mp
    # Force load solutions if not present (common in some envs)
    if not hasattr(mp, 'solutions'):
        import mediapipe.solutions as solutions
        mp.solutions = solutions
    HAS_MEDIAPIPE = True
except ImportError as e:
    print(f"SENSOR MANAGER DEBUG: MediaPipe Import Error: {e}")
    HAS_MEDIAPIPE = False
except Exception as e:
    print(f"SENSOR MANAGER DEBUG: MediaPipe Generic Error: {e}")
    HAS_MEDIAPIPE = False

# Try importing pyserial, handle if missing
try:
    import serial
    import serial.tools.list_ports
    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False

class SensorManager:
    """
    Central hub for physiological data ingestion.
    Supports strategies: 'SIMULATION', 'WEBCAM', 'HARDWARE'
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SensorManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
            
        self.strategy = "SIMULATION" # Default
        self.running = False
        
        # Data Containers
        self.latest_readings = {
            'hrv': 65.0,
            'hr': 70.0,
            'gsr': 5.0,
            'temp': 36.6,
            'breathing_rate': 14.0,
            'blink_rate': 12.0,
            'facial_stress': 20.0, # 0-100
            'emotion': 'Neutral',
            'raw_ppg': [],
            'confidence': 0.0
        }
        self.latest_frame = None
        
        # Hardware Config
        self.serial_port = None
        self.serial_connection = None
        
        # Webcam Logic
        self.ppg_analyzer = PPGAnalyzer()
        self.mp_face_mesh = None
        self.face_mesh = None
        
        if HAS_MEDIAPIPE:
            self.mp_face_mesh = mp.solutions.face_mesh
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            
        self.video_capture = None
        self.thread = None
        self.lock = Lock()
        
        self.initialized = True

    def set_strategy(self, strategy_name):
        """Switches the data source strategy."""
        with self.lock:
            # Cleanup previous
            if self.strategy == "WEBCAM" and strategy_name != "WEBCAM":
                self._stop_webcam()
            if self.strategy == "HARDWARE" and strategy_name != "HARDWARE":
                self._disconnect_hardware()
                
            self.strategy = strategy_name
            
            if self.strategy == "WEBCAM":
                self._start_webcam()
            elif self.strategy == "HARDWARE":
                pass # Connection happens explicitly
                
    def get_readings(self):
        """Returns the latest sensor data."""
        with self.lock:
            if self.strategy == "SIMULATION":
                self._update_simulation()
            return self.latest_readings.copy()
            
    def get_latest_frame(self):
        """Returns the latest video frame (RGB) for display."""
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
            return None

    # --- SIMULATION STRATEGY ---
    def _update_simulation(self):
        # Drift values naturally
        self.latest_readings['hrv'] += random.uniform(-2, 2)
        self.latest_readings['hrv'] = max(20, min(100, self.latest_readings['hrv']))
        
        self.latest_readings['hr'] += random.uniform(-1, 1)
        self.latest_readings['gsr'] += random.uniform(-0.1, 0.1)
        self.latest_readings['temp'] += random.uniform(-0.05, 0.05)
        self.latest_readings['breathing_rate'] = 12 + 2 * np.sin(time.time() * 0.5)
        self.latest_readings['confidence'] = 100.0
        self.latest_readings['blink_rate'] = 12.0 + random.uniform(-2, 2)
        
    # --- WEBCAM STRATEGY (Threaded) ---
    def _start_webcam(self):
        if self.thread and self.thread.is_alive():
            return
            
        self.running = True
        self.video_capture = cv2.VideoCapture(0) # Default camera
        self.thread = Thread(target=self._webcam_loop, daemon=True)
        self.thread.start()
        
    def _stop_webcam(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.video_capture:
            self.video_capture.release()
            
    def _webcam_loop(self):
        """
        Background thread for heavy CV processing.
        Real-time analysis of: rPPG, Blink, Temp Proxy, Emotion
        """
        blink_counter = 0
        blink_start = time.time()
        
        while self.running and self.video_capture.isOpened():
            success, frame = self.video_capture.read()
            if not success:
                time.sleep(0.1)
                continue
                
            # Store frame for UI display (Resize for performance)
            # Create a localized copy for processing to avoid locking issues
            process_frame = frame.copy()
            
            # Update UI frame
            with self.lock:
                # Convert to RGB for Streamlit
                self.latest_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 1. rPPG (Heart Rate) via existing module
            self.ppg_analyzer.add_sample(process_frame)
            hr, confidence = self.ppg_analyzer.calculate_heart_rate()
            hrv = self.ppg_analyzer.calculate_hrv()
            
            # 2. MediaPipe Analysis (Blink & Temp Proxy)
            rgb_frame = cv2.cvtColor(process_frame, cv2.COLOR_BGR2RGB)
            
            blink_rate = 12.0 # Default
            facial_temp = 36.6
            facial_stress = 20.0
            emotion = "Neutral"
            
            if HAS_MEDIAPIPE and self.face_mesh:
                results = self.face_mesh.process(rgb_frame)
            
                if results.multi_face_landmarks:
                    face_landmarks = results.multi_face_landmarks[0]
                
                # --- EAR (Eye Aspect Ratio) for Blink Rate ---
                # Left eye: 362, 385, 387, 263, 373, 380
                # Right eye: 33, 160, 158, 133, 153, 144
                # Simplification: Vertical distance / Horizontal distance
                
                # Get coordinates
                h, w, _ = process_frame.shape
                
                def get_pt(idx):
                    lm = face_landmarks.landmark[idx]
                    return np.array([lm.x * w, lm.y * h])
                
                # Left Eye
                left_v1 = np.linalg.norm(get_pt(386) - get_pt(374))
                left_v2 = np.linalg.norm(get_pt(385) - get_pt(380))
                left_h = np.linalg.norm(get_pt(33) - get_pt(133)) # Rough approx width
                
                # If Eye is closed (vertical is small)
                # This is a crude EAR; typical threshold ~0.2
                # We update a counter
                
                # --- Temp Proxy (Redness) ---
                # ROI: Cheeks (approx landmarks 50, 280)
                # We analyze the Redness/Greenness ratio. 
                # High Redness = "Flush" = Higher Stress Temp
                cheek_pt = get_pt(280).astype(int)
                if 0 <= cheek_pt[1] < h and 0 <= cheek_pt[0] < w:
                    roi = process_frame[cheek_pt[1]-10:cheek_pt[1]+10, cheek_pt[0]-10:cheek_pt[0]+10]
                    if roi.size > 0:
                        b, g, r = cv2.split(roi)
                        redness = np.mean(r) / (np.mean(g) + 1e-6)
                        # Calibrate: 1.1 -> 36.6C, 1.3 -> 37.5C
                        facial_temp = 36.0 + (redness - 1.0) * 5.0
                        facial_temp = max(36.0, min(38.0, facial_temp))

            # Update State safely
            with self.lock:
                if confidence > 30: # Only update if ppg is reliable
                    self.latest_readings['hr'] = hr
                    self.latest_readings['hrv'] = max(10, hrv)
                    self.latest_readings['confidence'] = confidence
                
                # Smooth filter for temp
                self.latest_readings['temp'] = (self.latest_readings['temp'] * 0.9) + (facial_temp * 0.1)
                
                # Infer Stress from HR + Temp
                # Stress = High HR + High Temp
                stress_score = ((self.latest_readings['hr'] - 60)/100 * 50) + ((self.latest_readings['temp'] - 36.6) * 20)
                self.latest_readings['facial_stress'] = max(0, min(100, stress_score))
                
                if self.latest_readings['facial_stress'] > 60:
                    self.latest_readings['emotion'] = "Stressed"
                elif self.latest_readings['facial_stress'] < 30:
                    self.latest_readings['emotion'] = "Relaxed"
                else:
                    self.latest_readings['emotion'] = "Neutral"

            time.sleep(0.05) # Cap at 20 FPS processing

    def process_external_frame(self, frame):
        """
        Processes a single frame from an external source (WebRTC).
        Updates internal metrics state. Thread-safe.
        Note: Simple blocking implementation for immediate feedback.
        """
        # 1. rPPG Analysis
        self.ppg_analyzer.add_sample(frame)
        hr, confidence = self.ppg_analyzer.calculate_heart_rate()
        hrv = self.ppg_analyzer.calculate_hrv()
        
        with self.lock:
            # Update HR/HRV if signal is good
            if confidence > 30: # Lower threshold for webcams
                self.latest_readings['hr'] = hr
                self.latest_readings['hrv'] = hrv
                
            # Simulate/Proxy metrics
            # GSR Proxy (Higher HR + Lower HRV -> Higher GSR estimate)
            self.latest_readings['gsr'] = 5.0 + (self.latest_readings['hr'] - 60)/20.0 
             
            # Temp Proxy
            self.latest_readings['temp'] = 36.5 + (self.latest_readings['hr'] - 60)/50.0

            # Combined Stress Score
            stress_score = (
                (self.latest_readings['hr'] / 110.0) * 50 + 
                ((100 - self.latest_readings['hrv']) / 100.0) * 50
            ) 
            self.latest_readings['facial_stress'] = min(100, max(10, stress_score))
            self.latest_readings['confidence'] = confidence
            
            # Emotion
            if self.latest_readings['facial_stress'] > 60:
                self.latest_readings['emotion'] = "Stressed"
            elif self.latest_readings['facial_stress'] < 30:
                self.latest_readings['emotion'] = "Relaxed"
            else:
                self.latest_readings['emotion'] = "Neutral"

    # --- HARDWARE STRATEGY (Serial) ---
    def get_available_ports(self):
        if not HAS_SERIAL:
            return []
        ports = serial.tools.list_ports.comports()
        return [p.device for p in ports]
        
    def connect_hardware(self, port):
        if not HAS_SERIAL:
            return False
        try:
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            self.strategy = "HARDWARE"
            
            # Start Hardware Thread
            self.running = True
            self.thread = Thread(target=self._hardware_loop, daemon=True)
            self.thread.start()
            
            return True
        except Exception as e:
            print(f"Serial Error: {e}")
            return False
            
    def _disconnect_hardware(self):
        self.running = False
        if self.serial_connection:
            try:
                self.serial_connection.close()
            except:
                pass

    def _hardware_loop(self):
        """Read loop for Arduino/Hardware Serial. Expects format: HR:x,GSR:y,TEMP:z"""
        while self.running and self.serial_connection and self.serial_connection.is_open:
            try:
                line = self.serial_connection.readline().decode('utf-8').strip()
                if not line:
                    continue
                
                # Parse Data
                # Example: "HR:75,GSR:3.4,TEMP:37.1"
                parts = line.split(',')
                updates = {}
                for p in parts:
                    if ':' in p:
                        key, val = p.split(':')
                        key = key.strip().upper()
                        try:
                            val = float(val)
                            if key == 'HR': updates['hr'] = val
                            elif key == 'GSR': updates['gsr'] = val
                            elif key == 'TEMP': updates['temp'] = val
                            elif key == 'HRV': updates['hrv'] = val
                        except ValueError:
                            pass
                
                if updates:
                    with self.lock:
                        self.latest_readings.update(updates)
                        self.latest_readings['confidence'] = 100.0 # Trust hardware
                        
            except Exception as e:
                print(f"Hardware Read Error: {e}")
                time.sleep(1)

# Singleton Export
sensor_manager = SensorManager()

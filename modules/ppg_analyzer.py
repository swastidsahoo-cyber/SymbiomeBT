"""
PPG (Photoplethysmography) Analysis from Camera
Extracts heart rate from facial video using color changes
"""
import cv2
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import Tuple, Optional

class PPGAnalyzer:
    """Extract heart rate from facial video using PPG"""
    
    def __init__(self, fps: int = 30, window_size: int = 300):
        self.fps = fps
        self.window_size = window_size  # 10 seconds at 30fps
        self.signal_buffer = []
        
    def extract_roi(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """Extract forehead region of interest"""
        # Convert to RGB
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        
        # Use Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None
        
        # Get largest face
        (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
        
        # Extract forehead ROI (top 30% of face)
        forehead_y = y + int(h * 0.1)
        forehead_h = int(h * 0.3)
        forehead_x = x + int(w * 0.25)
        forehead_w = int(w * 0.5)
        
        roi = frame[forehead_y:forehead_y+forehead_h, 
                   forehead_x:forehead_x+forehead_w]
        
        return roi
    
    def extract_green_channel(self, roi: np.ndarray) -> float:
        """Extract mean green channel intensity (most sensitive to blood volume)"""
        if roi is None or roi.size == 0:
            return 0.0
        
        green_channel = roi[:, :, 1]  # G channel in RGB
        return np.mean(green_channel)
    
    def add_sample(self, frame: np.ndarray) -> None:
        """Add frame to signal buffer"""
        roi = self.extract_roi(frame)
        if roi is not None:
            green_value = self.extract_green_channel(roi)
            self.signal_buffer.append(green_value)
            
            # Keep only recent samples
            if len(self.signal_buffer) > self.window_size:
                self.signal_buffer.pop(0)
    
    def calculate_heart_rate(self) -> Tuple[float, float]:
        """
        Calculate heart rate from signal buffer using FFT
        Returns: (heart_rate_bpm, confidence)
        """
        if len(self.signal_buffer) < self.window_size:
            return 0.0, 0.0
        
        # Detrend signal
        signal_array = np.array(self.signal_buffer)
        detrended = signal.detrend(signal_array)
        
        # Apply Hamming window
        windowed = detrended * np.hamming(len(detrended))
        
        # Bandpass filter (0.7 Hz - 3.5 Hz = 42-210 BPM)
        sos = signal.butter(4, [0.7, 3.5], btype='band', fs=self.fps, output='sos')
        filtered = signal.sosfilt(sos, windowed)
        
        # FFT
        fft_vals = fft(filtered)
        fft_freq = fftfreq(len(filtered), 1/self.fps)
        
        # Only positive frequencies in valid range
        valid_idx = (fft_freq > 0.7) & (fft_freq < 3.5)
        valid_fft = np.abs(fft_vals[valid_idx])
        valid_freq = fft_freq[valid_idx]
        
        if len(valid_fft) == 0:
            return 0.0, 0.0
        
        # Find peak frequency
        peak_idx = np.argmax(valid_fft)
        peak_freq = valid_freq[peak_idx]
        heart_rate = peak_freq * 60  # Convert Hz to BPM
        
        # Calculate confidence (peak prominence)
        peak_power = valid_fft[peak_idx]
        avg_power = np.mean(valid_fft)
        confidence = min(100, (peak_power / avg_power) * 20)
        
        return heart_rate, confidence
    
    def calculate_hrv(self) -> float:
        """
        Calculate HRV (RMSSD) from signal
        Returns: HRV in milliseconds
        """
        if len(self.signal_buffer) < self.window_size:
            return 0.0
        
        # Detect peaks (R-peaks in PPG)
        signal_array = np.array(self.signal_buffer)
        detrended = signal.detrend(signal_array)
        
        # Find peaks
        peaks, _ = signal.find_peaks(detrended, distance=self.fps//3)
        
        if len(peaks) < 2:
            return 0.0
        
        # Calculate RR intervals
        rr_intervals = np.diff(peaks) / self.fps * 1000  # Convert to ms
        
        # RMSSD (Root Mean Square of Successive Differences)
        if len(rr_intervals) < 2:
            return 0.0
        
        successive_diffs = np.diff(rr_intervals)
        rmssd = np.sqrt(np.mean(successive_diffs ** 2))
        
        return rmssd
    
    def reset(self):
        """Clear signal buffer"""
        self.signal_buffer = []

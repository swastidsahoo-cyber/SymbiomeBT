import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    print("Testing SensorManager Import...")
    from modules.sensor_manager import sensor_manager
    print("SUCCESS: SensorManager Imported.")
    
    print("Testing DataEngine Integration...")
    from data_engine import data_engine
    print("SUCCESS: DataEngine Imported.")
    
    # Test Default State
    try:
        import mediapipe
        print("DEBUG: Raw 'import mediapipe' SUCCEEDED")
    except Exception as e:
        print(f"DEBUG: Raw 'import mediapipe' FAILED: {e}")

    data = data_engine.get_live_data()
    print("Initial Data Packet:", data)
    
    # Verify MediaPipe Loading
    from modules.sensor_manager import HAS_MEDIAPIPE
    if HAS_MEDIAPIPE:
        print("SUCCESS: MediaPipe Library Detected.")
        if sensor_manager.face_mesh is not None:
             print("SUCCESS: FaceMesh Initialized.")
        else:
             print("WARNING: FaceMesh not initialized (Webcam not started yet, which is expected).")
    else:
        print("FAILURE: MediaPipe Library NOT Detected.")
    
    if data['hrv'] > 0:
        print("SUCCESS: Data Flow Functional.")
    else:
        print("FAILURE: Data Flow Issue.")
        
except Exception as e:
    print(f"FAILURE: {e}")
    import traceback
    traceback.print_exc()

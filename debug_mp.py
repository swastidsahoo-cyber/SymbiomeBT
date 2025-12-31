import mediapipe
import pkgutil
import sys

print(f"Python Version: {sys.version}")
print(f"MediaPipe File: {getattr(mediapipe, '__file__', 'Unknown')}")
print(f"MediaPipe Path: {getattr(mediapipe, '__path__', 'Unknown')}")
print(f"Dir(mediapipe): {dir(mediapipe)}")

try:
    print("\n--- Submodules ---")
    for importer, modname, ispkg in pkgutil.iter_modules(mediapipe.__path__):
        print(f"Found: {modname} (is_pkg={ispkg})")
except Exception as e:
    print(f"Error listing modules: {e}")

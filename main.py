from audio3d.tracker import SimpleCentroidTracker
from audio3d.geometry import calculate_azimuth, calculate_distance
from audio3d.audio_processor import apply_ild_itd
from audio3d.csv_handler import CSVWriter

def main():
    print("Audio3D App Running...")
    tracker = SimpleCentroidTracker()
    writer = CSVWriter("output.csv")

    # Example: append a frame
    writer.append([1, 10, 20, 30, 40, 1.2, 1])

if __name__ == "__main__":
    main()

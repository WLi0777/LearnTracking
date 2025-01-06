from dataprep import extract_frames

if __name__ == "__main__":
    extract_frames(
        input_path="path/to/your/video.mp4",  # Replace with your video path
        output_folder="path/to/output/folder",  # Replace with output folder
        percentage=10,  # Extract 10% of frames
        method="uniform",  # Use "uniform" or "random"
        seed=42  # Optional, for reproducibility in "random" method
    )
    print("Frame extraction completed!")

from dataprep.video_extraction import extract_frames

if __name__ == "__main__":
    extract_frames(
        input_path="path/to/your/video.mp4",  # Replace with the path (to a video file or a folder containing videos)
        output_folder="path/to/output/folder",  # Replace with the desired output folder
        percentage=10,  # Extract 10% of frames
        method="uniform",  # Choose "uniform" or "random"
        seed=40  # Optional seed for reproducibility in "random" method
    )
    print("Frames extracted successfully!")

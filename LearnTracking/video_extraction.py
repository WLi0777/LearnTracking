import os
import cv2
import random

def extract_frames(
        input_path,
        output_folder=None,
        percentage=100,
        method="uniform",
        seed=None
):
    """
    Extract frames from videos and save them into specified folders.

    Args:
        input_path (str): Path to a video file or a folder containing videos.
        output_folder (str): Root directory to save extracted frames. If None, a folder with the video name is created.
        percentage (int): Percentage of frames to extract (0-100).
        method (str): Extraction method, either "uniform" (evenly spaced frames) or "random".
        seed (int): Random seed for reproducibility when using the "random" method.

    Returns:
        None
    """
    # Check if the input is a folder or a single file
    if os.path.isdir(input_path):
        videos = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(('.mp4', '.avi'))]
    elif os.path.isfile(input_path):
        videos = [input_path]
    else:
        raise ValueError("The input path must be a valid video file or a folder containing videos.")

    # Process each video
    for video_path in videos:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        save_folder = output_folder or os.path.join(os.getcwd(), video_name)
        os.makedirs(save_folder, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if method == "random":
            if seed is not None:
                random.seed(seed)
            frame_indices = sorted(random.sample(range(total_frames), int(total_frames * percentage / 100)))
        elif method == "uniform":
            step = max(1, total_frames // (total_frames * percentage // 100))
            frame_indices = list(range(0, total_frames, step))
        else:
            raise ValueError(f"Unknown extraction method: {method}")

        frame_counter = 0
        for i in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                continue
            # Save frame with the video name in the filename
            frame_name = f"{video_name}_img{i:04d}.png"
            cv2.imwrite(os.path.join(save_folder, frame_name), frame)
            frame_counter += 1

        cap.release()
        print(f"Frames from video '{video_name}' have been saved to '{save_folder}'.")
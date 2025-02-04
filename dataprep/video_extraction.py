import os
import cv2
import random
import numpy as np
from tqdm import tqdm
from sklearn.cluster import MiniBatchKMeans

# for kmeans methods, find original code: from deeplabcut.utils import frameselectiontools
def extract_frames(
        input_path,
        output_folder=None,
        percentage=None,
        frames_number=None,
        method=None,
        seed=None,
        subfolder=True,
        resize_width=30,
        batch_size=100,
        max_iter=50
):
    """
    Extract frames from videos and save them into specified folders.

    Args:
        input_path (str): Path to a video file or a folder containing videos.
        output_folder (str): Root directory to save extracted frames. If None, a folder with the video name is created.
        percentage (int, optional): Percentage of frames to extract (0-100). Used if frames_number is None.
        frames_number (int, optional): Number of frames to extract. Overrides percentage if set.
        method (str): Extraction method, either "uniform", "random", or "kmeans".
        seed (int): Random seed for reproducibility.
        subfolder (bool): Whether to save frames in a subfolder per video.
        resize_width (int): Resize the frame width for K-means clustering.
        batch_size (int): Batch size for K-means clustering.
        max_iter (int): Maximum iterations for K-means.

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

    # Create a total folder if multiple videos are present
    if len(videos) > 1:
        total_frames_folder = os.path.join(output_folder,
                                           "total_video_frames") if output_folder else "total_video_frames"
        os.makedirs(total_frames_folder, exist_ok=True)
    else:
        total_frames_folder = os.path.join(output_folder,
                                           "total_video_frames") if output_folder else "total_video_frames"
        os.makedirs(total_frames_folder, exist_ok=True)

        # Process each video
    for video_path in videos:
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        # Create a specific folder for this video
        save_folder = os.path.join(output_folder, video_name) if output_folder else video_name
        os.makedirs(save_folder, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Video '{video_name}' has '{total_frames}' frames")

        # Select frames based on the method
        if frames_number is not None:
            if frames_number > total_frames:
                print(
                    f"Warning: Requested {frames_number} frames, but video only has {total_frames} frames. Extracting all.")
                frames_number = total_frames
            if method == "random":
                if seed is not None:
                    random.seed(seed)
                frame_indices = sorted(random.sample(range(total_frames), frames_number))
            elif method == "uniform":
                step = max(1, total_frames // frames_number)
                frame_indices = list(range(0, total_frames, step))[:frames_number]
            elif method == "kmeans":
                frame_indices = kmeans_frame_selection(cap, frames_number, resize_width, batch_size, max_iter)
            else:
                raise ValueError(f"Unknown extraction method: {method}")
        elif percentage is not None:
            if percentage < 0 or percentage > 100:
                raise ValueError("Percentage must be between 0 and 100.")
            num_frames = int(total_frames * (percentage / 100))
            if method == "random":
                if seed is not None:
                    random.seed(seed)
                frame_indices = sorted(random.sample(range(total_frames), num_frames))
            elif method == "uniform":
                step = max(1, total_frames // num_frames)
                frame_indices = list(range(0, total_frames, step))[:num_frames]
            else:
                raise ValueError(f"Unknown extraction method: {method}")
        else:
            raise ValueError("Either 'percentage' or 'frames_number' must be specified.")

        frame_counter = 0
        for i in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                continue

            # Save frame with the video name in the filename
            frame_name = f"{video_name}_img{i:04d}.png"
            # Save to the specific folder for this video
            if subfolder:
                cv2.imwrite(os.path.join(save_folder, frame_name), frame)
                # print(f"Frames from video '{video_name}' have been saved to '{save_folder}'.")

            # Additionally, save to the total frames folder if applicable
            if total_frames_folder:
                cv2.imwrite(os.path.join(total_frames_folder, frame_name), frame)

            frame_counter += 1

        cap.release()

    if total_frames_folder:
        print(f"All frames have also been saved to the total frames folder '{total_frames_folder}'.")

def kmeans_frame_selection(cap, num_frames, resize_width=30, batch_size=100, max_iter=50):
    """
    Select key frames with distinct features using the K-means clustering method.

    Args:
        cap (cv2.VideoCapture): Video capture object.
        num_frames (int): Number of frames to select.
        resize_width (int): Resize the frame width to reduce computational cost.
        batch_size (int): Batch size for K-means processing.
        max_iter (int): Maximum iterations for K-means.

    Returns:
        List[int]: Indices of the selected frames.
    """

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = np.linspace(0, total_frames - 1, num=min(1000, total_frames), dtype=int)

    feature_vectors = []
    for i in tqdm(frame_indices, desc="Extracting frames for K-means clustering"):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            continue

        frame_resized = cv2.resize(frame, (resize_width, resize_width))
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        feature_vectors.append(gray.flatten())

    if len(feature_vectors) < num_frames:
        print(f"Warning: Not enough frames for K-means. Returning all {len(feature_vectors)} frames.")
        return frame_indices[:num_frames]

    print("Performing K-means clustering...")
    kmeans = MiniBatchKMeans(n_clusters=num_frames, batch_size=batch_size, max_iter=max_iter)
    kmeans.fit(feature_vectors)

    selected_frames = []
    for cluster_id in range(num_frames):
        cluster_indices = np.where(kmeans.labels_ == cluster_id)[0]
        if len(cluster_indices) > 0:
            selected_frames.append(frame_indices[random.choice(cluster_indices)])

    return sorted(selected_frames)

import os

def create_folders(video_folder="ori_video", frames_folder="frames_labeling", labeled_folder="json_file", total_frames="frames_labeling/total_video_frames"):
    """
    Create necessary folders to avoid duplicates.
    
    Args:
        video_folder (str): Path to the video folder
        frames_folder (str): Path to the frames folder
        labeled_folder (str): Path to the labeled folder
        total_frames (str): Path to the total_video_frames folder
    """
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(frames_folder, exist_ok=True)
    os.makedirs(labeled_folder, exist_ok=True)
    os.makedirs(total_frames, exist_ok=True)

    print(f"Created folders: {video_folder}, {frames_folder}, {labeled_folder}")

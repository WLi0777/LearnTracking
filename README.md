# LearnTracking

## Step 1. Installation

To install the library, use the following command:
  ```
  pip install git+https://github.com/WLi0777/LearnTracking.git
  ```
Make sure you have Python 3.6 or higher installed.
<br><br>
## Step 2. Prepare Images for Labeling

To use [CVAT](https://www.cvat.ai/) as the labeling tool, note that the platform allows exporting annotated datasets for free but does not provide an option to export the original images used for labeling. Exporting a dataset with images requires upgrading the account.

As a workaround, you can process videos into selected frames and import them into CVAT. The function extract_frames helps you achieve this by extracting frames from a video or a folder of videos.

Here’s a quick [example](https://github.com/WLi0777/LearnTracking/blob/main/examples/example_video_extraction.py) of how to use extract_frames:
  ```
  from dataprep.frame_extractor import extract_frames

  extract_frames(
      input_path="path/to/your/video.mp4",  # Replace with the path (to a video file or a folder containing videos)
      output_folder="path/to/output/folder",  # Replace with the desired output folder
      percentage=10,  # Extract 10% of frames
      method="uniform",  # Choose "uniform" for evenly spaced frames or "random"
      seed=42  # Optional seed for reproducibility in "random" method
  )
  ```

Once frames are extracted, upload the images to CVAT for annotation. This ensures that the images used for labeling are accessible and manageable.


my_tracking_tools/ # Project root directory ├── dataprep/ # Main code package │ ├── init.py # Package initialization file │ ├── frame_extractor.py # Contains the extract_frames function │ ├── yolo_dataset.py # Contains the prepare_yolo_dataset function │ ├── util.py # Utility functions (optional) ├── examples/ # Example scripts │ ├── example_extraction.py │ ├── example_yolo.py ├── tests/ # Test scripts │ ├── test_frame_extractor.py │ ├── test_yolo_dataset.py ├── setup.py # Project setup configuration ├── requirements.txt # Dependency list ├── README.md # Project documentation ├── LICENSE # Project license


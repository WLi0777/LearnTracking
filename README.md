# LearnTracking

## Step 1. Installation

To install the library, use the following command:
  ```
  pip install git+https://github.com/WLi0777/LearnTracking.git
  ```
Make sure you have Python 3.6 or higher installed.

## Step 2. Prepare Images for Labeling

To use [CVAT](https://www.cvat.ai/) as the labeling tool, note that the platform allows exporting annotated datasets for free but does not provide an option to export the original images used for labeling. Exporting a dataset with images requires upgrading the account.
As a workaround, you can process videos into selected frames and import them into CVAT. The function extract_frames helps you achieve this by extracting frames from a video or a folder of videos.

Here’s a quick [example](https://github.com/WLi0777/LearnTracking/blob/main/examples/example_video_extraction.py) of how to use extract_frames:

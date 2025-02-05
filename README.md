# LearnTracking

Follow along in google colab:

YOLO tracking - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]([https://colab.research.google.com/github/username/repository/blob/main/path/to/notebook.ipynb](https://colab.research.google.com/drive/1ezXN6JsHfz_kCNhIaHtToSQuWV0nizmV?usp=sharing))


## 1. Installation

To install the library, use the following command:

```
pip install git+https://github.com/WLi0777/LearnTracking.git
```
    
Make sure you have Python 3.6 or higher installed.
<br><br>

## 2. Prepare Images for Labeling

To use [CVAT](https://www.cvat.ai/) as the labeling tool, note that the platform allows exporting annotated datasets for free but does not provide an option to export the original images used for labeling. Exporting a dataset with images requires upgrading the account.

As a workaround, you can process videos into selected frames and import them into CVAT. The function extract_frames helps you achieve this by extracting frames from a video or a folder of videos.

Here’s a quick [example](https://github.com/WLi0777/LearnTracking/blob/main/examples/example_video_extraction.py) of how to use extract_frames:
    
```python
from dataprep.video_extraction import extract_frames

extract_frames(
        input_path = video_folder,
        output_folder = frames_folder,
        frames_number = 10,  # Extract 20 frames
        method = "uniform"  # Choose "uniform" or "random" or "kmeans"
        )
```
    
Directory structure：

```
├── videos_folder
│  ├── video01.mp4
│  ├── video02.mp4
│  └── video03.mp4

├── output_frames_folder
│  ├── video01
│  │  ├── video01_img0000.png
│  │  ├── video01_img0005.png
│  │  ├── video01_img0010.png
│  │  └──  ...
│  ├── video02
│  │  ├── video02_img0000.png
│  │  ├── video02_img0004.png
│  │  ├── video02_img0008.png
│  │  └──  ...
│  ├── video03
│  │  ├── video03_img0000.png
│  │  ├── video03_img0007.png
│  │  ├── video03_img0014.png
│  │  └──  ...
```

Once frames are extracted, upload the images to CVAT for annotation. This ensures that the images used for labeling are accessible and manageable.
<br><br>

## 3. Labeling in CVAT

In [CVAT](https://www.cvat.ai/), Projects, Tasks, and Jobs serve different purposes to streamline the labeling process. 

- **Projects** organize related tasks and share common metadata like labels and guidelines.
- **Tasks** represent individual datasets (e.g., a video or images) and track progress.
- **Jobs** are subdivisions of tasks, splitting large datasets into smaller sections for concurrent labeling.

Once annotations are complete, export the labeled dataset in the desired format -- [**YOLO Detection 1.0**](https://docs.ultralytics.com/datasets/pose/#ultralytics-yolo-format).
<br><br>

## 4. Training a Model with YOLO

### Prepare Dataset

To train a YOLO model, first download and extract the annotated data exported from CVAT. After extraction, you should have a folder structure similar to this:

```
├── yolo_test
│  ├── data.yaml
│  ├── train.txt
│  ├── labels
│  │  ├── train
│  │  │  ├── video01_img0005.txt
│  │  │  ├── video02_img0010.txt
│  │  │  └──  ...
```

Before starting training, the configuration file (data.yaml) needs to be updated, and the data should be split into training and validation sets. Additionally, the corresponding image files must be copied to their respective directories.

Use the provided [script](https://github.com/WLi0777/LearnTracking/blob/main/examples/example_yolo_prep.py) to preprocess the data.

```python
from dataprep.yolo_prep import prepare_yolo_dataset

prepare_yolo_dataset(
        base_folder=labeled_folder,
        source_images_folder=total_frames,
        train_percentage=80
    )
```

After processing, the folder structure will look like this:

```
├── yolo_test
│  ├── data.yaml
│  ├── labels
│  │  ├── train
│  │  │  ├── video01_img0005.txt
│  │  │  ├── video02_img0010.txt
│  │  │  └──  ...
│  │  ├── val
│  │  │  ├── video01_img0015.txt
│  │  │  ├── video02_img0020.txt
│  │  │  └──  ...
│  ├── images
│  │  ├── train
│  │  │  ├── video01_img0005.png
│  │  │  ├── video02_img0010.png
│  │  │  └──  ...
│  │  ├── val
│  │  │  ├── video01_img0015.png
│  │  │  ├── video02_img0020.png
│  │  │  └──  ...
```


### Install YOLO

Install the YOLO training library using the following command:

```
pip install ultralytics
```


### Training the Model

Once the preprocessing is complete, you can start training your YOLO model with the following code:

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n-pose.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="yolo_test/data.yaml", epochs=100, imgsz=640)
```

> If the pretrained model is not downloaded automatically, visit this [link](https://docs.ultralytics.com/tasks/pose/#real-world-applications) to download the desired model and update the path accordingly.










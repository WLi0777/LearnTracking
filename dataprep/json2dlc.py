import warnings
from pathlib import Path
import deeplabcut
from deeplabcut import DEBUG
from deeplabcut.utils.auxfun_videos import VideoReader
import json
import os
import shutil
import csv


def create_new_project(
    project,
    experimenter,
    json_folder,
    videos_dir,
    frames_dir,
    working_directory=None,
    copy_videos=False,
    multianimal = False,
    videotype=""
):
    r"""Create the necessary folders and files for a new project.

    Creating a new project involves creating the project directory, sub-directories and
    a basic configuration file. The configuration file is loaded with the default
    values. Change its parameters to your projects need.

    Parameters
    ----------
    project : string
        The name of the project.

    experimenter : string
        The name of the experimenter.

    json_folder: string
        The path of the folder (contains .json file)

    videos : list[str]
        A list of strings representing the full paths of the videos to include in the
        project. If the strings represent a directory instead of a file, all videos of
        ``videotype`` will be imported.

    working_directory : string, optional
        The directory where the project will be created. The default is the
        ``current working directory``.

    copy_videos : bool, optional, Default: False.
        If True, the videos are copied to the ``videos`` directory. If False, symlinks
        of the videos will be created in the ``project/videos`` directory; in the event
        of a failure to create symbolic links, videos will be moved instead.

    multianimal: bool, optional. Default: False.
        For creating a multi-animal project (introduced in DLC 2.2)

    Returns
    -------
    str
        Path to the new project configuration file.

    """
    from datetime import datetime as dt
    from deeplabcut.utils import auxiliaryfunctions

    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    if json_files:
        json_file = os.path.join(json_folder, json_files[0])
        print(f"Using JSON file: {json_file}")
    else:
        print("No JSON file found in the specified folder.")

    videotypes = (".mp4", ".avi", ".mov", ".mkv")

    months_3letter = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
    }
    date = dt.today()
    month = months_3letter[date.month]
    day = date.day
    d = str(month[0:3] + str(day))
    date = dt.today().strftime("%Y-%m-%d")

    if working_directory is None:
        working_directory = "."
    wd = Path(working_directory).resolve()
    project_name = f"{project}-{experimenter}-{date}"
    project_path = wd / project_name

    if not DEBUG and project_path.exists():
        print(f'Project "{project_path}" already exists!')
        return os.path.join(str(project_path), "config.yaml")
    video_path = project_path / "videos"
    for p in [video_path, project_path / "labeled-data", project_path / "training-datasets",
              project_path / "dlc-models"]:
        p.mkdir(parents=True, exist_ok=DEBUG)
        print(f'Created "{p}"')

    videos = []
    videos_dir = Path(videos_dir).resolve()
    if videos_dir.is_dir():
        for ext in videotypes:
            videos.extend(videos_dir.rglob(f"*{ext}"))
        if not videos:
            print(f"No videos found in {videos_dir} with types {videotypes}.")
            return
    else:
        print(f"{videos_dir} is not a valid directory.")
        return


    destinations = [video_path / vp.name for vp in videos]
    if copy_videos:
        print("Copying the videos")
        for src, dst in zip(videos, destinations):
            shutil.copy(src, dst)
    else:
        print("Attempting to create symbolic links for videos...")
        for src, dst in zip(videos, destinations):
            try:
                os.symlink(src, dst)
                print(f"Created symbolic link for {src} to {dst}")
            except OSError:
                shutil.copy(src, dst)
                print(f"Copied {src} to {dst}")

    video_sets = {}
    for video in destinations:
        try:
            video = str(video.resolve())
            vid = VideoReader(video)
            video_sets[video] = {"crop": ", ".join(map(str, vid.get_bbox()))}
        except IOError:
            warnings.warn(f"Cannot open video file {video}! Skipping...")
            os.remove(video)

    if not video_sets:
        shutil.rmtree(project_path, ignore_errors=True)
        warnings.warn("No valid videos found. Project was not created.")
        return "nothingcreated"



    if multianimal:  # parameters specific to multianimal project
        print('No multianimal in this project')
    else:
        cfg_file, ruamelFile = auxiliaryfunctions.create_config_template()
        cfg_file["multianimalproject"] = False
        cfg_file["bodyparts"], cfg_file["skeleton"] = json2dlc_config_single(json_file)
        cfg_file["default_augmenter"] = "default"
        cfg_file["default_net_type"] = "resnet_50"

    # common parameters:
    cfg_file["Task"] = project
    cfg_file["scorer"] = experimenter
    cfg_file["video_sets"] = video_sets
    cfg_file["project_path"] = str(project_path)
    cfg_file["date"] = d
    cfg_file["cropping"] = False
    cfg_file["start"] = 0
    cfg_file["stop"] = 1
    cfg_file["numframes2pick"] = 20
    cfg_file["TrainingFraction"] = [0.95]
    cfg_file["iteration"] = 0
    cfg_file["snapshotindex"] = -1
    cfg_file["x1"] = 0
    cfg_file["x2"] = 640
    cfg_file["y1"] = 277
    cfg_file["y2"] = 624
    cfg_file["batch_size"] = (
        8  # batch size during inference (video - analysis); see https://www.biorxiv.org/content/early/2018/10/30/457242
    )
    cfg_file["corner2move2"] = (50, 50)
    cfg_file["move2corner"] = True
    cfg_file["skeleton_color"] = "black"
    cfg_file["pcutoff"] = 0.6
    cfg_file["dotsize"] = 12  # for plots size of dots
    cfg_file["alphavalue"] = 0.7  # for plots transparency of markers
    cfg_file["colormap"] = "rainbow"  # for plots type of colormap

    projconfigfile = os.path.join(str(project_path), "config.yaml")
    # Write dictionary to yaml  config file
    auxiliaryfunctions.write_config(projconfigfile, cfg_file)

    print('Generated "{}"'.format(project_path / "config.yaml"))
    print(
        "\nA new project with name %s is created at %s and a configurable file (config.yaml) is stored there. Change the parameters in this file to adapt to your project's needs.\n Once you have changed the configuration file, use the function 'extract_frames' to select frames for labeling.\n. [OPTIONAL] Use the function 'add_new_videos' to add new videos to your project (at any stage)."
        % (project_name, str(wd))
    )

    copy_images(frames_dir, project_path, json_file, experimenter)
    deeplabcut.convertcsv2h5(projconfigfile, userfeedback= False)
    deeplabcut.create_training_dataset(projconfigfile)

    return projconfigfile


def json2dlc_config_single(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    catalogue = data['categories']
    bodyparts = []
    skeleton = []

    for category in catalogue:
        if 'keypoints' in category:
            bodyparts.extend(category['keypoints'])

        if 'skeleton' in category:
            for pair in category['skeleton']:

                index1, index2 = pair[0] - 1, pair[1] - 1

                if index1 >= len(category['keypoints']) or index2 >= len(category['keypoints']):
                    print(f"Invalid pair: {pair}")
                    continue
                skeleton.append([bodyparts[index1], bodyparts[index2]])

    bodyparts = list(dict.fromkeys(bodyparts))
    skeleton = list(dict.fromkeys(tuple(pair) for pair in skeleton))
    skeleton = [list(pair) for pair in skeleton]

    return bodyparts, skeleton

def copy_images(frame_dir, proj_path, js_file, scorer):
    with open(js_file, 'r') as f:
        data = json.load(f)

    images = data.get('images', [])
    categories = data.get('categories', [])
    annotations = data.get('annotations', [])

    bodyparts = []
    for category in categories:
        if 'keypoints' in category:
            bodyparts.extend(category['keypoints'])

    for image in images:
        file_name = image.get('file_name')
        if file_name:
            found = False
            for root, dirs, files in os.walk(frame_dir):
                if file_name in files:
                    found = True
                    img_path = os.path.join(root, file_name)

                    video_name = file_name[:file_name.find('_img')]

                    target_dir = os.path.join(proj_path, "labeled-data", video_name)
                    os.makedirs(target_dir, exist_ok=True)

                    new_file_name = file_name[file_name.find('img'):] if 'img' in file_name else file_name
                    target_path = os.path.join(target_dir, new_file_name)

                    shutil.copy(img_path, target_path)

                    csv_file = os.path.join(target_dir, f"CollectedData_{scorer}.csv")

                    if not os.path.exists(csv_file):
                        with open(csv_file, mode='w', newline='') as f_csv:
                            writer = csv.writer(f_csv)

                            writer.writerow(['scorer'] + [''] * 2 + [f'{scorer}'] * (2 * len(bodyparts)))
                            expanded_bodyparts = [item for item in bodyparts for _ in range(2)]
                            writer.writerow(['bodyparts'] + [''] * 2 + expanded_bodyparts)
                            writer.writerow(['coords'] + [''] * 2 + ['x', 'y'] * len(bodyparts))

                    with open(csv_file, mode='a', newline='') as f_csv:
                        writer = csv.writer(f_csv)
                        relevant_annotations = [annotation for annotation in annotations if
                                                annotation['image_id'] == image['id']]

                        for annotation in relevant_annotations:
                            coords = []
                            for i, keypoint in enumerate(bodyparts):
                                if i * 3 + 1 < len(annotation['keypoints']):
                                    x = annotation['keypoints'][i * 3]
                                    y = annotation['keypoints'][i * 3 + 1]
                                    coords.extend([x, y])
                                else:
                                    coords.extend([None, None])

                            row = ['labeled-data', video_name, new_file_name] + coords
                            writer.writerow(row)

            if not found:
                print(f"Image {file_name} not found in {frame_dir}")







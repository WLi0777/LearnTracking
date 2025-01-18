from dataprep.json2dlc import create_new_project

create_new_project(project='test',
                   experimenter='wl',
                   json_file=r"C:\Users\wl077\Downloads\job_1961852_annotations_2025_01_18_08_47_14_coco keypoints 1.0\annotations\person_keypoints_default.json",
                   videos_dir=r'C:\Users\wl077\Downloads\video',
                   frames_dir = r'C:\Users\wl077\Downloads\frames_labeling'
                   )

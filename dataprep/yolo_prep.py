import os
import shutil
import yaml  # Ensure PyYAML is installed: pip install pyyaml
import random
import zipfile


def prepare_yolo_dataset(base_folder, source_images_folder, train_percentage):
    """
    Prepare YOLO dataset by copying images and splitting them into train and val sets.

    Args:
        base_folder (str): Path to the YOLO dataset base folder (e.g., 'C:\\Users\\wl077\\Downloads\\yolotest').
        source_images_folder (str): Path to the folder containing image files.
        train_percentage (int): Percentage of data to assign to the train set (0-100).
    """
    zip_files = [f for f in os.listdir(base_folder) if f.endswith('.zip')]

    if zip_files:
        zip_path = os.path.join(base_folder, zip_files[0])  
        zip_name = zip_files[0].replace('.zip','')
        # print(zip_name)
        extract_folder = os.path.join(base_folder, zip_name)
        
        # Ensure extraction folder exists
        os.makedirs(extract_folder, exist_ok=True)

        # Extract ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        print(f"Extracted {zip_files[0]} to {extract_folder}")


        # Define the labels and images folders based on the base folder
        labels_train_folder = os.path.join(extract_folder, "labels", "train")
        labels_val_folder = os.path.join(extract_folder, "labels", "val")
        images_train_folder = os.path.join(extract_folder, "images", "train")
        images_val_folder = os.path.join(extract_folder, "images", "val")

        os.makedirs(labels_train_folder, exist_ok=True)
        os.makedirs(labels_val_folder, exist_ok=True)
        os.makedirs(images_train_folder, exist_ok=True)
        os.makedirs(images_val_folder, exist_ok=True)


        # Check if labels/train folder exists
        if not os.path.isdir(labels_train_folder):
            raise FileNotFoundError(f"Labels folder not found: {labels_train_folder}")

        # Get all .txt files in the labels/train folder
        label_files = [f for f in os.listdir(labels_train_folder) if f.endswith('.txt')]

        # Shuffle the label files
        random.shuffle(label_files)

        # Calculate the split index
        split_index = int(len(label_files) * train_percentage / 100)

        # Split into train and val
        train_files = label_files[:split_index]
        val_files = label_files[split_index:]

        # Process train files
        for label_file in train_files:
            base_name = os.path.splitext(label_file)[0]

            # Move label file to train folder
            shutil.move(
                os.path.join(labels_train_folder, label_file),
                os.path.join(labels_train_folder, label_file)
            )

            # Copy corresponding image file to train folder
            for ext in ['.jpg', '.jpeg', '.png']:
                image_file = os.path.join(source_images_folder, base_name + ext)
                if os.path.exists(image_file):
                    shutil.copy(image_file, os.path.join(images_train_folder, base_name + ext))
                    break
            else:
                print(f"Warning: No matching image found for label file '{label_file}'")

        # Process val files
        for label_file in val_files:
            base_name = os.path.splitext(label_file)[0]

            # Move label file to val folder
            shutil.move(
                os.path.join(labels_train_folder, label_file),
                os.path.join(labels_val_folder, label_file)
            )

            # Copy corresponding image file to val folder
            for ext in ['.jpg', '.jpeg', '.png']:
                image_file = os.path.join(source_images_folder, base_name + ext)
                if os.path.exists(image_file):
                    shutil.copy(image_file, os.path.join(images_val_folder, base_name + ext))
                    break
            else:
                print(f"Warning: No matching image found for label file '{label_file}'")

        print(f"Train and val split completed. Train: {len(train_files)} frames, Val: {len(val_files)} frames")

        # Update the data.yaml file
        update_data_yaml(extract_folder)
        delete_train_txt(extract_folder)



def update_data_yaml(base_folder):
    """
    Update the first YAML file found in the base folder.

    Args:
        base_folder (str): Path to the folder containing YAML files (e.g., 'C:\\Users\\wl077\\Downloads\\yolotest').
    """
    # Scan for YAML files in the folder
    yaml_files = [f for f in os.listdir(base_folder) if f.endswith('.yaml')]

    if not yaml_files:
        raise FileNotFoundError(f"No YAML files found in the folder: {base_folder}")

    # Use the first YAML file found
    yaml_file_path = os.path.join(base_folder, yaml_files[0])

    # Read the YAML file
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Update the fields
    base_folder2 = os.path.join('/content', base_folder)
    data['path'] = base_folder2
    data['train'] = os.path.join(base_folder2, "images", "train")
    data['val'] = os.path.join(base_folder2, "images", "val")

    # Write back the updated YAML file
    with open(yaml_file_path, 'w') as file:
        yaml.safe_dump(data, file)

    print(f"Updated YAML file at: {yaml_file_path}")

def delete_train_txt(base_folder):
    """
    Attempt to delete 'train.txt' in the base folder.

    Args:
        base_folder (str): Path to the base folder (e.g., 'C:\\Users\\wl077\\Downloads\\yolotest').
    """
    train_txt_path = os.path.join(base_folder, "train.txt")

    if os.path.isfile(train_txt_path):
        try:
            os.remove(train_txt_path)
            # print(f"'train.txt' has been successfully deleted from {base_folder}")
        except Exception as e:
            print(f"Failed to delete 'train.txt': {e}")
    else:
        print(f"'train.txt' does not exist in {base_folder}")

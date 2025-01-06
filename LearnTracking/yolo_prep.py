import os
import shutil
import yaml  # Ensure PyYAML is installed: pip install pyyaml
import random
def prepare_yolo_dataset(base_folder, source_images_folder, train_percentage):
    """
    Prepare YOLO dataset by copying images and splitting them into train and val sets.

    Args:
        base_folder (str): Path to the YOLO dataset base folder (e.g., 'C:\\Users\\wl077\\Downloads\\yolotest').
        source_images_folder (str): Path to the folder containing image files.
        train_percentage (int): Percentage of data to assign to the train set (0-100).
    """
    # Define the labels and images folders based on the base folder
    labels_train_folder = os.path.join(base_folder, "labels", "train")
    labels_val_folder = os.path.join(base_folder, "labels", "val")
    images_train_folder = os.path.join(base_folder, "images", "train")
    images_val_folder = os.path.join(base_folder, "images", "val")

    # Ensure the output folders exist
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

    print(f"Train and val split completed. Train: {len(train_files)}, Val: {len(val_files)}")

    # Update the data.yaml file
    update_data_yaml(base_folder)
    delete_train_txt(base_folder)


def update_data_yaml(base_folder):
    """
    Update the data.yaml file in the base folder.

    Args:
        base_folder (str): Path to the YOLO dataset base folder (e.g., 'C:\\Users\\wl077\\Downloads\\yolotest').
    """
    data_yaml_path = os.path.join(base_folder, "data.yaml")

    # Check if the data.yaml file exists
    if not os.path.isfile(data_yaml_path):
        raise FileNotFoundError(f"data.yaml file not found at: {data_yaml_path}")

    # Read the YAML file
    with open(data_yaml_path, 'r') as file:
        data = yaml.safe_load(file)

    # Update the path, train, and add val fields
    data['path'] = base_folder
    data['train'] = "images/train"
    data['val'] = "images/val"

    # Write back the updated YAML file
    with open(data_yaml_path, 'w') as file:
        yaml.safe_dump(data, file)

    print(f"Updated data.yaml file at: {data_yaml_path}")


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
            print(f"'train.txt' has been successfully deleted from {base_folder}")
        except Exception as e:
            print(f"Failed to delete 'train.txt': {e}")
    else:
        print(f"'train.txt' does not exist in {base_folder}")

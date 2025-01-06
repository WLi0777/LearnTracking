from dataprep.yolo_prep import prepare_yolo_dataset

if __name__ == "__main__":
    prepare_yolo_dataset(
        base_folder="path/to/yolo_dataset",         # Replace with your YOLO dataset base folder
        source_images_folder="path/to/images",      # Replace with the folder containing your images
        train_percentage=80                         # Percentage of data to assign to the training set
    )
    print("YOLO dataset preparation completed!")

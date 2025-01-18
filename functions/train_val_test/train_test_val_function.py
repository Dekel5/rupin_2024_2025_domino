import os
import random


def split_images_into_groups(source_folder, train_ratio=0.5, val_ratio=0.5):
    """
    Splits image files from a source folder into training and validation groups.

    Parameters:
    source_folder (str): The path to the folder containing the image files.
    train_ratio (float): The proportion of images to allocate to the training set. Default is 0.5.
    val_ratio (float): The proportion of images to allocate to the validation set. Default is 0.5.

    Returns:
    dict: A dictionary containing the split files as lists:
          {'train': train_files, 'val': val_files}
    """
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"The source folder does not exist: {source_folder}")

    # Filter for image files
    image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.heic'))]

    if not image_files:
        raise ValueError(f"No images found in the source folder: {source_folder}")

    # Shuffle images randomly
    random.shuffle(image_files)

    # Calculate sizes for each group
    total_files = len(image_files)
    train_size = int(train_ratio * total_files)
    val_size = int(val_ratio * total_files)

    # Ensure no overlap between groups
    if train_size + val_size > total_files:
        raise ValueError("The sum of train_ratio and val_ratio exceeds 1.0.")

    # Split images into groups
    train_files = image_files[:train_size]
    val_files = image_files[train_size:train_size + val_size]

    return {
        'train': train_files,
        'val': val_files
    }

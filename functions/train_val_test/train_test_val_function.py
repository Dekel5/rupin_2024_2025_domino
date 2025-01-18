import os
import random

def split_images_into_groups(source_folder, train_ratio=0.5, val_ratio=0.5, random_seed=None):
    """
    Splits unique image files from a source folder into training and validation groups (in memory).

    Parameters:
    source_folder (str): The path to the folder containing the image files.
    train_ratio (float): The proportion of images to allocate to the training set. Default is 0.5.
    val_ratio (float): The proportion of images to allocate to the validation set. Default is 0.5.
    random_seed (int, optional): A seed for the random number generator to ensure reproducibility.

    Returns:
    dict: A dictionary containing the split files as lists:
          {'train': train_files, 'val': val_files}
    """
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"The source folder does not exist: {source_folder}")

    # Filter for unique image files (based on base names)
    image_files = {}
    for f in os.listdir(source_folder):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.heic')):
            base_name = os.path.splitext(f)[0]
            if base_name not in image_files:
                image_files[base_name] = f

    if not image_files:
        raise ValueError(f"No images found in the source folder: {source_folder}")

    # Get unique file list
    unique_files = list(image_files.values())

    # Ensure reproducibility if a random seed is provided
    if random_seed is not None:
        random.seed(random_seed)

    # Shuffle images randomly
    random.shuffle(unique_files)

    # Calculate sizes for each group
    total_files = len(unique_files)
    train_size = int(train_ratio * total_files)
    val_size = total_files - train_size  # Remaining files go to validation set

    # Split images into groups
    train_files = unique_files[:train_size]
    val_files = unique_files[train_size:train_size + val_size]

    return {
        'train': train_files,
        'val': val_files
    }

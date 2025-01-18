import os
import pandas as pd
import random

def balanced_split_with_fixed_count(source_folder, excel_file, feature_column, image_column, total_images, total_points, tolerance=10, random_seed=None):
    """
    Splits image files into training and validation sets with fixed count and balanced point totals.

    Parameters:
    source_folder (str): Path to the folder containing the image files.
    excel_file (str): Path to the Excel file containing image names and their associated feature.
    feature_column (str): Name of the column representing the feature (e.g., "view angle").
    image_column (str): Name of the column containing the image names.
    total_images (int): Total number of images to split (must be divisible by 2).
    total_points (int): Total points for all images.
    tolerance (int): Maximum allowed difference in points between train and validation sets.
    random_seed (int, optional): Seed for random shuffling.

    Returns:
    dict: A dictionary with the train and validation splits:
          {'train': train_files, 'val': val_files, 'train_points': train_points, 'val_points': val_points}
    """
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"The source folder does not exist: {source_folder}")
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"The Excel file does not exist: {excel_file}")

    # Load the Excel file
    data = pd.read_excel(excel_file)

    # Validate columns
    if feature_column not in data.columns or image_column not in data.columns:
        raise ValueError(f"The specified columns '{feature_column}' or '{image_column}' do not exist in the Excel file.")

    # Map image names to their feature values
    feature_map = data.set_index(image_column)[feature_column].to_dict()

    # Collect all images and shuffle them
    images = [
        (image_name, feature_map[os.path.splitext(image_name)[0]])
        for image_name in os.listdir(source_folder)
        if os.path.splitext(image_name)[0] in feature_map
    ]

    # Validate the total number of images
    if len(images) != total_images:
        raise ValueError(f"The source folder contains {len(images)} images, but {total_images} were expected.")

    # Retry logic for balanced split
    attempt = 0
    while True:
        attempt += 1
        if random_seed is not None:
            random.seed(random_seed + attempt)  # Modify seed for new shuffle
        random.shuffle(images)

        # Initialize groups
        train_files, val_files = [], []
        train_points, val_points = 0, 0
        target_points = total_points // 2
        target_images = total_images // 2

        # Distribute images
        for image_name, points in images:
            if len(train_files) < target_images and abs((train_points + points) - val_points) <= tolerance:
                train_files.append(image_name)
                train_points += points
            elif len(val_files) < target_images:
                val_files.append(image_name)
                val_points += points

        # Check if the split is balanced
        if len(train_files) == target_images and len(val_files) == target_images and abs(train_points - val_points) <= tolerance:
            print(f"Split successful after {attempt} attempts.")
            break

    return {
        'train': train_files,
        'val': val_files,
        'train_points': train_points,
        'val_points': val_points
    }

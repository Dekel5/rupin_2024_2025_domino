import os


def count_image_files_in_folder(folder_path):
    """
    Counts the number of image files (PNG, JPG, JPEG) in the given folder.

    Parameters:
    folder_path (str): The path to the folder containing the image files.

    Returns:
    int: The number of image files in the folder.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder does not exist: {folder_path}")

    # Filter for image files with specific extensions
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return len(image_files)

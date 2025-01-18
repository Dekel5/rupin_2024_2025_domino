import os
from PIL import Image
import pillow_heif

# Register HEIF format with PIL
pillow_heif.register_heif_opener()

def count_image_files_in_folder(folder_path, convert_heic=False):
    """
    Counts the number of unique image files (PNG, JPG, JPEG, HEIC) in the given folder.
    Optionally converts HEIC files to JPEG.

    Parameters:
    folder_path (str): The path to the folder containing the image files.
    convert_heic (bool): If True, converts HEIC files to JPEG and includes them in the count.

    Returns:
    int: The number of unique image files in the folder.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder does not exist: {folder_path}")

    # Supported image file extensions
    supported_extensions = ('.png', '.jpg', '.jpeg', '.heic')

    # Initialize a set to store unique file base names
    unique_files = set()

    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if the file has a supported extension
        if file_name.lower().endswith(supported_extensions):
            base_name = os.path.splitext(file_name)[0]  # Get base name without extension
            unique_files.add(base_name)

            # If HEIC and conversion is enabled, convert to JPEG
            if convert_heic and file_name.lower().endswith('.heic'):
                jpeg_path = os.path.join(folder_path, base_name + '.jpeg')
                if not os.path.exists(jpeg_path):  # Avoid duplicate conversion
                    try:
                        image = Image.open(file_path)
                        image.save(jpeg_path, "JPEG")
                    except Exception as e:
                        print(f"Failed to convert {file_name}: {e}")

    return len(unique_files)

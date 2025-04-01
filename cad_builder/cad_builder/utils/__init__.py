import os
import glob


def find_project_root(current_dir):
    """Searches recursively upwards until it finds the marker file and returns this path."""

    if glob.glob(os.path.join(current_dir, ".env*")):
        # Marker found, this is the root directory
        return current_dir
    else:
        # Go up one folder and search again
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # Root of the file system reached without finding the marker file
            raise FileNotFoundError("Could not find the marker file.")
        return find_project_root(parent_dir)
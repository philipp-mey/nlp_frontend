import logging
import os
import shutil
from typing import List
from uuid import uuid4

logger: logging.Logger = logging.getLogger(__name__)


def remove_file(file_path: str) -> None:
    """Remove a file if it exists.

    Args:
        file_path (str): The path to the file to remove.

    Raises:
        OSError: If the file could not be removed and it exists.
    """
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            logger.info("Removed file: %s", file_path)
        except OSError as e:
            logger.error(
                "Failed to remove file %s: %s", file_path, e, exc_info=True
            )
            raise
    else:
        logger.warning("File not found, so not removed: %s", file_path)


def move_files_to_uuid_folder(
    files: List[str],
    destination_root: str,
) -> str:
    """Move specified files to a new UUID folder in the destination root.

    Args:
        files (List[str]): List of file paths to move.
        destination_root (str): Root directory for destination.

    Returns:
        str: Path to the created UUID folder.
    """
    folder_uuid = str(uuid4())
    target_dir = os.path.join(destination_root, folder_uuid)
    os.makedirs(target_dir, exist_ok=True)
    for src_path in files:
        if not os.path.isfile(src_path):
            logger.warning("File not found (not moved): %s", src_path)
            continue
        file_name = os.path.basename(src_path)
        dst_path = os.path.join(target_dir, file_name)
        shutil.move(src_path, dst_path)
        logger.info("Moved %s to %s", src_path, dst_path)
    return target_dir

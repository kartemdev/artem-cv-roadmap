from pathlib import Path
from typing import TypedDict

import pandas as pd
from PIL import Image, UnidentifiedImageError

from cv_lab.config import IMAGE_EXTENSIONS


class ImageData(TypedDict):
    file_name: str
    width: int | None
    height: int | None
    mode: str | None
    format: str | None
    is_valid: bool
    error: str | None


def collect_image_paths(
    root: Path, extensions: set[str] = IMAGE_EXTENSIONS
) -> list[Path]:
    image_paths: list[Path] = []

    for ext in extensions:
        image_paths.extend(root.rglob(f"*{ext}"))

    return image_paths


def inspect_image(path: Path) -> ImageData:
    try:
        with Image.open(path) as image:
            image.verify()

            return {
                "file_name": path.stem,
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "format": image.format,
                "is_valid": True,
                "error": None,
            }
    except UnidentifiedImageError:
        return {
            "file_name": path.stem,
            "width": None,
            "height": None,
            "mode": None,
            "format": None,
            "is_valid": False,
            "error": "UnidentifiedImageError",
        }


def save_csv_report(rows: list[ImageData], output_path: Path) -> None:
    if not rows:
        return

    data_frame = pd.DataFrame(rows)

    data_frame.to_csv(output_path, index=False)

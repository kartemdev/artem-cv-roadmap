import csv
from pathlib import Path

from PIL import Image

from cv_lab.io import collect_image_paths, inspect_image, save_csv_report


def test_collect_image_paths_finds_only_images(tmp_path: Path) -> None:
    (tmp_path / "nested").mkdir()
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "nested" / "diagram.png").touch()
    (tmp_path / "notes.txt").touch()

    paths = collect_image_paths(tmp_path)

    assert {path.relative_to(tmp_path) for path in paths} == {
        Path("photo.jpg"),
        Path("nested/diagram.png"),
    }


def test_inspect_image_marks_valid_image_as_valid(tmp_path: Path) -> None:
    image_path = tmp_path / "valid.png"
    Image.new("RGB", (10, 20), color="red").save(image_path)

    result = inspect_image(image_path)

    assert result["is_valid"] is True
    assert result["width"] == 10
    assert result["height"] == 20
    assert result["error"] is None


def test_inspect_image_handles_broken_file(tmp_path: Path) -> None:
    broken_image_path = tmp_path / "broken.jpg"
    broken_image_path.write_bytes(b"this is not an image")

    result = inspect_image(broken_image_path)

    assert result["is_valid"] is False
    assert result["error"] == "UnidentifiedImageError"


def test_save_csv_report_writes_to_requested_path(tmp_path: Path) -> None:
    image_path = tmp_path / "valid.png"
    Image.new("RGB", (10, 20), color="red").save(image_path)
    output_path = tmp_path / "report.csv"

    save_csv_report([inspect_image(image_path)], output_path)

    assert output_path.is_file()
    with output_path.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 1
    assert rows[0]["file_name"] == "valid"
    assert rows[0]["is_valid"] == "True"

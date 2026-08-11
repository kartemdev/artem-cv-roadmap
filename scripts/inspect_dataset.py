import argparse

from cv_lab.config import PROJECT_ROOT
from cv_lab.io import ImageData, collect_image_paths, inspect_image, save_csv_report

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i", "--input", required=True, help="raw data path for input inspect", type=str
)
parser.add_argument(
    "-o", "--output", required=True, help="path for output inspected data", type=str
)

args = parser.parse_args()

image_paths = collect_image_paths(PROJECT_ROOT / args.input)

inspected_data: list[ImageData] = list()

for path in image_paths:
    inspected_data.append(inspect_image(path))

save_csv_report(inspected_data, PROJECT_ROOT / args.output)

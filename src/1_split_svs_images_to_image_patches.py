# Fork from https://github.com/BMIRDS/deepslide

import os
import sys
from os import listdir
from os.path import isfile, join
from PIL import Image
import openslide
from utils import path_utils, enums, svs_utils, image_patch_file_name_builder
import argparse

compression_factor = 1
Image.MAX_IMAGE_PIXELS = 1e10


def get_start_positions(width, height, window_size, axis, overlapping_percentage):
    start_positions = []

    start_position = 0
    start_positions.append(start_position)

    dimension = width if axis == enums.Axis.X else height

    while not (start_position + (window_size * (1 - overlapping_percentage))) > dimension:
        start_position = start_position + (window_size * (1 - overlapping_percentage))
        start_positions.append(int(start_position))

    return start_positions


def output_jpeg_tiles(full_image_path,
                      full_output_path,
                      resolution_level,
                      overlapping_percentage,
                      window_size):  # converts svs image with meta data into just the jpeg image

    img = openslide.OpenSlide(full_image_path)
    width, height = img.level_dimensions[resolution_level]

    x_start_positions = get_start_positions(width, height, window_size, enums.Axis.X, overlapping_percentage)
    y_start_positions = get_start_positions(width, height, window_size, enums.Axis.Y, overlapping_percentage)

    total_number_of_patches = len(x_start_positions) * len(y_start_positions)
    tile_number = 1

    for x_index, x_start_position in enumerate(x_start_positions):
        for y_index, y_start_position in enumerate(y_start_positions):

            x_end_position = min(width, x_start_position + window_size)
            y_end_position = min(height, y_start_position + window_size)
            patch_width = x_end_position - x_start_position
            patch_height = y_end_position - y_start_position

            is_image_patch_size_equal_to_window_size = ((patch_height == window_size) and (patch_width == window_size))
            if not is_image_patch_size_equal_to_window_size:
                continue

            SVS_level_ratio = int(
                svs_utils.get_SVS_level_ratio(img, enums.ResolutionLevel.LEVEL_0_BASE, resolution_level))
            patch = img.read_region((x_start_position * SVS_level_ratio, y_start_position * SVS_level_ratio),
                                    resolution_level,
                                    (patch_width, patch_height))
            patch.load()
            patch_rgb = Image.new("RGB", patch.size, (255, 255, 255))
            patch_rgb.paste(patch, mask=patch.split()[3])

            print("\n")
            print("Patch data", x_start_position, y_start_position, resolution_level, patch_width, patch_height)
            print("Tile size for tile number " + str(tile_number) + ":" + str(patch.size))

            # compress the image
            # patch_rgb = patch_rgb.resize(
            #    (int(patch_rgb.size[0] / compression_factor), int(patch_rgb.size[1] / compression_factor)),
            #    Image.ANTIALIAS)

            # save the image

            case_id = full_image_path.split('/')[-1][:-4]

            output_subfolder = join(full_output_path, case_id)
            path_utils.create_directory_if_directory_does_not_exist_at_path(output_subfolder)

            output_image_name = join(output_subfolder,
                                     image_patch_file_name_builder.build_image_patch_file_name(
                                         case_id, resolution_level, x_start_position,
                                         y_start_position, patch_width, patch_height))

            patch_rgb.save(output_image_name)
            print("Tile", tile_number, "/", total_number_of_patches, "created")
            tile_number = tile_number + 1


parser = argparse.ArgumentParser(
    description='Split a WSI at a specific resolution in a .SVS file into .JPEG tiles.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.",
                    required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)

parser.add_argument("-s", "--start_at_image_name", type=str, default=None, help="Resume from a certain filename."
                                                                                " Default value is None.")
parser.add_argument("-r", "--resolution_level", type=int, default=0, choices=[0, 1, 2, 3],

                    help="Resolution level for image to be split."
                         " Low level equals high resolution, lowest level is 0. Choose between {0, 1, 2, 3}."
                         " Default value is 0.")

parser.add_argument("-op", "--overlap_percentage", type=int, default=0,
                    help="Overlapping percentage between patches."
                         " Default value is 0.")
parser.add_argument("-ws", "--window_size", type=int, default=10000,
                    help="Size for square window"
                         " Default value is 10000.")

args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path
start_at_image_name = args.start_at_image_name
resolution_level = args.resolution_level
overlapping_percentage = float("{0:.2f}".format(args.overlap_percentage / 100))
window_size = args.window_size

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

full_tcga_download_directories_paths = path_utils.create_full_paths_to_directories_in_directory_path(input_folder_path)
for full_tcga_download_directories_path in full_tcga_download_directories_paths:
    full_image_name_paths = path_utils.create_full_paths_to_files_in_directory_path(full_tcga_download_directories_path)
    for full_image_name_path in full_image_name_paths:
        output_path = output_folder_path + '/'
    output_jpeg_tiles(full_image_name_path, output_path, resolution_level, overlapping_percentage, window_size)

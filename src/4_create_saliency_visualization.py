import argparse
import os
from os.path import isfile, join
from PIL import Image
import openslide
from utils import path_utils
from utils import enums
from utils import svs_utils


def create_jpeg_thumbnail_of_wsi(full_image_path,
                                 full_output_path):
    resolution_level = enums.ResolutionLevel.LEVEL_3
    img = openslide.OpenSlide(full_image_path)
    thumbnail = img.associated_images["thumbnail"]

    output_subfolder = join(full_output_path, full_image_path.split('/')[-1][:-4])
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)
    output_image_name = join(output_subfolder,
                             full_image_path.split('/')[-1][:-4] + '.png')
    print(output_image_name)
    thumbnail.save(output_image_name)


parser = argparse.ArgumentParser(description='Saliency visualization.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)
args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)
full_image_name_paths = path_utils.create_full_paths_to_files_in_directory_path(input_folder_path)

for full_image_name_path in full_image_name_paths:
    output_path = output_folder_path + '/'
    create_jpeg_thumbnail_of_wsi(full_image_name_path, output_path)

import argparse
import os
from os.path import isfile, join
from PIL import Image, ImageDraw
import openslide
from utils import path_utils
from utils import enums
from utils import svs_utils, image_patch_predictions_constants, image_patch_file_name_constants
import csv


def create_jpeg_thumbnail_of_wsi(full_image_name_path,
                                 image_name,
                                 full_output_path):
    img = openslide.OpenSlide(full_image_name_path)
    print (img.level_dimensions)
    thumbnail = img.associated_images["thumbnail"]
    print (thumbnail.size)

    output_subfolder = join(full_output_path, image_name)
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)
    output_image_name = join(output_subfolder,
                             image_name + '.png')
    thumbnail.save(output_image_name)
    return thumbnail


def draw_prediction_annotations_onto_thumbnail(thumbnail, full_cvs_path):
    TINT_COLOR = (0, 255, 0)  # Black
    TRANSPARENCY = .20  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)


    with open(full_cvs_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            saliency_prediction = float(row[image_patch_predictions_constants.PREDICTION_VALUE_SALIENT])

            if saliency_prediction > 0.95:
                resolution_level = svs_utils.get_SVS_level_ratio(
                    int(row[image_patch_file_name_constants.RESOLUTION_LEVEL]))

                x_coordinate = scale(int(row[image_patch_file_name_constants.X_COORDINATE]), resolution_level,
                                     enums.SVSLevelRatio.THUMBNAIL)
                y_coordinate = scale(int(row[image_patch_file_name_constants.Y_COORDINATE]), resolution_level,
                                     enums.SVSLevelRatio.THUMBNAIL)

                width = scale(int(row[image_patch_file_name_constants.WIDTH]), resolution_level,
                              enums.SVSLevelRatio.THUMBNAIL)
                height = scale(int(row[image_patch_file_name_constants.HEIGHT]), resolution_level,
                               enums.SVSLevelRatio.THUMBNAIL)

                # print(x_coordinate)
                # print(y_coordinate)
                # print(width)
                # print(height)


                overlay = Image.new('RGBA', thumbnail.size, TINT_COLOR + (0,))
                draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
                draw.rectangle(((x_coordinate, y_coordinate), (x_coordinate+width, y_coordinate+height)),
                               fill=TINT_COLOR + (OPACITY,))


                thumbnail = Image.alpha_composite(thumbnail, overlay)

    thumbnail = thumbnail.convert("RGB")
    thumbnail.save('dark-cat.jpeg')


def scale(value, from_resolution_level_ratio, to_resolution_level_ratio):
    # print (value, from_resolution_level_ratio, to_resolution_level_ratio)
    return (value/4.5)


parser = argparse.ArgumentParser(description='Saliency visualization.')
parser.add_argument("-svs", "--svs_input_folder_path", type=str, help="The path to the SVS input folder.",
                    required=True)
parser.add_argument("-csv", "--csv_input_folder_path", type=str, help="The path to the CSV input folder.",
                    required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)

args = parser.parse_args()

svs_input_folder_path = args.svs_input_folder_path
csv_input_folder_path = args.csv_input_folder_path
output_folder_path = args.output_folder_path

path_utils.halt_script_if_path_does_not_exist(svs_input_folder_path)
path_utils.halt_script_if_path_does_not_exist(csv_input_folder_path)

path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

full_image_name_paths = path_utils.create_full_paths_to_files_in_directory_path(svs_input_folder_path)
full_image_patch_data_dict_paths = path_utils.create_full_paths_to_files_in_directory_path(csv_input_folder_path)

for full_image_name_path_index, full_image_name_path in enumerate(full_image_name_paths):
    output_path = output_folder_path + '/'
    image_name = full_image_name_path.split('/')[-1][:-4]
    thumbnail = create_jpeg_thumbnail_of_wsi(full_image_name_path, image_name, output_path)
    draw_prediction_annotations_onto_thumbnail(thumbnail, full_image_patch_data_dict_paths[full_image_name_path_index])

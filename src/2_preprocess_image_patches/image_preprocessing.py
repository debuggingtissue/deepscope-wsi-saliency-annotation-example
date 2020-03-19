from PIL import Image
import argparse


class ImagePreprocessing:

    def preprocess_image(self, input_image_path):
        input_image = Image.open(input_image_path)
        first_centermost_crop_image = self.crop_to_the_centermost(input_image, FIRST_CENTERMOST_CROP_SIZE)
        scaled_image = self.scale_image(first_centermost_crop_image, DOWNSCALED_SIZE)
        second_centermost_crop_image = self.crop_to_the_centermost(scaled_image, SECOND_CENTERMOST_CROP_SIZE)

        return second_centermost_crop_image


    def crop_to_the_centermost(self, image, new_size):
        print(image)
        width, height = image.size  # Get dimensions

        left = (width - new_size) / 2
        top = (height - new_size) / 2
        right = (width + new_size) / 2
        bottom = (height + new_size) / 2

        # Crop the center of the image
        cropped_image = image.crop((left, top, right, bottom))
        return cropped_image

    def scale_image(self, image, new_size):

        maxsize = (new_size, new_size)
        image.thumbnail(maxsize, Image.ANTIALIAS)
        return image


parser = argparse.ArgumentParser(description='Split a WSI at a specific resolution in a .SVS file into .JPEG tiles.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
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




2_preprocess_image_patches/image_preprocessing.py -i S2_PREPROCESS_IMAGE_PATCHES_INPUT_DIRECTORY_PATH \
  -o S2_PREPROCESS_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH \
  -is S2_IMAGE_PATCH_INPUT_SIZE \
  -fc S2_FIRST_CENTERMOST_CROP_SIZE \
  -ds S2_DOWNSCALED_SIZE \
  -sc S2_SECOND_CENTERMOST_CROP_SIZE
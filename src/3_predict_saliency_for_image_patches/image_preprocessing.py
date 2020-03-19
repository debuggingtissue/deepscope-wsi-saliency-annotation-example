from PIL import Image

INPUT_SIZE = 800
FIRST_CENTERMOST_CROP_SIZE = 512
DOWNSCALED_SIZE = 256
SECOND_CENTERMOST_CROP_SIZE = 227


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

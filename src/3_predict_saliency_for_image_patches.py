import caffe
import argparse

from utils import path_utils


net = caffe.Classifier("cnn_model/deploy.prototxt",
                       "cnn_model/PRAD.patho_tune_joe-overlap75-nbr.rightleft.trim512.rot360flip.shuffle.3fold.trial9_patho_tune_trial9_fold1_iter_10000.caffemodel",
                       image_dims=(227, 227),
                       raw_scale=255)


parser = argparse.ArgumentParser(description='DeepScope classifier.')
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



# if __name__ == '__main__':

# IMAGE_FILE_CANCER = 'test_images/cancer.jpg'
# IMAGE_FILE_WHITE_DUMMY = 'test_images/white_dummy.jpg'
# IMAGE_FILE_NORMAL = 'test_images/normal.jpg'
# IMAGE_FILE_PURPLE_DUMMY = 'test_images/purple_dummy.jpeg'
#
# image_processor = ImagePreprocessing()
#
# input_image_cancer = caffe.io.load_image(image_processor.preprocess_image(IMAGE_FILE_CANCER))
# input_image_white = caffe.io.load_image(IMAGE_FILE_WHITE_DUMMY)
# input_image_normal = caffe.io.load_image(IMAGE_FILE_NORMAL)
# input_image_lilla = caffe.io.load_image(IMAGE_FILE_PURPLE_DUMMY)
#
# pred = net.predict([input_image_cancer])
# print(pred)

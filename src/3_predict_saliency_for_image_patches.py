import caffe
import argparse
import numpy as np

from utils import path_utils


def load_images_patches_to_caffe(full_image_patches_paths):
    loaded_image_patches = []
    for full_image_patch_path in full_image_patches_paths:
        loaded_image_patch = caffe.io.load_image(full_image_patch_path)
        loaded_image_patches.append(loaded_image_patch)
    return loaded_image_patches


def predict_saliency_for_loaded_image_patches(loaded_image_patches):
    net = caffe.Classifier("cnn_model/deploy.prototxt",
                           "cnn_model/PRAD.patho_tune_joe-overlap75-nbr.rightleft.trim512.rot360flip.shuffle.3fold.trial9_patho_tune_trial9_fold1_iter_10000.caffemodel",
                           image_dims=(227, 227),
                           raw_scale=255)

    predictions = net.predict(loaded_image_patches)
    return predictions


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

full_case_paths = path_utils.create_full_paths_to_directories_in_directory_path(input_folder_path)

case_predictions = []
for full_case_path in full_case_paths:
    full_image_patches_paths = path_utils.create_full_paths_to_files_in_directory_path(full_case_path)
    loaded_image_patches = load_images_patches_to_caffe(full_image_patches_paths)
    predictions_for_image_patches = predict_saliency_for_loaded_image_patches(loaded_image_patches)
    case_predictions.append(predictions_for_image_patches)

ids = []
id = 0
for case_prediction in case_predictions[0]:
    ids.append(id)
    id = id + 1

print(ids)
print(np.asarray(ids))

id_array = np.asarray(ids)
id_column = id_array.reshape((-1, 1))

print (case_predictions)
print (id_column)

np.set_printoptions(formatter={'all':lambda x: str(x)})

case_predictions = np.hstack((case_predictions[0], id_column))
print case_predictions

#
# case_predictions_with_id = []
#

# print(case_predictions_with_id)

# cases
# image_patches

# one prediction file for each case


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

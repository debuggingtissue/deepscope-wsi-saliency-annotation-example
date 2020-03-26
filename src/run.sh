#!/bin/bash

###################################
#             INPUTS              #
###################################

S0_VIRTUAL_ENV_27=${1?Error: no virtual environment directory path given}
S0_VIRTUAL_ENV_36=${2?Error: no virtual environment directory path given}
S0_INPUT_DIRECTORY_PATH=${3?Error: no input directory path given}
S0_OUTPUT_DIRECTORY_PATH=${4?Error: no output directory path given}

###################################
#             CONFIG              #
###################################

# 1_split_svs_images_to_image_patches
#####################################
S1_SPLIT_SVS_S0_INPUT_DIRECTORY_PATH=${S0_INPUT_DIRECTORY_PATH}
S1_SPLIT_SVS_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/1_split_svs_images_to_image_patches"
S1_RESOLUTION_LEVEL=2
S1_OVERLAP_PERCENTAGE=50
S1_WINDOW_SIZE=800

# 2_preprocess_image_patches
#####################################
S2_PREPROCESS_IMAGE_PATCHES_INPUT_DIRECTORY_PATH=${S1_SPLIT_SVS_OUTPUT_DIRECTORY_PATH}
S2_PREPROCESS_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/2_preprocess_image_patches"
S2_FIRST_CENTERMOST_CROP_SIZE=512
S2_DOWNSCALED_SIZE=256
S2_SECOND_CENTERMOST_CROP_SIZE=227

# 3_predict_saliency_for_image_patches
#####################################
S3_PREDITCT_SALIENCY_INPUT_DIRECTORY_PATH=${S2_PREPROCESS_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH}
S3_PREDITCT_SALIENCY_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/3_predict_saliency_for_image_patches"

# 4_create_saliency_visualization
#####################################
S4_CREATE_SALIENCY_VISUALIZATION_SVS_INPUT_DIRECTORY_PATH=${S0_INPUT_DIRECTORY_PATH}
S4_CREATE_SALIENCY_VISUALIZATION_CSV_INPUT_DIRECTORY_PATH=${S3_PREDITCT_SALIENCY_OUTPUT_DIRECTORY_PATH}
S4_CREATE_SALIENCY_VISUALIZATION_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/4_create_saliency_visualization"

###################################
#               RUN               #
###################################

source "${S0_VIRTUAL_ENV_36}/bin/activate"
python3.6 1_split_svs_images_to_image_patches.py \
  -i $S1_SPLIT_SVS_S0_INPUT_DIRECTORY_PATH \
  -o $S1_SPLIT_SVS_OUTPUT_DIRECTORY_PATH \
  -r $S1_RESOLUTION_LEVEL \
  -op $S1_OVERLAP_PERCENTAGE \
  -ws $S1_WINDOW_SIZE
#
python3.6 2_preprocess_image_patches.py \
  -i $S2_PREPROCESS_IMAGE_PATCHES_INPUT_DIRECTORY_PATH \
  -o $S2_PREPROCESS_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH \
  -fc $S2_FIRST_CENTERMOST_CROP_SIZE \
  -ds $S2_DOWNSCALED_SIZE \
  -sc $S2_SECOND_CENTERMOST_CROP_SIZE

source "${S0_VIRTUAL_ENV_27}/bin/activate"
python 3_predict_saliency_for_image_patches.py \
  -i $S3_PREDITCT_SALIENCY_INPUT_DIRECTORY_PATH \
  -o $S3_PREDITCT_SALIENCY_OUTPUT_DIRECTORY_PATH

source "${S0_VIRTUAL_ENV_36}/bin/activate"
python3.6 4_create_saliency_visualization.py \
  -svs $S4_CREATE_SALIENCY_VISUALIZATION_SVS_INPUT_DIRECTORY_PATH \
  -csv $S4_CREATE_SALIENCY_VISUALIZATION_CSV_INPUT_DIRECTORY_PATH \
  -o $S4_CREATE_SALIENCY_VISUALIZATION_OUTPUT_DIRECTORY_PATH \

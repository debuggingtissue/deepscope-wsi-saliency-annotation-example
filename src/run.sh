#!/bin/bash

VIRTUAL_ENV_27=${1?Error: no virtual environment directory path given}
VIRTUAL_ENV_36=${2?Error: no virtual environment directory path given}
INPUT_DIRECTORY_PATH=${3?Error: no input directory path given}
OUTPUT_DIRECTORY_PATH=${4?Error: no output directory path given}

###################################
#             CONFIG              #
###################################

# 1_split_svs_images_to_image_patches
#####################################
SPLIT_SVS_INPUT_DIRECTORY_PATH=${INPUT_DIRECTORY_PATH}
SPLIT_SVS_OUTPUT_DIRECTORY_PATH="${OUTPUT_DIRECTORY_PATH}/1_split_svs_images_to_image_patches"
RESOLUTION_LEVEL=2
OVERLAP_PERCENTAGE=50
WINDOW_SIZE=800

# 2_preprocess_image_patches
#####################################


###################################
#               RUN               #
###################################

source "${VIRTUAL_ENV_36}/bin/activate"
python3.6 1_split_svs_images_to_image_patches/deepslide-svs-wsi-to-jpeg-patch-generator-master/src/wsi_svs_to_jpeg_tiles.py \
  -i $SPLIT_SVS_INPUT_DIRECTORY_PATH \
  -o $SPLIT_SVS_OUTPUT_DIRECTORY_PATH \
  -r $RESOLUTION_LEVEL \
  -op $OVERLAP_PERCENTAGE \
  -ws $WINDOW_SIZE

#source "${VIRTUAL_ENV_27}/bin/activate"
#python 3_predict_saliency_for_image_patches/deepscope_saliency_classifier.py

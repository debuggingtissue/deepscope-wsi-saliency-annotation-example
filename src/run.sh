#!/bin/bash

VIRTUAL_ENV_27=${1?Error: no virtual environment directory path given}
VIRTUAL_ENV_36=${2?Error: no virtual environment directory path given}
#INPUT_DIRECTORY_PATH=${3?Error: no input directory path given}
#OUTPUT_DIRECTORY_PATH=${4?Error: no output directory path given}

source "${VIRTUAL_ENV_36}/bin/activate"
python3.6 1_split_svs_images_to_image_patches/deepslide-svs-wsi-to-jpeg-patch-generator-master/src/wsi_svs_to_jpeg_tiles.py
source "${VIRTUAL_ENV_27}/bin/activate"
python 3_predict_saliency_for_image_patches/deepscope_saliency_classifier.py

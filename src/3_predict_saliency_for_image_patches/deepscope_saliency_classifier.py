import caffe
from image_preprocessing import ImagePreprocessing

if __name__ == '__main__':
    net = caffe.Classifier("cnn_model/deploy.prototxt",
                           "cnn_model/PRAD.patho_tune_joe-overlap75-nbr.rightleft.trim512.rot360flip.shuffle.3fold.trial9_patho_tune_trial9_fold1_iter_10000.caffemodel",
                           image_dims=(227, 227),
                           raw_scale=255)

    IMAGE_FILE_CANCER = 'test_images/cancer.jpg'
    IMAGE_FILE_WHITE_DUMMY = 'test_images/white_dummy.jpg'
    IMAGE_FILE_NORMAL = 'test_images/normal.jpg'
    IMAGE_FILE_PURPLE_DUMMY = 'test_images/purple_dummy.jpeg'

    image_processor = ImagePreprocessing()

    input_image_cancer = caffe.io.load_image(image_processor.preprocess_image(IMAGE_FILE_CANCER))
    input_image_white = caffe.io.load_image(IMAGE_FILE_WHITE_DUMMY)
    input_image_normal = caffe.io.load_image(IMAGE_FILE_NORMAL)
    input_image_lilla = caffe.io.load_image(IMAGE_FILE_PURPLE_DUMMY)

    pred = net.predict([input_image_cancer])
    print(pred)

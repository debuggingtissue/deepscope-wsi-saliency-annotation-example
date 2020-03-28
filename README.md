# deepscope-wsi-saliency-annotation-example

Tool for finding the image patches that are the most likely to be salient for pathologists using the DeepScope classifier. 

Link to the DeepScope paper: https://europepmc.org/article/med/29601065

## How to run

1. [Install Openslide](https://openslide.org/download/) using your OS package manager (apt, yum, brew etc.)

2. Download the project 

3. Create a virtual environment with a Python 3.6 interpreter

        python3.6 -m venv name-of-virtual-environment

4. Activate the virtual environment

        . ./name-of-python36-virtual-environment/bin/activate
    

5. Navigate to the project directory 
    
        cd my/path/to/deepscope-wsi-saliency-annotation-example

6. Install the dependencies using the `requirements-python36.txt` file

        pip install -r requirements-python36.txt


7. [Install Caffe](https://www.debuggingtissue.com/latest-articles/converting-a-caffe-model-to-a-caffe2-model-using-ubuntu-18044-lts) using a Python 2.7 interpreter

8. Create a virtual environment with a Python 2.7 interpreter

        python2.7 -m venv name-of-python27-virtual-environment

9. Activate the virtual environment

        . ./name-of-python27-virtual-environment/bin/activate
    
10. Navigate to the project directory 
    
        cd my/path/to/deepscope-wsi-saliency-annotation-example

6. Install the dependencies using the `requirements-python27.txt` file

        pip install -r requirements-python27.txt

5. Navigate to the `src` directory

        cd src

6. Run the Python script with desired arguments
    
        source run.sh absolute-path/to/name-of-python27-virtual-environment absolute-path/to/name-of-python36-virtual-environment absolute-path/to/input-folder absolute-path/to/jpeg-tiles-folder
   

# Hdf5_Conv
Batch conversion of YeaZ .hdf5 ouput mask images stored into .tif files.
Hdf5 converter
Description : 
This program was developed to batch convert Yeaz’s output .hdf5 mask files into .tif images, therefore facilitating downstream processing and visualization of segmentation.

Download:
The python scripts and the standalone executable are available at: https://github.com/VZufferey/Hdf5_Conv The standalone is available in the “releases” section on the right of the Github repository and can be used directly in windows.

Installation and running python script:
-	Installation: (assuming Cond is installed, see Yeaz/BatchYeaz guides):
Create python environment and add packages with the following commands (launch Console from the folder containing Hdf5_converter and requirement file, type “cmd” in the address bar)

conda create --name hdf5-conv
conda activate hdf5-conv
pip install -r requirements.txt

-	Run with the following commands: 

conda activate hdf5-conv
python Hdf5_converter.py

How to use:
Select the folder where the program will look for .hdf5 files to convert
Select the output format: Sequence or in single frames 
Click OK

# ORPER
ORPER summer school 2023

------------------------------------------------------
-- General information:
------------------------------------------------------

	- Author: Samuel Vorlet

	- Date of creation: 14.09.2023

	- Python version: 3.10.4

------------------------------------------------------
-- Description: 
------------------------------------------------------
This repository contains the implementation of python code to perform basic statistical analysis of turbulence.

The dataset comes from "C. Renner, J. Peinke, and R. Friedrich, “Experimental indications for Markov
properties of small–scale turbulence,” J. Fluid Mech. 433, 383 (2001)" and can be found on the following github repository: 
https://github.com/andre-fuchs-uni-oldenburg/OPEN_FPE_IFT/tree/master/sample_data

The script was created using jupyter notebook as markdown (.ipynb). However, the script was exported as executable script (.py) for simplicity.

------------------------------------------------------
-- Folders/files description:
------------------------------------------------------
On the root:

	- code: folder that contains all executable files (.py). It also contains the dataset to be used (Renner.mat) 

	- .gitignore: file that contains the list of files/folders to be ignored (empty at the moment)

	- LICENSE: github license related file

------------------------------------------------------
-- Instructions for compilation of the script
------------------------------------------------------

The file is a direct executable script. The user needs to open it and run it, and the script will perform basic statistical analysis of turbulent flow from a time-series.

The code contains 3 parts:

	- Data importation -> import the time-series

	- Stationarity -> performing basic stationarity tests

	- Probability Density Function -> calculate and plot the PDF of the data, check if it has a gaussian behavior

Depending on the computational power, the full script can take up to 90 seconds to compile and run fully.
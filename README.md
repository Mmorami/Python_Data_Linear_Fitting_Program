# Python Linear Fitting Program

A linear fitting program written in python.<br>
The program gets expirement data points in a text file orgenized in a certain format as an input (examples can be found in the Examples directory), and makes a linear fit by minimizing chi^2.<br>
The program outputs the fitting parameters along with their errors, the ideal chi^2 and chi^2 reduced, and finally plots the fit.<br>
The bonus function enables numerical search of the minimal chi^2 within predefined limits of the parameters and a desired step size.

[add image here]

## Installation

To run the program create an input .txt file according to format and run the main.py file.
Note that the program was wrote using python 3.6.

## Usage

Please check the example .txt file to see the allowed input formats.<br>
To execute a numerical search add the searching range and the step size of each parameter according to the following pattern: start end step.
Please check the example .txt file to see the exact format.`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Any improvement should be saved as a new version, with documentation on changes and improvements from previous version.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

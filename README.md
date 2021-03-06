## Introduction
This repository is a simple graphical user interface (GUI) that unlocks protected pdf files. With this tool it is possible to unlock multiple pdf's at once.
The tool may be run via the .py file or via de executable.
The tool has the following options:
- unlock pdf files in a folder
- unlock pdf files in a zipped folder

This last option unzips de folder and checks if the file name needs to be adjusted due to a too long path or the existence of files with the same name.

## Requirements
The executable ('PDF_unlock_tool.exe') installs all the needed dependencies to run the tool.
If the tool is run from the .py file ('PDF_unlock_tool.py') there are extra files needed (also available in this repository):
- file '_functions/unlock_file.py'
- file '_functions/unzip_files.py'
- file '_functions/check_length.py'
- 'logo.ico' (file with a logo)
- package: 
	- [pikepdf](https://github.com/pikepdf/pikepdf) (see file 'requirements/requirements_gui.txt')

## Test files
Test files are also available in this repository and can be downloaded to test the tool:
- 1 normal folder 'test files'
- 1 zip folder 'test files_zip.zip'

## Using the tool
### Run the tool using the python script
- Create a new virtual environment (Python 3.7) and activate the new environment
- Install the dependencies: 'pip install -r requirements_gui.txt'
- Run the file 'PDF_unlock_tool.py' to unlock one or more pdf files (see 'Manual PDF unlock tool.pdf')
- Check if unlocked files can be edited

### Run the tool using the executable
- Download the file 'PDF_unlock_tool.exe'
- Read the instructions manual ('Manual PDF unlock tool.pdf') to learn how to install and run the tool
- Check if unlocked files can be edited

## Error detection
Every time the tool is used, information on what happens in every step of the tool is saved in a file (‘Logging_UnlockTool.txt’), in the same folder als the tool. If errors occur, this file can be used to check which step went wrong.

## Author
Joana Cardoso

## Contact
For questions or suggestions please contact: vdwh@pzh.nl

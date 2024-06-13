
# Python Scripts for File Comparisons

This repo has two different script for comparing files. 

## identify_differences.py 
This will take two files and produces two outputs. The first is a file that the user can choose a name for in the GUI, for example `output_file.csv`
This file will show differences between the files within the cells of the output file so the user can locate differences in the original files if needed.   
A second file will be produced that provides summary data of the differences. The file name of this will prepend `summary` to the user selected file name, ie., `summary_output_file.csv`  
See below for more details about usage. Some information is also available when you are using hte GUI.  


## Roadmap

- Additional browser support

- Add more integrations


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Tech Stack

**Client:** React, Redux, TailwindCSS

**Server:** Node, Express


## Documentation
# Find Unique Data
## Description of `gui_find_unique_data.py` 

The Find Unique Data Tool is a graphical user interface (GUI) application built using Python's Tkinter library. This tool allows users to compare two CSV files and identify unique records in the second file based on specified unique identifier columns. The unique records are then saved to an output CSV file.

## Features

- **File Browsing:** Easily select CSV files using the browse buttons.
- **Customizable Output Path:** Specify the path where the output file will be saved.
- **Informational Popup:** Define one or two columns to use as unique identifiers for the comparison.
- **Clear Inputs for Reuse:** After running the comparison, the tool can clear inputs to allow for additional comparisons.

## Requirements

- Python >= 3.12
- `tkinter library` (usually included with Python, but if you are using a Mac with silicone chip you may need to Brew Install it)
- `pandas` library

## Installation
Ensure you have Python installed on your machine.
   You can download it from [The Python download page](https://www.python.org/downloads/)

1. **Setup Virtual Environment (Optional but Recommended):**
   - Create a new directory for your project and navigate into it:

     ```sh
     mkdir find_unique_data_tool
     cd find_unique_data_tool
     ```

   - Create a virtual environment inside this directory:

     ```sh
     python -m venv venv
     ```

   - Activate the virtual environment. The command to activate the virtual environment depends on your operating system:

     On Windows:

     ```sh
     venv\Scripts\activate
     ```

     On macOS and Linux:

     ```sh
     source venv/bin/activate
     ```

2. **Install Required Libraries:**
   - Install Python libraries required by the tool using pip. Ensure you are in the virtual environment before running this command:

     ```sh
     pip install pandas tkinter
     ```

3. **Run the Application:**
   - Launch the application by running the script using Python:

     ```sh
     python find_unique_data_tool.py
     ```

   Follow the instructions in the application to select CSV files, specify unique identifier columns, and run comparisons.

4. **Deactivate the Virtual Environment (Optional):**
   - Once you're done using the tool, you can deactivate the virtual environment:

     ```sh
     deactivate
     ```

     This step is optional but recommended to isolate dependencies for different projects.


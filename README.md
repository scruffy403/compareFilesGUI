
# Python Scripts for File Comparisons

## Scripts
- **`gui_find_unique_data.py`**:
    A script to compate two files, assuming the second file has additonal date, and produce a new file with the rows of data unique to the second file. 
    *This tool has its own GUI*

- **`identify_differences.py`**:
    Compares two files and produces two output files. The first file (the user selects the name) shows differences in each cell of the file if differences are found in a cell of the input files.  
    The second file is a summary file (`summary` is prepended to the user output file name) that provides a summary of today differences per column name and some other details.  
    *This tool has its own GUI*

- **`find_unique_data.py`**:
    A command line implemntation similar to `find_unique_data_tool.py`. This was the initial implementation of the `gui_find_unique_data.py` logic and would need to be updated to reflect the changes to the GUI app in order to have the same function as a command line tool.

- **`check_environment.py`**:
    This tool is being developed to check that a suitable version of Python is installed and if so set up a virtual environment and then install the dependencies listed in `requirements.txt`.  
    *This is a command line script*


# Documentation
## Find Unique Data
### Description of `gui_find_unique_data.py` 

The Find Unique Data Tool is a graphical user interface (GUI) application built using Python's Tkinter library. This tool allows users to compare two CSV files and identify unique records in the second file based on specified unique identifier columns. The unique records are then saved to an output CSV file.

## Features

- **File Browsing:** Easily select CSV files using the browse buttons.
- **Customizable Output Path:** Specify the path where the output file will be saved.
- **Informational Popup:** Define one or two columns to use as unique identifiers for the comparison.
- **Clear Inputs for Reuse:** After running the comparison, the tool can clear inputs to allow for additional comparisons.

## GUI Components
- **Main Window:** A Tkinter window with labels, entries, and buttons for user interaction.
- **File Path Entries:** Text entries for the paths of File 1, File 2, and the output file.
- **Unique Identifier Entries:** Text entries for specifying unique identifier columns (Option to enter a second unique identifer column).
- **Run Button:** A button to start the comparison process.
- **Usage Info Button:** A button to display usage instructions.

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


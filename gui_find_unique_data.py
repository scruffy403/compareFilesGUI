import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def browse_files(file_type, label_var):
    """Opens a file dialog and sets the selected path to the label variable"""
    filename = filedialog.askopenfilename(title=f"Select {file_type} file")
    label_var.set(filename)

def run_program():
    """Reads data from files, performs operations, and saves the output"""
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()
    output_path = output_entry.get()
    unique_id1 = unique_id_entry1.get()
    unique_id2 = unique_id_entry2.get()

    # Read CSV files with specific data types
    df1 = pd.read_csv(file1_path, dtype={'sourceAccountSortCode': object, 'sourceAccountAccountNumber': object, 'orderId': object, 'merchantCategoryCode': object})
    df2 = pd.read_csv(file2_path, dtype={'sourceAccountSortCode': object, 'sourceAccountAccountNumber': object, 'orderId': object, 'merchantCategoryCode': object})

    # Convert DataFrames to sets
    df1_set = set(df1[unique_id1])

    def is_unique(row):
        return (row[unique_id1] not in df1_set) and (not unique_id2 or row[unique_id2] not in df1_set)

    if unique_id2:
        df2_set = set(zip(df2[unique_id1], df2[unique_id2]))
        df_not_in_1 = df2[df2.apply(is_unique, axis=1)]
    else:
        df2_unique_set = set(df2[unique_id1]) - df1_set
        df_not_in_1 = df2[df2[unique_id1].isin(df2_unique_set)]

    # Save the unique data to a new CSV file
    df_not_in_1.to_csv(output_path, index=False)

    # Display success message in popup window
    message = f"Unique data saved to {output_path}. Do more files?"
    result = messagebox.askyesno("Prompt", message, icon='question')
    
    print(f"User clicked: {result}")

    if not result:
        window.destroy()
    else:
        # Clear entry fields for new run
        file1_entry.set("")
        file2_entry.set("")
        output_entry.set("")
        unique_id_entry1.set("")
        unique_id_entry2.set("")

def show_info():
    """Displays an informational message box."""
    info_message = (
        "This tool assumes the second file has the unique data\n"
        "It compares two CSV files to find unique data.\n\n"
        "Instructions:\n"
        "1. Select File 1 and File 2 using the Browse buttons.\n"
        "2. Specify the output file path where the results will be saved.\n"
        "   Example usage:  'output_file_name.csv'\n"
        "   By default the output file will be put into the same folder as the script\n"
        "   Unless you enter a sub folder before the out put file name\n"
        "   Example usage:  'sub_folder_name/output_file_name.csv'\n"
        "3. Enter the column name for the unique identifier(s).\n"
        "4. Click 'Run' to start the comparison."
    )
     # Create a custom Toplevel window
    info_window = tk.Toplevel(window)
    info_window.title("Usage Information")
    info_window.geometry("400x350")  # Set custom size for the message box

    # Add the information text to the window
    info_label = tk.Label(info_window, text=info_message, justify=tk.LEFT, wraplength=380)
    info_label.pack(padx=10, pady=10)

    # Add a button to close the window
    close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
    close_button.pack(pady=(0, 10))

# Create the main window
window = tk.Tk()
window.geometry("500x400")
window.title("Find Unique Data Tool")


# Info Button
info_button = tk.Button(window, text="Usage Info", command=show_info)
info_button.pack(pady=(20, 5))

# File 1 path label and entry
file1_label = tk.Label(window, text="File 1 path:")
file1_label.pack()

file1_entry = tk.StringVar()
file1_entry_box = tk.Entry(window, textvariable=file1_entry)
file1_entry_box.pack()

file1_browse_button = tk.Button(window, text="Browse", command=lambda: browse_files("File 1", file1_entry))
file1_browse_button.pack()

# File 2 path label and entry (similar to file 1)
file2_label = tk.Label(window, text="File 2 path:")
file2_label.pack()

file2_entry = tk.StringVar()
file2_entry_box = tk.Entry(window, textvariable=file2_entry)
file2_entry_box.pack()

file2_browse_button = tk.Button(window, text="Browse", command=lambda: browse_files("File 2", file2_entry))
file2_browse_button.pack()

# Output path label and entry (similar to file 1)
output_label = tk.Label(window, text="Output file path:")
output_label.pack()

output_entry = tk.StringVar()
output_entry_box = tk.Entry(window, textvariable=output_entry)
output_entry_box.pack()

# Unique identifier label and entry (for first identifier)
unique_id_label1 = tk.Label(window, text="Unique identifier column 1:")
unique_id_label1.pack()

unique_id_entry1 = tk.StringVar()
unique_id_entry_box1 = tk.Entry(window, textvariable=unique_id_entry1)
unique_id_entry_box1.pack()

# New label and entry for second unique identifier (optional)
unique_id_label2 = tk.Label(window, text="Unique identifier column 2 (optional):")
unique_id_label2.pack()

unique_id_entry2 = tk.StringVar()
unique_id_entry_box2 = tk.Entry(window, textvariable=unique_id_entry2)
unique_id_entry_box2.pack()

# Run button
run_button = tk.Button(window, text="Run", command=run_program)
run_button.pack(pady=10)

# Message label to display output
print_message = tk.StringVar()
message_label = tk.Label(window, textvariable=print_message)
message_label.pack()

window.mainloop()
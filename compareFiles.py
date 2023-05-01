import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import threading
import os


def create_tooltip(widget, text):
    def enter(event):
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(
            tooltip, text=text, background="white", borderwidth=1, relief="solid"
        )
        label.pack()

    def leave(event):
        for t in widget.winfo_children():
            t.destroy()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


def compare_files(file1, file2, output_file, id_cols, file_format="csv"):
    # Add a function to read different file formats
    def read_file(file, format):
        if format == "csv":
            return pd.read_csv(file)
        elif format == "excel":
            return pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format.")

    # Read the files using the appropriate function
    df1 = read_file(file1, file_format)
    df2 = read_file(file2, file_format)

    # Set multi-level index
    df1["seq"] = df1.groupby(id_cols).cumcount()
    df2["seq"] = df2.groupby(id_cols).cumcount()
    df1 = df1.set_index(id_cols + ["seq"])
    df2 = df2.set_index(id_cols + ["seq"])

    # Merge DataFrames on index
    df1["row_number_file1"] = np.arange(2, len(df1) + 2)
    df2["row_number_file2"] = np.arange(2, len(df2) + 2)
    merged_df = df1.merge(
        df2,
        how="outer",
        left_index=True,
        right_index=True,
        suffixes=("_file1", "_file2"),
        indicator=True,
    )

    merged_df["row_number_file2"] = merged_df["row_number_file2"].fillna(0).astype(int)

    # Replace left_only and right_only in _merge column with actual file names
    merged_df["_merge"] = merged_df["_merge"].replace(
        {"left_only": file1 + "_ONLY", "right_only": file2 + "_ONLY"}
    )

    # Compare columns and store differences
    diff_data = {}
    summary_data = {}
    for col in df1.columns:
        if col in df2.columns:
            diff_col_name = f"{col}_diff"
            diff_data[diff_col_name] = np.where(
                merged_df[col + "_file1"] != merged_df[col + "_file2"], True, False
            )
            summary_data[col] = np.sum(diff_data[diff_col_name])

    # Create a DataFrame of actual differences
    actual_diff_df = pd.DataFrame(diff_data, index=merged_df.index)
    actual_diff_df["row_number_file1"] = merged_df["row_number_file1"]
    actual_diff_df["row_number_file2"] = merged_df["row_number_file2"]
    actual_diff_df["_merge"] = merged_df["_merge"]

    # Reorder columns to move the _merge column to the end
    columns = actual_diff_df.columns.tolist()
    columns.remove("_merge")
    columns.append("_merge")
    actual_diff_df = actual_diff_df[columns]

    # Filter out rows with no differences
    actual_diff_df = actual_diff_df[actual_diff_df.any(axis=1)]

    # Replace True with actual values side by side
    for col in actual_diff_df.columns:
        if col != "_merge" and not col.startswith("row_number"):
            actual_diff_col = col.replace("_diff", "")
            file1_col = actual_diff_col + "_file1"
            file2_col = actual_diff_col + "_file2"
            actual_diff_df[col] = np.where(
                actual_diff_df[col],
                merged_df[file1_col].astype(str).replace("nan", "--")
                + " | "
                + merged_df[file2_col].astype(str).replace("nan", "--"),
                "--",
            )

    # Calculate the number of differences per column
    summary_df = pd.DataFrame(summary_data, index=["num_differences"]).transpose()
    summary_df.index.name = "column_name"

    # Get the unique row numbers for each file
    unique_rows_file1 = merged_df[merged_df["_merge"] == file1 + "_ONLY"].index.tolist()
    unique_rows_file2 = merged_df[merged_df["_merge"] == file2 + "_ONLY"].index.tolist()

    # Add unique row numbers to the summary DataFrame
    summary_df.loc[file1 + "_unique_rows", "num_differences"] = str(unique_rows_file1)
    summary_df.loc[file2 + "_unique_rows", "num_differences"] = str(unique_rows_file2)

    # Write the summary to a separate CSV file
    summary_file = os.path.join(
        os.path.dirname(output_file), f"summary_{os.path.basename(output_file)}"
    )
    summary_df.to_csv(summary_file, index_label="column_name")

    # Write the results to a new CSV file
    actual_diff_df.to_csv(output_file, index_label=id_cols)


def browse_file(entry_widget):
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx"),
            ("All Files", "*.*"),
        ]
    )
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)


def run_comparison(
    file1_entry, file2_entry, output_format, progress_bar, summary_text, id_cols_entry
):
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()

    if file1_path and file2_path:
        output_path = filedialog.asksaveasfilename(
            defaultextension=".{}".format(output_format.get()),
            filetypes=[
                ("CSV Files", "*.csv"),
                ("Excel Files", "*.xlsx"),
                ("All Files", "*.*"),
            ],
        )
        if output_path:
            id_cols = id_cols_entry.get().strip().split(",")
            progress_bar.start()
            compare_files(
                file1_path,
                file2_path,
                output_path,
                id_cols=id_cols,
                file_format=output_format.get(),
            )
            progress_bar.stop()
            progress_bar.grid_forget()

            summary_file = os.path.join(
                os.path.dirname(output_path), f"summary_{os.path.basename(output_path)}"
            )

            with open(summary_file, "r") as f:
                summary_text.delete(1.0, tk.END)
                summary_text.insert(tk.END, f.read())

            status_label.config(text="Comparison complete.")
        else:
            status_label.config(text="Output file not selected.")
    else:
        status_label.config(text="Input files not selected.")


def exit_app():
    root.destroy()


def reset(file1_entry, file2_entry, output_format, progress_bar, summary_text):
    file1_entry.delete(0, tk.END)
    file2_entry.delete(0, tk.END)
    output_format.set("csv")
    progress_bar.grid_forget()
    summary_text.delete(1.0, tk.END)
    status_label.config(text="")


def update_progress_bar(current, total):
    progress_percentage = (current / total) * 100
    progress_bar["value"] = progress_percentage
    progress_label.config(text=f"Progress: {progress_percentage:.1f}%")


root = tk.Tk()
root.title("CSV File Comparison Tool")
root.geometry("1000x800")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(
    6, weight=1
)  # Add this line to configure the row containing the summary_text widget

file1_frame = ttk.LabelFrame(mainframe, text="First File")
file1_frame.grid(column=0, row=0, sticky=(tk.W, tk.E), padx=10, pady=10)
file1_frame.columnconfigure(1, weight=1)

file2_frame = ttk.LabelFrame(mainframe, text="Second File")
file2_frame.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=10, pady=10)
file2_frame.columnconfigure(1, weight=1)

compare_files_btn = ttk.Button(mainframe, text="Compare Files", command=compare_files)
compare_files_btn.grid(column=0, row=2, padx=10, pady=10)

file2_format = tk.StringVar()
file2_format.set("csv")

file2_format_label = ttk.Label(file2_frame, text="File Format:")
file2_format_label.grid(column=3, row=0, padx=5, pady=5)

file2_format_combobox = ttk.Combobox(
    file2_frame, textvariable=file2_format, state="readonly"
)
file2_format_combobox["values"] = ("csv", "excel")
file2_format_combobox.grid(column=4, row=0, padx=5, pady=5)

file1_entry = ttk.Entry(file1_frame)
file1_entry.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

file1_btn = ttk.Button(
    file1_frame, text="Browse", command=lambda: browse_file(file1_entry)
)
file1_btn.grid(column=2, row=0, padx=5, pady=5)

file2_entry = ttk.Entry(file2_frame)
file2_entry.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

file2_btn = ttk.Button(
    file2_frame, text="Browse", command=lambda: browse_file(file2_entry)
)
file2_btn.grid(column=2, row=0, padx=5, pady=5)

file1_format = tk.StringVar()
file1_format.set("csv")

file1_format_label = ttk.Label(file1_frame, text="File Format:")
file1_format_label.grid(column=3, row=0, padx=5, pady=5)

file1_format_combobox = ttk.Combobox(
    file1_frame, textvariable=file1_format, state="readonly"
)
file1_format_combobox["values"] = ("csv", "excel")
file1_format_combobox.grid(column=4, row=0, padx=5, pady=5)

file1_identifier_label = ttk.Label(file1_frame, text="Identifier Column:")
file1_identifier_label.grid(column=5, row=0, padx=5, pady=5)

file1_identifier_entry = ttk.Entry(file1_frame)
file1_identifier_entry.grid(column=6, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

file2_identifier_label = ttk.Label(file2_frame, text="Identifier Column:")
file2_identifier_label.grid(column=5, row=0, padx=5, pady=5)

file2_identifier_entry = ttk.Entry(file2_frame)
file2_identifier_entry.grid(column=6, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

# Replace the following lines of code to create separate tooltips for the input fields and buttons
create_tooltip(file1_btn, "Click to select the first file")
create_tooltip(file2_btn, "Click to select the second file")
create_tooltip(file1_format_combobox, "Select the format of the first file")
create_tooltip(file2_format_combobox, "Select the format of the second file")
create_tooltip(file1_identifier_label, "Enter the identifier column for the first file")
create_tooltip(
    file2_identifier_label, "Enter the identifier column for the second file"
)
create_tooltip(compare_files_btn, "Click to compare the files")

# Modify the following lines of code to show the progress percentage and update the label text
progress_label = ttk.Label(mainframe, text="Progress: 0.0%")
progress_label.grid(column=0, row=4, sticky=(tk.W, tk.E), padx=10, pady=(0, 5))

id_cols_frame = ttk.Frame(mainframe)
id_cols_frame.grid(column=0, row=2, sticky=(tk.W, tk.E))
id_cols_frame.columnconfigure(1, weight=1)

id_cols_label = ttk.Label(id_cols_frame, text="Identifier Columns (comma separated):")
id_cols_label.grid(column=0, row=0, padx=5, pady=5)

id_cols_entry = ttk.Entry(id_cols_frame)
id_cols_entry.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))
id_cols_entry.insert(0, "Ref,DateDue")

# Add the following lines below the id_cols_entry
control_col1 = tk.StringVar()
control_col1.set("Ref")

control_col2 = tk.StringVar()
control_col2.set("DateDue")

control_col1_label = ttk.Label(id_cols_frame, text="Control Column 1:")
control_col1_label.grid(column=2, row=0, padx=5, pady=5)

control_col1_entry = ttk.Entry(id_cols_frame, textvariable=control_col1)
control_col1_entry.grid(column=3, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

control_col2_label = ttk.Label(id_cols_frame, text="Control Column 2:")
control_col2_label.grid(column=4, row=0, padx=5, pady=5)

control_col2_entry = ttk.Entry(id_cols_frame, textvariable=control_col2)
control_col2_entry.grid(column=5, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))


output_format_frame = ttk.Frame(mainframe)
output_format_frame.grid(column=0, row=3, sticky=(tk.W, tk.E))

output_format_label = ttk.Label(output_format_frame, text="Output Format:")
output_format_label.grid(column=0, row=0, padx=5, pady=5)

output_format = tk.StringVar()
output_format.set("csv")

output_format_combobox = ttk.Combobox(
    output_format_frame, textvariable=output_format, state="readonly"
)
output_format_combobox["values"] = ("csv", "excel")
output_format_combobox.grid(column=1, row=0, padx=5, pady=5)

compare_button = ttk.Button(
    mainframe,
    text="Compare Files",
    command=lambda: threading.Thread(
        target=run_comparison,
        args=(
            file1_entry,
            file2_entry,
            output_format,
            progress_bar,
            summary_text,
            id_cols_entry,
        ),
    ).start(),
)
compare_button.grid(column=0, row=3, padx=5, pady=10)

progress_bar = ttk.Progressbar(mainframe, mode="indeterminate")
progress_bar.grid(column=0, row=4, padx=5, pady=10, sticky=(tk.W, tk.E))

summary_label = ttk.Label(mainframe, text="Summary:")
summary_label.grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)

summary_text = tk.Text(mainframe, wrap=tk.WORD, width=100, height=15)
summary_text.grid(column=0, row=6, padx=5, pady=5, sticky=(tk.W, tk.E))

status_label = ttk.Label(mainframe, text="")
status_label.grid(column=0, row=7, padx=5, pady=5)

reset_button = ttk.Button(
    mainframe,
    text="Reset",
    command=lambda: reset(
        file1_entry, file2_entry, output_format, progress_bar, summary_text
    ),
)
reset_button.grid(column=0, row=8, padx=5, pady=5)

exit_button = ttk.Button(mainframe, text="Exit", command=exit_app)
exit_button.grid(column=0, row=9, padx=5, pady=5)

root.mainloop()

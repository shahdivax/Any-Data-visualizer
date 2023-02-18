import math
import tkinter

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox
import matplotlib.dates as mdates
from matplotlib import ticker

root = Tk()
root.title("CSV Plotter")

# Global variables
df = None
column1_name = ""
column2_name = ""
chart_type = ""
chart_title = ""
filef = False


# Create the GUI
def create_gui():
    global column1_dropdown, column2_dropdown, chart_type_dropdown, chart_title_entry, T1, T2,TF

    TF = StringVar()
    T1 = StringVar()
    T2 = StringVar()

    # Load button
    load_button = Button(root, text="Load CSV", command=load_csv)
    load_button.pack()

    Tk3 = Message(root, textvariable=TF)
    Tk3.pack()
    TF.set("file : {}".format("None"))

    # Column 1 dropdown menu
    column1_label = Label(root, text="Select column for X-axis:")
    column1_label.pack()
    column1_dropdown = OptionMenu(root, StringVar(), "")
    column1_dropdown.pack()

    Tk1 = Message(root, textvariable=T1)
    Tk1.pack()
    T1.set("X-axis : {}".format("None"))

    # Column 2 dropdown menu
    column2_label = Label(root, text="Select column for Y-axis:")
    column2_label.pack()
    column2_dropdown = OptionMenu(root, StringVar(), "")
    column2_dropdown.pack()

    Tk2 = Message(root, textvariable=T2)
    Tk2.pack()
    T2.set("Y-axis : {}".format("None"))

    # Chart type dropdown menu
    chart_type_label = Label(root, text="Select chart type:")
    chart_type_label.pack()
    chart_type_dropdown = OptionMenu(root, StringVar(), "line", "bar", "pie", "scatter")
    chart_type_dropdown.pack()

    # Chart title entry
    chart_title_label = Label(root, text="Enter chart title:")
    chart_title_label.pack()
    chart_title_entry = Entry(root)
    chart_title_entry.pack()

    # Create button
    create_button = Button(root, text="Create Plot", command=create_plot)
    create_button.pack()


# Load the CSV file
def load_csv():
    global df, column1_name, column2_name,filef

    # Load the CSV file
    filepath = filedialog.askopenfilename()
    if filepath:
        df = pd.read_csv(filepath)
        filef = True
        ff = filepath.split("/")
        TF.set("file : {}".format(ff[len(ff)-1]))
        # Get the column names from the CSV file
        column_names = list(df.columns.values)

        # Populate the dropdown menus with the column names
        column1_dropdown["menu"].delete(0, "end")
        column2_dropdown["menu"].delete(0, "end")
        for name in column_names:
            column1_dropdown["menu"].add_command(label=name, command=lambda value=name: set_column1(value))
            column2_dropdown["menu"].add_command(label=name, command=lambda value=name: set_column2(value))

        # Set the default column names
        column1_name = column_names[0]
        column2_name = column_names[1]
        T1.set("X-axis : {}".format(column1_name))
        T2.set("Y-axis : {}".format(column2_name))

        try:
            df[column1_name] = pd.to_datetime(df[column1_name])
        except:
            pass

        # # Disable the column selection dropdown menus for non-numeric columns
        # for column_name in column_names[1:]:
        #     if df[column_name].dtype == "object":
        #         column1_dropdown["state"] = "disabled"
        #         column2_dropdown["state"] = "disabled"
        #         messagebox.showwarning("Non-numeric column",
        #                                f"The column {column_name} is non-numeric and cannot be used for plotting.")
        #         break
    else:
        messagebox.showwarning("File not selected", "No CSV file was selected.")


# Set the column 1 name
def set_column1(name):
    global column1_name
    column1_name = name
    T1.set("X-axis : {}".format(column1_name))


# Set the column 2 name
def set_column2(name):
    global column2_name
    column2_name = name
    T2.set("Y-axis : {}".format(column2_name))


# Create the plot
def create_plot():
    global column1_name, column2_name, chart_type, chart_title

    # Get the selected chart type and title
    chart_type = chart_type_dropdown.cget("text")
    if len(chart_type) != 0 and filef:
        chart_title = chart_title
        chart_title = chart_title_entry.get()

        # Create the plot based on the selected chart type
        if chart_type == "line":
            plt.plot(df[column1_name], df[column2_name])
        elif chart_type == "bar":
            plt.bar(df[column1_name], df[column2_name])
        elif chart_type == "pie":
            plot_pie_chart()
        elif chart_type == "scatter":
            plt.scatter(df[column1_name], df[column2_name])

        # Set the chart title and axis labels
        plt.title(chart_title)
        plt.xlabel(column1_name)
        plt.ylabel(column2_name)
        plt.xticks(rotation=45)

        # Show the plot
        plt.show()
    else:
        messagebox.showwarning("Chart or File not selected", "No Chart Type or File was selected.")


def plot_pie_chart():
    # Group the data by the selected column and sum the other column
    selected_column = column1_name
    group_by_column = df.groupby(selected_column).sum().reset_index()

    # Set the title
    plt.title(chart_title)

    # Plot the pie chart
    plt.pie(group_by_column.iloc[:, 1], labels=group_by_column.iloc[:, 0], autopct='%1.1f%%', startangle=90)


# Create the GUI
create_gui()

# Start the main loop
root.mainloop()

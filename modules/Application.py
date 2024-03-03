import sqlite3
import folium
import webbrowser
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from statistics import mean


# Function to create a map with markers
def create_map(data=None, path='./templates/map.html', location=(45.7578, 4.8351), zoom=12,
               icon_path="./static/icons/tree-icon.png"):
    """
    Create a map with markers from the given data and save it to the specified path.

    Args:
        data (list): List of marker data tuples (latitude, longitude, planting_date).
        path (str): Path to save the map HTML file.
        location (tuple): Center location of the map (latitude, longitude).
        zoom (int): Zoom level of the map.
        icon_path (str): Path to the custom marker icon image.

    Returns:
        str: Path to the saved map HTML file.
    """
    # Create a Folium map object
    m = folium.Map(location=location, zoom_start=zoom, attr='© Contributors OpenStreetMap')

    # Add markers to the map if data is provided
    if data is not None:
        for marker_data in data[:]:
            # Create marker tooltip showing tree age
            tooltip = "unknown age" if marker_data[
                                           2] is None else f"{datetime.now().year - int(marker_data[2][:4])} years"

            # Add marker to the map
            folium.Marker(
                location=(marker_data[0], marker_data[1]),
                tooltip=tooltip,
                icon=folium.CustomIcon(icon_path, icon_size=(50, 50)),
            ).add_to(m)

    # Save the map as an HTML file
    m.save(path)
    return path


# Function to show a warning popup
def popup_warning(n):
    """
    Show a warning popup with the given message and return user response.

    Args:
        n (int): Number of trees.

    Returns:
        bool: True if user chooses to continue, False otherwise.
    """

    # Function to proceed with the operation
    def proceed():
        window.destroy()
        result.set(True)

    # Function to cancel the operation
    def cancel():
        window.destroy()
        result.set(False)

    # Create a Tkinter window for the popup
    window = tk.Tk()
    window.title("WARNING")

    # Display warning message
    label_message = tk.Label(window,
                             text=f"Please note that there are {n} trees, the browser may have difficulty displaying them.")
    label_message.pack(padx=20, pady=20)

    # Create "Continue" button
    button_continue = tk.Button(window, text="Continue", command=proceed)
    button_continue.pack(side="left", padx=10, pady=10)

    # Create "Cancel" button
    button_cancel = tk.Button(window, text="Cancel", command=cancel)
    button_cancel.pack(side="right", padx=10, pady=10)

    # Variable to store user response
    result = tk.BooleanVar()
    result.set(False)

    # Start the Tkinter event loop
    window.mainloop()

    # Return user response
    return result.get()


# Function to create the application GUI
def application(defaultgenus="Cercis"):
    """
    GUI application for selecting genus and language.

    Args:
        defaultgenus (str): Default genus selected.

    Returns:
        str: Selected genus.
    """
    global c, genus_names, language

    # Function to launch the map creation
    def launch():
        global language

        genus = genus_var.get()

        # Query database to get tree markers
        c.execute(
            f"select latitude, longitude, planting_date from trees join genus_names on trees.genus = genus_names.Latin where {language} = '{genus}'")
        markers = c.fetchall()

        # Check if number of markers exceeds a threshold and show warning popup if necessary
        if len(markers) < 1000 or popup_warning(len(markers)):
            # Open web browser with the map
            webbrowser.open(create_map(data=markers, location=(
                mean([marker[0] for marker in markers]), mean([marker[1] for marker in markers]))))
        return genus

    # Function to retrieve info and destroy the app window
    def retrieve_info(app):
        info = launch()

        app.destroy()
        application(defaultgenus=info)

    # Function to change the language
    def change_language():
        global language
        last_language = language
        language = language_menu.get()
        new_genus_list = genus_names[language][:]
        new_genus_list.sort()
        genus_menu.config(values=new_genus_list)
        genus_var.set(genus_names[language][genus_names[last_language].index(genus_var.get())])

    # Create a Tkinter application window
    app = tk.Tk()
    app.title("genus selection")
    app.config(bg="black")
    app.attributes("-topmost", True)

    # Retrieve genus list and set default genus
    genus_list = genus_names[language][:]
    genus_list.sort()
    genus_var = tk.StringVar(app)
    genus_var.set(defaultgenus)

    # Add genus selection label and combobox
    genus_label = tk.Label(app, text="Select a genus :", fg="white", bg="black")
    genus_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
    genus_menu = ttk.Combobox(app, textvariable=genus_var, values=genus_list, state="readonly", width=20)
    genus_menu.grid(row=1, column=0, sticky='w', padx=10, pady=10)

    # Add language selection label and combobox
    language_var = tk.StringVar(app)
    language_var.set(language)
    language_label = tk.Label(app, text="Language", fg="white", bg="black")
    language_label.grid(row=0, column=1, sticky='e', padx=10, pady=10)
    language_menu = ttk.Combobox(app, textvariable=language_var, values=list(genus_names.keys()), state="readonly",
                                 width=10)
    language_menu.grid(row=1, column=1, sticky='e', padx=10, pady=10)
    language_menu.bind("<<ComboboxSelected>>", lambda event: change_language())

    # Add "Exit" button
    quit_button = tk.Button(app, text="Exit", command=app.destroy, bg="black", fg="white")
    quit_button.grid(row=3, column=0, sticky='w', padx=10, pady=10)

    # Add "Run" button
    launch_button = tk.Button(app, text="Run", command=lambda: retrieve_info(app), bg="black", fg="white")
    launch_button.grid(row=3, column=1, sticky='e', padx=10, pady=10)

    # Start the Tkinter event loop
    app.mainloop()


# Function to run the application
def run_app():
    """
        Runs application with default parameters.
    """
    global c, genus_names, language
    language = "Latin"

    # Connect to the SQLite database
    connexion_BD = sqlite3.connect('./static/data/trees.sqlite3')
    c = connexion_BD.cursor()

    # Retrieve genus names from the database
    c.execute("select * from genus_names")
    result = c.fetchall()
    genus_names = {"Latin": [row[0] for row in result],
                   "Français": [row[1] for row in result],
                   "English": [row[2] for row in result]}

    # Launch the application GUI
    application()
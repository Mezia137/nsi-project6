import csv
from datetime import datetime


# Function to import data from a CSV file
def import_csv(path='./static/data/trees_data.csv'):
    """
    Import data from a CSV file and return it as a list of dictionaries.

    Args:
        path (str): Path to the CSV file.

    Returns:
        list: List of dictionaries containing the data.
    """
    with open(path, 'r') as csvfile:
        data = list(csv.DictReader(csvfile, delimiter=';'))

    return data


# Function to process the imported data
def data_processing(trees_data):
    """
    Process the imported data and clean it.

    Args:
        trees_data (list): List of dictionaries containing the data.

    Returns:
        list: List of cleaned data dictionaries.
    """
    trees_data_clean = []
    id_counter = 0
    for i, arbre_data in enumerate(trees_data):
        if arbre_data['codegenre'] not in ['0', '1'] and (
                arbre_data['anneeplantation'] == '' or int(arbre_data['anneeplantation']) >= 1900):
            trees_data_clean.append({
                'circumference': None if arbre_data['circonference_cm'] in ['0', ''] else int(
                    arbre_data['circonference_cm']),
                'height': None if arbre_data['hauteurtotale_m'] in ['0', ''] else int(
                    arbre_data['hauteurtotale_m']),
                'planting_date': None if arbre_data['dateplantation'] in [''] else datetime.strptime(
                    arbre_data['dateplantation'], "%Y-%m-%d").date(),
                'genus': arbre_data['genre'],
                'species': arbre_data['espece'],
                'variety': arbre_data['variete'],
                'planting_area': arbre_data['localisation'],
                'municipality': arbre_data['commune'],
                'street_name': arbre_data['nomvoie'],
                'longitude': float(arbre_data['lon'].replace(',', '.')),
                'latitude': float(arbre_data['lat'].replace(',', '.')),
                'identifier': id_counter
            })

            id_counter += 1

    return trees_data_clean


# Function to export cleaned data to a CSV file
def export_csv(trees_data_clean, path='./static/data/trees_data_clean.csv'):
    """
    Export cleaned data to a CSV file.

    Args:
        trees_data_clean (list): List of cleaned data dictionaries.
        path (str): Path to save the CSV file.
    """
    # Get keys of the first dictionary and move 'identifier' to the beginning
    k = list(trees_data_clean[0].keys())
    k.remove('identifier')
    k.insert(0, 'identifier')

    # Write data to the CSV file
    with open(path, 'w', newline='') as fichier_csv:
        writer = csv.DictWriter(fichier_csv, fieldnames=k)
        writer.writeheader()
        writer.writerows(trees_data_clean)


# Function to perform default data processing and export
def default_data_processing():
    """
    Perform default data processing and export.
    """
    export_csv(data_processing(import_csv()))

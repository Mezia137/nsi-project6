from modules.Application import run_app
from modules.CSVprocessing import default_data_processing


def main(args):
    # CSV data processing: import of the original CSV, processing and export to a clean CSV.
    # default_data_processing()

    # Application: opening of a genre selection window and creation and display of a personalized map.
    run_app()


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))

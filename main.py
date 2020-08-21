import argparse
from src import user_interaction
from src.excel_file_processing import extract_data_from_file


parser = argparse.ArgumentParser()
parser.add_argument("--input-file", type=str, required=True)

args = parser.parse_args()

extract_data_from_file(file=args.input_file)

user = user_interaction.user_interaction()

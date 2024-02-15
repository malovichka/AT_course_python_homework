import os
import csv
import json


def converter_to_json(file_path: str, converted_file_name: str = "converted") -> None:
    """This function converts content of the given csv file to json
    Args:
    file_path (str) - path to the file that will be converted
    converted_file_name (str) - name with which .jsom file will be saved, default option - 'converted.json'
    """

    # deserializing csv into python object (reading data from the file and writing into data_list)
    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)
        data_list = list(reader)
    # serializing python object into json file
    with open(f"{converted_file_name}.json", "w") as json_file:
        json.dump(data_list, json_file, indent=2)


if __name__ == "__main__":
    cars_csv = os.path.abspath("cars.csv")
    converter_to_json(file_path=cars_csv, converted_file_name="list_of_cars")

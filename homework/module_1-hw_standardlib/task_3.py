import os
import csv
import json


def converter_to_json(file_path: str, converted_file_name: str = "converted") -> None:
    data_list = []
    # deserializing csv into python object (reading data from the file and writing into data_list)
    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(row)
    # serializing python object into json file
    with open(f"{converted_file_name}.json", "w") as json_file:
        json.dump(data_list, json_file, indent=2)


if __name__ == "__main__":
    cars_csv = os.path.abspath("module_2-hw_standardlib\cars.csv")
    converter_to_json(cars_csv, "module_2-hw_standardlib\list_of_cars")

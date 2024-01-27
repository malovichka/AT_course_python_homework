import os
import sys
import argparse
import prettytable


def directory_content(directory: str):
    """This function takes a path to a directory as an argument and prints a table with its contents and their data"""

    content_table = prettytable.PrettyTable()
    content_table.field_names = ["Mode", "Owner", "Group", "Size", "File name"]
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        item_info = os.stat(item_path)
        content_table.add_row(
            [
                item_info.st_mode,
                item_info.st_uid,
                item_info.st_gid,
                item_info.st_size,
                item,
            ]
        )

    print(content_table)


def parse_cmd_args():
    path_help = "Path to a folder"
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help=path_help)

    if len(sys.argv) <= 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    cmd, _ = parser.parse_known_args()

    return cmd.path


if __name__ == "__main__":
    directory = parse_cmd_args()
    directory_content(directory)

import sys


def file_size(size_in_bytes: int) -> str:
    """This function converts given in bytes size of the file to kilobytes, megabytes or gigabytes
    Args:
    size_in_bytes (int) - size of the file in bytes"""
    measures = ["B", "Kb", "Mb", "Gb"]
    i = 0
    if size_in_bytes < 1024:
        pass
    else:
        while size_in_bytes >= 1024 and i < len(measures) - 1:
            size_in_bytes /= 1024
            i += 1
    return f"{size_in_bytes:.1f}{measures[i]}"


if __name__ == "__main__":
    # answer to the question from task
    print(file_size(sys.maxsize))
    assert file_size(19) == "19.0B"
    assert file_size(12345) == "12.1Kb"
    assert file_size(1101947) == "1.1Mb"
    assert file_size(572090) == "558.7Kb"
    assert file_size(999999999999) == "931.3Gb"

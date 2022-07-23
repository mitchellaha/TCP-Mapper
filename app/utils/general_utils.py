import errno
import json
import os


def save_to_JSON(Dictionary: dict, FileName: str):  # ? Unused in Main
    """
    Saves the dictionary to a JSON file
    """
    # make directory if it doesn't exist
    if not os.path.exists("output"):
        try:
            os.makedirs("output")
        except OSError as exc:  # Guard against
            if exc.errno != errno.EEXIST:
                raise
    with open("./output/" + FileName, "w") as f:
        json.dump(Dictionary, f)
        f.close()

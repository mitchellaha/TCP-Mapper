from datetime import datetime as dt


def metadata_dt_convert(dict):
    """
    Converts the string to a datetime object
    """
    # Current Date and Time String = 2/1/2022 8:47 AM
    listToConvert = ["Date modified", "Date accessed", "Date created"]
    for key in listToConvert:
        if key in dict:
            dict[key] = dt.strptime(dict[key], "%m/%d/%Y %I:%M %p")
    return dict

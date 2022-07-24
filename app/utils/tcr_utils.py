

def find_dict_type(Dictionary: dict):
    """
    Utility function to find the type of dictionary. eg. Ticket or Customer
    """
    if "CheckWithForeman" in Dictionary.keys():  # CheckWithForeman is a key that SHOULD only show in Ticket a dictionary
        return "Ticket"
    elif "BillingCycle" in Dictionary.keys():  # BillingCycle is a key that SHOULD only show in Customer a dictionary
        return "Customer"
    else:
        return "Unknown"

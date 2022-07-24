# Need To ReWrite TCRAPI Filter/Sort Building Before Continuing

import datetime as dt
import json
import os

from dotenv import load_dotenv
from TCRAPI import api, auth
from TCRAPI.getgriddata import customersClass, ticketsClass

load_dotenv()

TCRAUTH = auth(email=os.getenv("TCR_EMAIL"), password=os.getenv("TCR_PASSWORD"))
tcr = api(headers=TCRAUTH.header)


def datetime_to_string(datetime: dt.datetime):  # Not Really Needed For This Script Only JSON testing
    return datetime.strftime("%Y-%m-%d %H:%M:%S")

def milliseconds_to_datetime(milliseconds: int):  # ? As much as i would like to move this to datetime_utils, id rather handlers be independent
    """
    Convert milliseconds to datetime object removing the "/Date(...)/"
    """
    seconds = int("".join([x for x in milliseconds if x.isdigit()])) / 1000  # Remove the "/Date(...)/" and convert to seconds
    return dt.datetime.fromtimestamp(seconds) + dt.timedelta(hours=1)  # Add 1 Hour Since TCR is off by 1 hour

class Customer_TCR:
    ID_KEY = "CustomerID"
    GRID_INFO = customersClass()

    def __init__(self):
        pass

    def get_customer(self, CustomerID: int):
        """
        Get a customer from TCR with the given CustomerID
        """
        customer = tcr.getCustomer(CustomerID)
        del customer["__type"]
        del customer["OriginalRecordData"]
        dateKeys = ["DateOpened", "DateCreated", "DateUpdated", "InsurCertExpiration"]
        for key in dateKeys:
            if customer[key] is not None:
                customer[key] = milliseconds_to_datetime(customer[key])
        return customer

    def get_customer_grid(self, StartIndex: int = 1, RecordCount: int = 250, IncludeCount: bool = False):  # TODO: Add Sort/Filter By Recently Updated
        customerGrid = tcr.getGridData(
            Grid=self.GRID_INFO.GRIDID,
            FilterConditions=self.GRID_INFO.filterConditions,
            StartIndex=StartIndex,
            RecordCount=RecordCount,
            IncludeCount=IncludeCount
        )
        return customerGrid

class Ticket_TCR:
    ID_KEY = "TicketID"
    GRID_INFO = ticketsClass()

    def get_ticket(TicketID: int):
        """
        Get a ticket from TCR with the given TicketID
        """
        ticket = tcr.getTicket(TicketID)
        del ticket["__type"]
        del ticket["OriginalRecordData"]
        dateKeys = ["TicketDate", "DelPUDate", "DateCreated", "DateUpdated", "PortalDateCreated",
                    "VoidDate", "DateSigned", "DateSigned_Adjusted", "DriverCompletedDate",
                    "DateFinalEdited", "EstimatedStartTime", "EstimatedEndTime"]
        for key in dateKeys:
            if ticket[key] is not None:
                ticket[key] = milliseconds_to_datetime(ticket[key])
        return ticket




ticketTest = Ticket_TCR.get_ticket(TicketID=1794817)
with open("Ticket.json", "w") as f:
    json.dump(ticketTest, f, indent=4, default=datetime_to_string)

customerTest = Customer_TCR.get_customer(CustomerID=47326)
with open("Customer.json", "w") as f:
    json.dump(customerTest, f, indent=4, default=datetime_to_string)

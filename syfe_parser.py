# -*- coding: utf-8 -*-
"""
Created on Sat May 16 00:14:55 2020

Updated script to handle certain bugs:
- "<0.01" issue. Value will be set to 0.00 instead.
- ValueError: could not convert string to float: "1,081.62" (due to the comma)

@author: KPO
"""

import numpy as np
import pandas as pd

from helper import reit_lookup

filename = "transactions.txt"
special = [
    "TRANSFER_IN",
    "BONUS_IN",
    "MANAGEMENT_FEE",
    "Funds added",
    "Bonus",
    "Management fee",
    "Adjustment (in)",
    "Portfolio transfer (in)",
]

list_date = []
list_type = []
list_details = []
list_amount = []
list_units = []

fh = open(filename)

counter = 1

with open(filename) as f:
    content = f.readlines()
    content = [x.strip() for x in content]

    for line in content:
        if line.strip() != "":
            if counter == 1:
                list_date.append(line)
                counter += 1
            elif counter == 2:
                list_type.append(line)
                if line in special:
                    list_details.append("")
                    counter += 2
                else:
                    counter += 1
            elif counter == 3:
                list_details.append(line)
                counter += 1
            elif counter == 4:
                list_amount.append(line)
                counter += 1
            elif counter == 5:
                if line == "<0.01":
                    line = 0.00
                list_units.append(line)
                counter = 1
        else:
            continue

df = pd.DataFrame(
    list(zip(list_date, list_type, list_details, list_amount, list_units)),
    columns=["Date", "Type", "Details", "Amount", "Units"],
)

# Remove commas in numbers
df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
df["Units"] = df["Units"].str.replace(",", "").astype(float)

# Compute price of stock
df["Computed_Price"] = df["Amount"] / df["Units"]

# Reformat datetime column
df["Date"] = pd.to_datetime(df["Date"])

# Set default exchange and currency
df["Exchange"] = "SGX"
df["Currency"] = "SGD"

# Map stock name to ticker symbol
df["Symbol"] = df["Details"].map(reit_lookup)

# Rename transaction type
df["Type"].replace(
    {"Bought": "BUY", "Sold": "SELL", "Management fee": "FEES"}, inplace=True
)

# Drop transactions of fund addition
df = df[df["Type"] != "Funds added"]
df = df[df["Type"] != "Dividend received"]

df.loc[df["Type"] == "FEES", "Units"] = np.NaN
df.loc[df["Type"] == "FEES", "Computed_Price"] = np.NaN
df.loc[df["Type"] == "FEES", "Symbol"] = np.NaN

# Add remarks
df["Remarks"] = ""

df = df[
    [
        "Type",
        "Exchange",
        "Symbol",
        "Units",
        "Currency",
        "Computed_Price",
        "Date",
        "Amount",
        "Remarks",
    ]
]

df.to_csv("syfe_transactions.csv", index=False, header=False)

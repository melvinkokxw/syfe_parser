import numpy as np
import pandas as pd

from helper import reit_lookup

input_df = pd.read_excel("./transactions.xlsx")
input_df = input_df[input_df["Trade Type"].isin(["BUY", "SELL", "MANAGEMENT_FEE"])]

"""
Column 1) (-1 or 1 or 0 to indicate sell for -1, buy for 1 and fees for 0) OR (Buy or Sell or Fees text are also acceptable)
Column 2) Exchange Code (i.e. SGX or HKEX)
Column 3) Symbol
Column 4) Units Purchased or Sold
Column 5) Currency
Column 6) Price Paid or Received (based on the currency this stock trades in)
Column 7) Date of transaction (YYYY-MM-DD or MM/DD/YYY)
Column 8) Total after fees (Blank is allowed) (based on the currency this stock trades in)
Column 9) Anything you would like to note about the transaction (Blank is allowed)
"""

df = pd.DataFrame()
df["Type"] = input_df["Trade Type"]
df["Type"].replace({"MANAGEMENT_FEE": "FEES"}, inplace=True)
df["Exchange"] = "SGX"
df["Symbol"] = input_df["Security Name"].map(reit_lookup)
df["Units"] = input_df["Units"]
df["Currency"] = "SGD"
df["Price"] = input_df["Price Per Unit"]
df["Date"] = input_df["Trade Date"]
df["Total"] = input_df["Net Amount"]
df["Remarks"] = ""

df.loc[df["Type"] == "FEES", "Units"] = np.NaN
df.loc[df["Type"] == "FEES", "Price"] = np.NaN
df.loc[df["Type"] == "FEES", "Symbol"] = np.NaN

df = df[["Type", "Exchange", "Symbol", "Units", "Currency", "Price", "Date", "Total", "Remarks"]]

df.to_csv("detailed_syfe_transactions.csv", index=False, header=False)

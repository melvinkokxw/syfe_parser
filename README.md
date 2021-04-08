# Syfe Parser

A parser for [Syfe](https://syfe.com) transactions, specifically for Syfe REIT+ portfolio. Output format is intended for importing into [StocksCafe](https://stocks.cafe). 

Contains two parser scripts, one for basic logs and one for detailed logs. 
- Basic log parser (adapted from [KPO's Syfe parser](https://gist.github.com/kpooooooooooo/93a40ef866113afc2b51d60cc3086333)) only requires copying and pasting from Syfe's website, but Syfe's practice of rounding off transactions to 2 decimal places causes inconsistences e.g. appearing to still own small amount of stock despite having sold them all off. 
- Detailed log parser requires a more detailed transaction history (up to 5 d.p.) that can be obtained by contacting Syfe's support.

## Usage

### Basic logs

Follow KPO's instructions [here](https://kpo-and-czm.blogspot.com/2020/05/syfe-transactions-parser.html) to get basic logs (i.e. copying transactions from Syfe's site). More detailed instructions can also be found [here](https://www.turtleinvestor.net/how-to-import-syfe-transactions-into-stockscafe-platform-using-python/).

Place `transactions.txt` in the same folder as `syfe_parser.py`

Install pandas

```bash
python3 -m pip install pandas -U
```

To run parser

```bash
python3 syfe_parser.py
```

### Detailed logs

To get detailed logs, drop Syfe's support a message requesting for detailed transaction history. Once file is obtained, rename file to `transactions.xlsx`. Place `transactions.xlsx` in the same folder as `detailed_syfe_parser.py`

Install required packages

```bash
python3 -m pip install pandas openpyxl -U
```

To run parser

```bash
python3 detailed_syfe_parser.py
```
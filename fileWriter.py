import pandas as pd

from stockscraper import parsePrice

prices = parsePrice()

stockPrices = pd.DataFrame(list(prices.items()), columns=['Stock', 'Price'])


#stockPricesFR = pd.DataFrame.from_records(prices)

print(stockPrices)

with pd.ExcelWriter('./ExcelSheets/stockPrices.xlsx', mode='a') as writer:
    stockPrices.to_excel(writer, sheet_name="Sheet1")

#print(stockPricesFR)
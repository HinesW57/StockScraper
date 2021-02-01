import os
import robin_stocks as r
import cryptoStocks as cs
import pandas as pd 
import matplotlib.pyplot as plt
from dotenv import load_dotenv



'''
Robinhood includes dividends as part of your net gain. This script removes
dividends from net gain to figure out how much your stocks/options have paid
off.
Note: load_portfolio_profile() contains some other useful breakdowns of equity.
Print profileData and see what other values you can play around with.
'''
load_dotenv()
#!!! Fill out username and password
try:
     username = os.environ["RHUSERNAME"]
except:
    print("Please set the USERNAME environment variable")
try:
     password = os.environ["RHPASSWORD"]
except:
    print("Please set the PASSWORD environment variable")

#!!!

login = r.login(username,password)

profileData = r.load_portfolio_profile()
allTransactions = r.get_bank_transfers()
cardTransactions= r.get_card_transactions()

deposits = sum(float(x['amount']) for x in allTransactions if (x['direction'] == 'deposit') and (x['state'] == 'completed'))
withdrawals = sum(float(x['amount']) for x in allTransactions if (x['direction'] == 'withdraw') and (x['state'] == 'completed'))
debits = sum(float(x['amount']['amount']) for x in cardTransactions if (x['direction'] == 'debit' and (x['transaction_type'] == 'settled')))
reversal_fees = sum(float(x['fees']) for x in allTransactions if (x['direction'] == 'deposit') and (x['state'] == 'reversed'))

money_invested = deposits + reversal_fees - (withdrawals - debits)
dividends = r.get_total_dividends()
percentDividend = dividends/money_invested*100

equity = float(profileData['extended_hours_equity'])
totalGainMinusDividends = equity - dividends - money_invested
percentGain = totalGainMinusDividends/money_invested*100

print("The total money invested is {:.2f}".format(money_invested))
print("The total equity is {:.2f}".format(equity))
print("The net worth has increased {:0.2}% due to dividends that amount to {:0.2f}".format(percentDividend, dividends))
print("The net worth has increased {:0.3}% due to other gains that amount to {:0.2f}".format(percentGain, totalGainMinusDividends))
print("\n")

stocks = r.build_holdings()


def individualStockPerformanceBreakdown():

    total_profit = 0.00

    for key, i in stocks.items():
        spent = (float(i['average_buy_price'])*float(i['quantity']))
        currentCost = (float(i['price'])) * float(i['quantity'])
        print("{} has a price of {:0.2f}. You have {:0.2f} share(s) at {:0.2f} a share.".format(key, float(i['price']), float(i['quantity']), float(i['average_buy_price'])))
        print("You have {:0.2f} invested. Your current value is {:0.2f}. Your profit for {} is {:0.2f}.".format(spent,currentCost, key, (currentCost-spent)))
        print("Your percentage gain/loss is {:0.2f}%.\n".format(float((currentCost-spent)/spent)*100))
        total_profit += (currentCost-abs(spent))

    print("Your total profit is {:0.2f}.".format(total_profit))
    print("\n")




stocks_df = pd.DataFrame(stocks)

def printStockEquity():

    stocks_equity = stocks_df.loc['equity']
    #print(stocks_equity)
    stocks_equity=stocks_equity.astype(float)
    plt.figure();
    ax = stocks_equity.plot(kind='bar', title='Stock Equity')
    
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() /2

        space = 5
        va = 'bottom'

        if y_value < 0:
            space *= -1
            va = 'top'
        label = "{:.1f}".format(y_value)

        ax.annotate(
            label,
            (x_value, y_value),
            xytext=(0, space),
            textcoords="offset points",
            ha='center',
            va=va)


    # plt.bar(range(len(stocks)), list(stocks.values()), align='center')
    # plt.xticks(range(len(stocks)), list(stocks.keys()))
    plt.show()


if __name__ == "__main__":
    individualStockPerformanceBreakdown()
    cs.print_crypto_info()
    printStockEquity()
    #print(stocks)

#TODO crate a dictionary with key = symbol and value = %gain/loss, order by highest gains

#© 2020 GitHub, Inc.
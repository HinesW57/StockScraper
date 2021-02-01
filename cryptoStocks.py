import os
import robin_stocks as r

'''
Robinhood includes dividends as part of your net gain. This script removes
dividends from net gain to figure out how much your stocks/options have paid
off.
Note: load_portfolio_profile() contains some other useful breakdowns of equity.
Print profileData and see what other values you can play around with.
'''
#!!! Fill out username and password
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
crypto = r.crypto.load_crypto_profile()
quantity = r.crypto.get_crypto_positions('quantity')
quantity = float(quantity[0])
symbol = r.crypto.get_crypto_positions('currency')
symbol = symbol[0]
symbol = symbol['code']
paid = r.crypto.get_crypto_positions('cost_bases')
paid = paid[0][0]['direct_cost_basis']
paid = float(paid)
#paid = round(float(paid),2)
current_price = float(r.crypto.get_crypto_quote('BTC')['ask_price'])
current_value = current_price * quantity


def get_crypto_earnings():
    #TODO
    ###THIS FUNCTION SHOULD RETURN A LIST OF CRYPTOS WITH A DICTIONARY OF VALUES###
    ###VALUES WOULD BE QTY, PAID, SYBOL, CURRENT_PRICE, CURRENT_VALUE, PERCENT_CHANGE###
    
    pass

def print_crypto_info():
    print("You have {:0.4f} {} in your account.".format(quantity,symbol))
    print("You have invested ${:0.2f}.".format(paid))
    print("The current price of {} is ${:0.2f}.".format(symbol, current_price))
    print("You have a value of ${:0.2f}.".format(quantity*current_price))
    print("Your % change is {:0.2f}%.".format(((current_value-paid)/paid)*100))



if __name__ == "__main__":   
    print("You have {:0.4f} {} in your account.".format(quantity,symbol))
    print("You have invested ${:0.2f}.".format(paid))
    print("The current price of {} is ${:0.2f}.".format(symbol, current_price))
    print("You have a value of ${:0.2f}.".format(quantity*current_price))
    print("Your % change is {:0.2f}%.".format(((current_value-paid)/paid)*100))

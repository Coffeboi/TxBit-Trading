# Written by Coffeboi

from secrets import APIKEY, SECRET
from txbit import Txbit
import time
import requests
import os
import random

# Access secret apis
client = Txbit(APIKEY, SECRET)

def trade():
    # Amount used for trading.
    amount = int("1337")

    # Get current ask price.
    price = client.getTicker("XKR/USDT")
    price_ask = price.result["Ask"]
    price_bid = price.result["Bid"]

    spread = price_ask - price_bid
    print("The spread right now is " + str((round(spread / price_ask, 2)) * 100) + "%")

    # Get my prices
    my_ask = round(price_ask - 0.00000001, 8)
    my_bid = round(price_bid + 0.00000001, 8)

    buy = client.buyLimit("XKR/USDT", amount, my_bid)
    sell = client.sellLimit("XKR/USDT", amount, my_ask)

    # The methods that will buy and sell.
    try:
        if spread > 0.000010:
            print(buy)
        else:
            print("Trade not succesfull.")
    except:
        print("Not successfull, trying again")
    try:
        if spread > 0.000010:
            print(sell)
        else:
            print("Trade not succesfull.")
    except:
        print("Not successfull, trying again")

    # Return uuid's of buy and sell orders
    try:
        buy_uuid = buy.result["uuid"]
        sell_uuid = sell.result["uuid"]
    except:
        print("No uuid's!")
        return None, None
    return buy_uuid, sell_uuid

def cancel_orders(buy_uuid, sell_uuid):

   # Cancels all open orders.
    cancelsleep = int(1)
    time.sleep(cancelsleep)
    print("Sleeping for " + str(cancelsleep) + "s")

    try:
        print(client.cancel(buy_uuid))
        print("Canceling buy order 🗙 ")
    except:
        print("Error canceling buy order, trying again")
    try:
        print(client.cancel(sell_uuid))
        print("Canceling sell order 🗙 ")
    except:
        print("Error canceling sell order, trying again")
    try:
        print(client.cancel(buy_uuid))
        print("Canceling buy order 🗙 " )
    except:
        print("Error canceling buy order, trying again")

    time.sleep(cancelsleep)
    print("Sleeping for " + str(cancelsleep) + "s")

    try:
        print(client.cancel(sell_uuid))
        print("Canceling sell order 🗙 " )
    except:
        print("Error canceling sell order, trying again")

    # Check if orders were successfully canceled
    buy_order_canceled = False
    sell_order_canceled = False
    while not buy_order_canceled or not sell_order_canceled:
        buy_order_info = client.getOrder(buy_uuid)
        sell_order_info = client.getOrder(sell_uuid)
        if buy_order_info.result["IsOpen"] == False:
            buy_order_canceled = True
        if sell_order_info.result["IsOpen"] == False:
            sell_order_canceled = True
        time.sleep(cancelsleep)

def main():
    os.system("clear")
    buy_uuid, sell_uuid = trade()
    cancel_orders(buy_uuid, sell_uuid)
while True:
    main()

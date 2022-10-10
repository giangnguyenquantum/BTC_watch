import telegram_send
from binance.client import Client
from datetime import datetime
import personal_function as pf
import websocket, json
from binance.enums import *
from datetime import datetime, timezone, timedelta

config_telegram='BTCUSDT_watch.conf'

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    time= json_message['E']
    is_candle_closed = candle['x']
    close_price = candle['c']
    time=int(time/1000)
    time=(datetime.fromtimestamp(time,time_zone).strftime('%Y-%m-%d %H:%M:%S'))
    if is_candle_closed:
        telegram_send.send(messages=['BTCUSDT at {}: {:.2f}.'.format(time,float(close_price))],conf=config_telegram)
        with open("results.txt", "a") as f:
            f.write('BTCUSDT at {}: {:.2f}.\n'.format(time,float(close_price)))  

#main
open("results.txt", "w").close()
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"
client=pf.client()
time_zone = timezone(timedelta(hours=8))
open("results.txt", "w").close()
telegram_send.send(messages=['Hello, This is the BTCUSDT watch bot.'],conf=config_telegram)
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
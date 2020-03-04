import json
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk
import urllib.request

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.animation as animation
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.ticker as mticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

style.use('ggplot')

f = plt.figure()

TITLE_FONT = ("Helvetica", 11)

NORM_FONT = ("Helvetica", 10)

DataPace = '1d'
paneCount = 1
chartLoad = True
refreshRate = 2000
resampleSize = '15Min'
candleWidth = .008
exchange = 'BTC-e'
programName = 'btce'
topIndicator = "none"
bottomIndicator = "none"
middleIndicators = "none"
EMAs = []
SMAs = []

darkColor = '#183A54'
lightColor = '#00A3E0'


DatCounter = 9000


def popupmsg(msg):
    popup = tk.Tk()
    def leavemini():
       popup.destroy()

    popup.wm_title("!")
       
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text = "Okay", command = leavemini)
    B1.pack()

    popup.mainloop()
    
    

def addTopIndicator(what):
    global topIndicator
    global DatCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available, choose 1 minute tf if you want short term.")

    if what == "none":
        topIndicator = what
        DatCounter = 9000

    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text="Choose how many periods you want each RSI calculation to consider.\nThese periods are contingent on your current time settings on the chart. 1 period = 1 OHLC candlestick.", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)
            topIndicator = group
            DatCounter = 9000
            print("set top indicator to",group)
            rsiQ.destroy()
        
        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()

        tk.mainloop()

    elif what == "macd":
        topIndicator = "macd"
        DatCounter = 9000


def addMiddleIndicator(what):
    global middleIndicators
    global DatCounter
    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available, choose 1 minute tf if you want short term.")

    if what != "none":
        if middleIndicators == "none":

            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want each SMA calculation to consider.\nThese periods are contingent on your current time settings on the chart.\n1 period = 1 OHLC candlestick.", font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()
                def callback():
                    middleIndicators = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter = 9000
                    print("mid indicator",middleIndicators)
                    midIQ.destroy()
                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()
                
            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want each EMA calculation to consider.\nThese periods are contingent on your current time settings on the chart.\n1 period = 1 OHLC candlestick.", font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()
                def callback():
                    middleIndicators = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter = 9000
                    print("mid indicator",middleIndicators)
                    midIQ.destroy()
                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()


        else:
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want each SMA calculation to consider.\nThese periods are contingent on your current time settings on the chart.\n1 period = 1 OHLC candlestick.", font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()
                def callback():
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter = 9000
                    print("mid indicator",middleIndicators)
                    midIQ.destroy()
                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want each EMA calculation to consider.\nThese periods are contingent on your current time settings on the chart.\n1 period = 1 OHLC candlestick.", font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()
                def callback():
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter = 9000
                    print("mid indicator",middleIndicators)
                    midIQ.destroy()
                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()
    else:
        middleIndicators = "none"
        
            


def addBottomIndicator(what):
    global bottomIndicator
    global DatCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available, choose 1 minute tf if you want short term.")

    if what == "none":
        bottomIndicator = what
        DatCounter = 9000

    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text="Choose how many periods you want each RSI calculation to consider.\nThese periods are contingent on your current time settings on the chart. 1 period = 1 OHLC candlestick.", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)
            bottomIndicator = group
            DatCounter = 9000
            print("set top indicator to",group)
            rsiQ.destroy()
        
        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()

        tk.mainloop()

    elif what == "macd":
        bottomIndicator = "macd"
        DatCounter = 9000





def tutorial():
    def leavemini(what):
       what.destroy()

    def page2():
        leavemini(tut)
        tut2 = tk.Tk()
        def leavemini2(what):
           what.destroy()
           
        def page3():

            leavemini2(tut2)
            tut3 = tk.Tk()
            tut3.wm_title("part 3!")
    
            label = ttk.Label(tut3, text="Part 3", font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(tut3, text = "Done!", command = tut3.destroy)
            B1.pack()
            tut3.mainloop()
            


        tut2.wm_title("part 2!") #to be done
       
        label = ttk.Label(tut2, text="Part 2", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(tut2, text = "next!", command = page3)
        B1.pack()

        tut.mainloop()
        
        
    tut = tk.Tk()
    tut.wm_title("Tutorial")
    label = ttk.Label(tut, text="What do you need help with?", font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(tut, text = "Overview of the application", command = page2)
    B1.pack()

    B2 = ttk.Button(tut, text = "How do I trade here?", command=lambda: popupmsg('Not supported just yet!'))
    B2.pack()

    B3 = ttk.Button(tut, text = "Indicator questions/help", command=lambda: popupmsg('Not supported just yet!'))
    B3.pack()

    tut.mainloop()
    

def changeSampleSize(size,width):
    global resampleSize
    global DatCounter
    global candleWidth

    if DataPace == '7d' and size == '1Min':
        popupmsg("Too much data chosen, choose a smaller Data Time Frame or higher OHLC Interval!")
        
    if DataPace == 'tick':
        popupmsg("You are currently viewing tick data, not OHLC. Choose a larger Data Time Frame!")
        
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width

def changeExchange(toWhat,pn):
    global exchange
    global DatCounter
    global programName
    exchange = toWhat
    programName = pn
    DatCounter = 9000

def changeTimeFrame(tf):
    global DataPace
    global DatCounter
    if tf == '7d' and resampleSize == '1Min':
        popupmsg("Too much data chosen, choose a smaller data time frame or higher OHLC Interval!")
    else:
        DataPace = tf
        DatCounter = 9000
    
def loadChart(run):
    global chartLoad

    if run == 'start':
        chartLoad = True
    elif run == 'stop':
        chartLoad = False
        
def quit():
    quit()

        
def animate(i):
    global refreshRate
    global DatCounter



    def moving_average(x, n, type='simple'):

        x = np.asarray(x)
        if type=='simple':
            weights = np.ones(n)
        else:
            weights = np.exp(np.linspace(-1., 0., n))

        weights /= weights.sum()


        a =  np.convolve(x, weights, mode='full')[:len(x)]
        a[:n] = a[n]
        return a



        
    print(exchange)

    if chartLoad:
        if paneCount == 1:
            if DataPace == 'tick':
                try:
                    if exchange == 'BTC-e':
                        a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex = a)
                        
                        dataLink = 'https://btc-e.com/api/3/trades/btc_usd?limit=2000'

                        data = urllib.request.urlopen(dataLink)
                        data = data.readall().decode('utf-8')
                        data = json.loads(data)
                        data = data["btc_usd"]
                        data = pd.DataFrame(data)

                        

                        data["datestamp"] = np.array(data['timestamp']).astype('datetime64[s]')
                        allDates = data["datestamp"].tolist()

                        buys = data[(data['type']=='bid')]
                        #buys["datestamp"] = np.array(buys['timestamp']).astype('datetime64[s]')
                        buyDates = (buys["datestamp"]).tolist()

                        sells = data[(data['type']=='ask')]
                        #sells["datestamp"] = np.array(sells['timestamp']).astype('datetime64[s]')
                        sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"]
                        
                        a.clear()
                        
                        a.plot_date(buyDates,buys["price"], '#00A3E0', label ="buys")
                        a.plot_date(sellDates,sells["price"], '#183A54', label = "sells")
                        a2.fill_between(allDates,0, volume, facecolor='#183A54')
                        a.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                           ncol=2, borderaxespad=0.)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
                        plt.setp(a.get_xticklabels(), visible=False)
                        
                        title = exchange+' Tick Data\nLast Price: '+str(data["price"][0])
                        a.set_title(title)
                        priceData = data["price"].apply(float).tolist()


                        
                    if exchange == 'Bitstamp':
                        a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex = a)

                        dataLink = 'https://www.bitstamp.net/api/transactions/'
                        data = urllib.request.urlopen(dataLink)
                        data = data.readall().decode('utf-8')
                        data = json.loads(data)
                        data = pd.DataFrame(data)
                        data["datestamp"] = np.array(data['date'].apply(int)).astype('datetime64[s]')
                        datestamps = data["datestamp"].tolist()
                        volume = data["amount"].apply(float).tolist()

                        a.clear()

                        a.plot_date(datestamps,data["price"], '#183A54')


                        a2.fill_between(datestamps,0, volume, facecolor='#183A54')


                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
                        plt.setp(a.get_xticklabels(), visible=False)
                        
                        title = exchange+' Tick Data\nLast Price: '+str(data["price"][0])
                        a.set_title(title)
                        priceData = data["price"].apply(float).tolist()


                    if exchange == 'Bitfinex':
                        a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex = a)
                        
                        dataLink = 'https://api.bitfinex.com/v1/trades/btcusd?limit=2000'

                        data = urllib.request.urlopen(dataLink)
                        data = data.readall().decode('utf-8')
                        data = json.loads(data)
                        data = pd.DataFrame(data)
                        
                        volume = data["amount"].apply(float).tolist()

                        #print(data)

                        data["datestamp"] = np.array(data['timestamp']).astype('datetime64[s]')
                        allDates = data["datestamp"].tolist()

                        buys = data[(data['type']=='buy')]
                        #buys["datestamp"] = np.array(buys['timestamp']).astype('datetime64[s]')
                        buyDates = (buys["datestamp"]).tolist()

                        sells = data[(data['type']=='sell')]
                        #sells["datestamp"] = np.array(sells['timestamp']).astype('datetime64[s]')
                        sellDates = (sells["datestamp"]).tolist()

                        a.clear()
                        
                        
                        a.plot_date(buyDates,buys["price"], lightColor, label ="buys")
                        a.plot_date(sellDates,sells["price"], darkColor, label = "sells")
                        a2.fill_between(allDates,0, volume, facecolor='#183A54')


                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
                        plt.setp(a.get_xticklabels(), visible=False)
                        a.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                           ncol=2, borderaxespad=0.)
                        
                        title = exchange+' Tick Data\nLast Price: '+str(data["price"][0])
                        a.set_title(title)
                        priceData = data["price"].apply(float).tolist()

                    if exchange == 'Huobi':
                        try:
                            a = plt.subplot2grid((6,4), (0,0), rowspan=6, colspan=4)

                            data = urllib.request.urlopen('#newSourceOfData'+programName).read()
                            
                            data = str(data).replace('b','').replace("'",'')
                            data = json.loads(data)

                            

                            dateStamp = np.array(data[0]).astype('datetime64[s]')
                            dateStamp = dateStamp.tolist()
                            print('here')

                            df = pd.DataFrame({'Datetime':dateStamp})

                            
                            
                            
                            df['Price'] = data[1]
                            
                            df['Volume'] = data[2]
                            df['Symbol'] = "BTCUSD"
                            df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                            df = df.set_index('Datetime')
                            lastPrice = df['Price'][-1]

                            a.plot_date(df['MPLDate'][-4500:],df['Price'][-4500:], lightColor, label ="price")

                            a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                            a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

                            
                            title = exchange+' Tick Data\nLast Price: '+str(lastPrice)
                            a.set_title(title)
                            priceData = df['Price'].apply(float).tolist()
                        except Exception as e:
                            print(str(e))
                  
                except:
                    DatCounter = 9000
###### BEGIN NON-TICK GRAPHING#################################################################################    

            else:

                if DatCounter > 12:
                    try:
                        if exchange == 'Huobi':
                            if topIndicator != "none":

                                a = plt.subplot2grid((6,4), (1,0), rowspan=5, colspan=4)
                                a0 = plt.subplot2grid((6,4), (0,0), sharex=a, rowspan=1, colspan=4)
                            else:
                                a = plt.subplot2grid((6,4), (0,0), rowspan=6, colspan=4)

                        else:
                            if topIndicator != "none" and bottomIndicator != "none":
                                # actual price chart. 
                                a = plt.subplot2grid((6,4), (1,0), rowspan=3, colspan=4)
                                # volume!
                                a2 = plt.subplot2grid((6,4), (4,0), sharex=a, rowspan=1, colspan=4)
                                # top indicator
                                a0 = plt.subplot2grid((6,4), (0,0), sharex=a, rowspan=1, colspan=4)
                                # bottom indicator
                                a3 = plt.subplot2grid((6,4), (5,0), sharex=a, rowspan=1, colspan=4)
                                
                            elif topIndicator != "none":
                                a = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
                                a2 = plt.subplot2grid((6,4), (5,0), sharex=a, rowspan=1, colspan=4)
                                a0 = plt.subplot2grid((6,4), (0,0), sharex=a, rowspan=1, colspan=4)
                            elif bottomIndicator != "none":
                                a = plt.subplot2grid((6,4), (0,0), rowspan=4, colspan=4)
                                a2 = plt.subplot2grid((6,4), (4,0), sharex=a, rowspan=1, colspan=4)
                                #a0 = plt.subplot2grid((6,4), (0,0), sharex=a, rowspan=1, colspan=4)
                                a3 = plt.subplot2grid((6,4), (5,0), sharex=a, rowspan=1, colspan=4)

                            else:
                                a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
                                a2 = plt.subplot2grid((6,4), (5,0), sharex=a, rowspan=1, colspan=4)
                                
                                
                            
                        print('#newSourceOfData'+DataPace+'&exchange='+programName)
                        data = urllib.request.urlopen('#newSourceOfData'+DataPace+'&exchange='+programName).read()




                            
                        data = str(data).replace('b','').replace("'",'')
                        data = json.loads(data)

                        dateStamp = np.array(data[0]).astype('datetime64[s]')
                        dateStamp = dateStamp.tolist()

                        df = pd.DataFrame({'Datetime':dateStamp})
                        df['Price'] = data[1]
                        df['Volume'] = data[2]
                        df['Symbol'] = "BTCUSD"
                        df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                        df = df.set_index('Datetime')


                        OHLC =  df['Price'].resample(resampleSize, how='ohlc')
                        OHLC = OHLC.dropna() 

                        volumeData = df['Volume'].resample(resampleSize, how={'volume':'sum'})

                        OHLC['dateCopy'] = OHLC.index
                        OHLC['MPLDates'] = OHLC['dateCopy'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                        del OHLC['dateCopy']

                        volumeData['dateCopy'] = volumeData.index
                        volumeData['MPLDates'] = volumeData['dateCopy'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                        del volumeData['dateCopy']


                        priceData = OHLC['close'].apply(float).tolist()

                        

                                
                        
                        

                        a.clear()
                        if middleIndicators != "none":
                            for eachMA in middleIndicators:
                                ewma = pd.stats.moments.ewma
                                #print("type:",eachMA[0],"periods:",eachMA[1])
                                if eachMA[0] == "sma":
                                    sma = pd.rolling_mean(OHLC["close"],eachMA[1])
                                    label = str(eachMA[1])+" SMA"
                                    a.plot(OHLC['MPLDates'],sma, label=label)
                                if eachMA[0] == "ema":
                                    ewma = pd.stats.moments.ewma
                                    label = str(eachMA[1])+" EMA"
                                    a.plot(OHLC['MPLDates'],ewma(OHLC["close"], eachMA[1]), label=label)


                            #a.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                            #   ncol=2, borderaxespad=0.)

                            a.legend(loc=0)

                                    

                        if topIndicator[0] == "rsi":
                            rsiIndicator(priceData,"top")
                        elif topIndicator == "macd":
                            try:
                                computeMACD(priceData,location="top")
                            except:
                                print("failed macd")
                            


                            
                        if bottomIndicator[0] == "rsi":
                            rsiIndicator(priceData,"bottom")
                        elif bottomIndicator == "macd":
                            try:
                                computeMACD(priceData,location="bottom")
                            except:
                                print("failed macd")

                        
                            

                        
                        
                        csticks = candlestick_ohlc(a, OHLC[['MPLDates', 'open', 'high', 'low', 'close']].values, width=candleWidth, colorup=lightColor, colordown=darkColor)
                        a.set_ylabel("price")
                        if exchange != 'Huobi':
                            a2.fill_between(volumeData['MPLDates'],0, volumeData['volume'], facecolor='#183A54')#, alpha=.4)
                            a2.set_ylabel("volume")

                        
                        a.xaxis.set_major_locator(mticker.MaxNLocator(3))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

                        plt.setp(a.get_xticklabels(), visible=False)
                        
                        if topIndicator != "none":  
                            plt.setp(a0.get_xticklabels(), visible=False)

                        if bottomIndicator != "none":  
                            plt.setp(a2.get_xticklabels(), visible=False)

                        x = (len(OHLC['close']))-1

                        if DataPace == '1d':
                            title = exchange+' 1 Day Data with '+resampleSize+' Bars\nLast Price: '+str(OHLC['close'][x])
                        if DataPace == '3d':
                            title = exchange+' 3 Day Data with '+resampleSize+' Bars\nLast Price: '+str(OHLC['close'][x])
                        if DataPace == '7d':
                            title = exchange+' 7 Day Data with '+resampleSize+' Bars\nLast Price: '+str(OHLC['close'][x])


                        if topIndicator != "none":  
                            a0.set_title(title)
                        else:
                            a.set_title(title)
                        print('NewGraph!')
                        
                        DatCounter = 0



                        
                        



                        
                    except Exception as e:
                        print(str(e),"main animate non tick")
                        DatCounter = 9000
                        
                else:
                    DatCounter += 1


                

class AndyBTCTradingApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        

        tk.Tk.__init__(self, *args, **kwargs)
        
        #menubar = tk.Menu(tk.Tk)

        style = ttk.Style()
        style.layout("Button", [
           ("Menubutton.background", None),
           ("Menubutton.foreground", None),
           ("Menubutton.button", {"children":
               [("Menubutton.focus", {"children":
                   [("Menubutton.padding", {"children":
                       [("Menubutton.label", {"side": "left", "expand": 1})]
                   })]
               })]
           }),
        ])

        style.layout("TMenubutton", [
           ("Menubutton.background", None),
           ("Menubutton.button", {"children":
               [("Menubutton.focus", {"children":
                   [("Menubutton.padding", {"children":
                       [("Menubutton.label", {"side": "left", "expand": 1})]
                   })]
               })]
           }),
        ])
        
        

        container = tk.Frame(self, width=1280, height=720)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg('Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=tutorial)
        menubar.add_cascade(label="Help", menu=helpmenu)

        
        tk.Tk.config(self, menu=menubar)


        self.frames = {}
        for F in (StartPage, dashboard):
            frame = F(container, self)
            self.frames[F] = frame
            # put all of the pages in the same location; 
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        try:
            tk.Tk.iconbitmap(self,default='clienticon.ico')
            tk.Tk.wm_title(self, "Andy Bitcoin Trading Client")
        except Exception as e:
            print(str(e))

    def show_frame(self, c):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="""Andy Bitcoin Client was developed in order to help and support traders. Developer of this app do not take any responsibility for loss of money, data or any kind of damage that might occur as a result of using this software. You agree to use it on your own responsibility.""", font=TITLE_FONT)


        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="Agree", 
                            command=lambda: controller.show_frame(dashboard))
        button2 = ttk.Button(self, text="Disagree",
                            command=quit)
        button1.pack()
        button2.pack()

class dashboard(tk.Frame):

    def __init__(self, parent, controller):
        

        
        tk.Frame.__init__(self, parent)

        # title and leading text #
        label = tk.Label(self, text="Dashboard", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        # setting up the frame #
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk( canvas, self )
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        mb=  ttk.Menubutton ( self, text="Resume/Pause Updates")
        mb.menu  =  tk.Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
        mb.menu.add_command ( label="Resume",
                                  command=lambda: loadChart('start'))
        mb.menu.add_command ( label="Pause",
                                  command=lambda: loadChart('stop'))
        mb.pack(side='right')
        

        mb=  ttk.Menubutton ( self, text="Exchange")
        mb.menu  =  tk.Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
        mb.menu.add_command ( label="BTC-e",
                                  command=lambda: changeExchange('BTC-e','btce') )
        mb.menu.add_command ( label="Bitfinex",
                                  command=lambda: changeExchange('Bitfinex','bitfinex') )
        mb.menu.add_command ( label="Bitstamp",
                                  command=lambda: changeExchange('Bitstamp','bitstamp') )
        mb.menu.add_command ( label="Huobi",
                                  command=lambda: changeExchange('Huobi','huobi') )
        mb.pack(side='left')
        

        mb=  ttk.Menubutton ( self, text="Data Time Frame")
        mb.menu  =  tk.Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
        mb.menu.add_command ( label="Tick",
                                  command=lambda: changeTimeFrame('tick') )
        mb.menu.add_command ( label="1 day",
                                  command=lambda: changeTimeFrame('1d') )
        mb.menu.add_command ( label="3 day",
                                  command=lambda: changeTimeFrame('3d') )
        mb.menu.add_command ( label="1 Week",
                                  command=lambda: changeTimeFrame('7d') )
        mb.pack(side='left')


        mb=  ttk.Menubutton ( self, text="OHLC Interval")
        mb.menu  =  tk.Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
        mb.menu.add_command ( label="Tick",
                                  command=lambda: changeTimeFrame('tick') )
        mb.menu.add_command ( label="1 minute",
                                  command=lambda: changeSampleSize('1Min',0.0005) )
        mb.menu.add_command ( label="5 minute",
                                  command=lambda: changeSampleSize('5Min',0.003) )
        mb.menu.add_command ( label="15 minute",
                                  command=lambda: changeSampleSize('15Min',0.008) )
        mb.menu.add_command ( label="30 minute",
                                  command=lambda: changeSampleSize('30Min',0.016) )
        mb.menu.add_command ( label="1 Hour",
                                  command=lambda: changeSampleSize('1H',0.032) )
        mb.menu.add_command ( label="3 Hour",
                                  command=lambda: changeSampleSize('3H',0.096) )

        
        mb.pack(side='left')


        mb=  ttk.Menubutton ( self, text="Top Indicator")
        mb.menu  =  tk.Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
        mb.menu.add_command ( label="None",
                                  command=lambda: addTopIndicator('none'))
        mb.menu.add_command ( label="RSI",
                                  command=lambda: addTopIndicator('rsi'))
        mb.menu.add_command ( label="MACD",
                                  command=lambda: addTopIndicator('macd'))
        mb.pack(side='left')

        mb=  ttk.Menubutton ( self, text="Main Graph Indicator")
        mb.menu  =  tk.Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
        mb.menu.add_command ( label="None",
                                  command=lambda: addMiddleIndicator('none'))
        mb.menu.add_command ( label="SMA",
                                  command=lambda: addMiddleIndicator('sma'))
        mb.menu.add_command ( label="EMA",
                                  command=lambda: addMiddleIndicator('ema'))

        mb.pack(side='left')

        mb=  ttk.Menubutton ( self, text="Bottom Indicator")
        mb.menu  =  tk.Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
        mb.menu.add_command ( label="None",
                                  command=lambda: addBottomIndicator('none'))
        mb.menu.add_command ( label="RSI",
                                  command=lambda: addBottomIndicator('rsi'))
        mb.menu.add_command ( label="MACD",
                                  command=lambda: addBottomIndicator('macd'))
        mb.pack(side='left')



if __name__ == "__main__":

    

    
    app = AndyBTCTradingApp()
    app.geometry("1600x900")
    ani = animation.FuncAnimation(f,animate, interval=refreshRate)
    # create a toplevel menu
    app.mainloop()


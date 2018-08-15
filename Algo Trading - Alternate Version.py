#Algorithmic Trading with Machine Learning
# - Using Analysis of Highs Lows and Trading Volume

#imports
from time import *
from sklearn import tree
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
# pandas_datareader is not compatible with newest pandas version. below line is inserted to avoid the issue 
pd.core.common.is_list_like = pd.api.types.is_list_like 
import pandas_datareader.data as web
import time
start_time = time.time()
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
from models import HLV_tree
algo = HLV_tree    


#fields    
acc = 20
Points = []
Highs = []
Lows = []
Volumes = []
dates = []
CashRecords = []
hold = []
nohold = []

Cash = 100
Bought = False
days = 0
decision = 0
stockSymbol = 'AAPL'

style.use('ggplot')
start = dt.datetime(2015,1,1)
end = dt.datetime(2017,12,31)

#importing data from iex (investors exchange)
df = web.DataReader(stockSymbol,'iex',start,end)
#to save data file in same folder 
import os
dir_path = os.path.dirname(os.path.realpath(__file__)) 
datafile = os.path.join(dir_path, 'data.csv')
resultsfile = os.path.join(dir_path, 'results.csv')
df.to_csv(datafile)

df = pd.read_csv(datafile, parse_dates = True)

for i in df[['close']]:
    for j in df[i]:
        Points.append(round(j,2))
        
for i in df[['high']]:
    for j in df[i]:
        Highs.append(round(j,2))

for i in df[['low']]:
    for j in df[i]:
        Lows.append(round(j,2))
        
for i in df[['volume']]:
    for j in df[i]:
        Volumes.append(round(j,2))

for i in df[['date']]:
    for j in df[i]:
        dates.append(dt.datetime.strptime(j, "%Y-%m-%d"))
        

#graph labels        
plt.figure(num = stockSymbol)
plt.title(stockSymbol + " Stock Algorithmic Trading Analysis")
plt.xlabel('Date')
plt.ylabel('Stock Price / Cash')

while days <= len(df[['close']]) - 1:
    
    #stock info
    days += 1
    StockPrice = Points[days - 1]
    
    if days == 1:
        initP = StockPrice
        initC = Cash
        
    #your money
    if Bought == True:
        Cash = round(Cash*StockPrice/Points[days-2],2)
        c = "green"
        hold.append(Points[days-1])
        nohold.append(0)
    else:
        c = "red"
        hold.append(0)
        nohold.append(Points[days-1])
                  
    CashRecords.append(Cash)
    
    if days > acc:
        decision = algo(Points[:days],Highs[:days],Lows[:days],Volumes[:days],acc)

    if Bought == True:
        if decision == 0:
            Bought = False
    else:
        if decision == 1:
            Bought = True

    
    plt.plot(dates[days - 2:days], Points[days - 2:days], color=c)

results = pd.DataFrame({'Date':dates,'Hold': hold, 'Nohold':nohold, 'Cash':CashRecords})
results.to_csv(resultsfile)
    
print("Ending Cash: " + str(CashRecords[-1]))
print("Expected Cash: " + str(round(CashRecords[0] * Points[-1] / Points[0],2)))
print("Performance: " + str(round(100 * CashRecords[-1] * Points[0] / (Points[-1] * CashRecords[0]),2)) + "%")

plt.plot(dates, CashRecords, color='blue')
plt.show()



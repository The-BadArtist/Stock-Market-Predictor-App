import pandas as pd
import yfinance as yf
import os, time
from datetime import date, timedelta
from statistics import mode
import shutil

today = date.today()
one_day_ago = today - timedelta(days = 1)
five_days_ago = today - timedelta(days = 5)
three_months_ago = today - timedelta(days = 90)
five_years_ago = today - timedelta(days = 365 * 5)
one_year_ago = today - timedelta(days =365)




# This function allows for the execution of multiple function hints the name junction
def junction_function(ticker):
    historical_data5Y = yf.download(ticker, start=five_years_ago, end=today)
    historical_dataYTD = yf.download(ticker, period="ytd", interval="1d", start=one_year_ago, end=today)
    historical_data3M = yf.download(ticker, start=three_months_ago, end=today)
    historical_data5D = yf.download(ticker, period="5d", interval="5m", start=five_days_ago, end=today)
    real_time_data = yf.download(ticker, start=one_day_ago, end=today)

    #Creates and Organized the CSV Files Into Folders
    directory = "CSV"
    subdirectory = ticker
    fullpath = f"{directory}/{subdirectory}"

    # Checks for existance of directories and removes and add current csv
    if os.path.exists(fullpath) == False:
        os.makedirs(fullpath)
    elif os.path.exists(fullpath) == True:
        shutil.rmtree(fullpath)
        os.makedirs(fullpath)
    
    # Save the data to a CSV file
    historical_data5Y.to_csv(f"{fullpath}/{ticker}_5Y.csv")
    historical_dataYTD.to_csv(f"{fullpath}/{ticker}_YTD.csv")
    historical_data3M.to_csv(f"{fullpath}/{ticker}_3M.csv")
    historical_data5D.to_csv(f"{fullpath}/{ticker}_5D.csv")

    
    dataset_1 = prediction_model(historical_data5Y)
    dataset_2 = prediction_model(historical_dataYTD)
    dataset_3 = prediction_model(historical_data3M)
    dataset_4 = prediction_model(historical_data5D)
    dataset_5 = prediction_model(real_time_data)

    # os.system('cls')

    # print("\n\n############### Stock Information ###############\n")
    
    # print("\n--------- Current Stock Information ---------\n")
    current_price = display_stock_info(real_time_data)
    # # display_stock_info(historical_data5D)

    # print("\n-------------- Call-to-Action ---------------\n")

    # print("Action: ", mode([dataset_1[0], dataset_2[0], dataset_3[0], dataset_4[0], dataset_5[0]]))
    # print("Trend: ", mode([dataset_1[1], dataset_2[1], dataset_3[1], dataset_4[1], dataset_5[1]]))


    # print("\n\n")
    predicted_action = mode([dataset_1[0], dataset_2[0], dataset_3[0], dataset_4[0], dataset_5[0]])
    predicted_trend = mode([dataset_1[1], dataset_2[1], dataset_3[1], dataset_4[1], dataset_5[1]])
    print([dataset_1[1], dataset_2[1], dataset_3[1], dataset_4[1], dataset_5[1]])
    print([dataset_1[0], dataset_2[0], dataset_3[0], dataset_4[0], dataset_5[0]])

    return predicted_action, predicted_trend, current_price, historical_dataYTD


def prediction_model(data):
    
    # Define short-term and long-term window sizes for SMA
    short_window = 50
    long_window = 200

    # Calculate moving averages
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

    # Simulate buy/sell signals based on SMA crossover and predicts the trend based on the candles set
    data['Signal'] = 0  # 0: Hold, 1: Buy, -1: Sell
    for i in range(len(data)):
        if data.loc[data.index[i], 'SMA_short'] > data.loc[data.index[i], 'SMA_long'] and data.loc[data.index[i-1], 'Signal'] != 1:
            data.loc[data.index[i], 'Signal'] = 1  # Buy signal
        elif data.loc[data.index[i], 'SMA_short'] < data.loc[data.index[i], 'SMA_long'] and data.loc[data.index[i-1], 'Signal'] != -1:
            data.loc[data.index[i], 'Signal'] = -1  # Sell signal

        # Predicts the trend of the market based on the SMA crossover and datasets given.
        if data.loc[data.index[-1], "SMA_short"] > data.loc[data.index[-1], "SMA_long"]:
            trend = "Upward"
        elif data.loc[data.index[-1], "SMA_short"] < data.loc[data.index[-1], "SMA_long"]:
            trend = "Downward"
        else:
            trend = "Neutral"

    '''
    Based on the average signal, the variable 'value' will be assigned an action
    1 = Buy
    0 = Hold
    -1 = Sell
    ''' 
    value = data['Signal'].mean()
    if value > 0:
        action = "Buy"
    elif value == 0:
        action = "Hold"
    else:
        action = "Sell"
    


    return action, trend

def display_stock_info(data):
    """Displays basic stock information such as current price, change, opening price, 
    and 52-week high/low.

    Args:
        data (pandas.DataFrame): The DataFrame containing stock data.
    """
    # print("Current Price:", data.loc[data.index[-1], 'Close'])
    # print("Opening Price:", data.loc[data.index[-1], 'Open'])
    # print("52-Week High:", data["High"].max())
    # print("52-Week Low:", data["Low"].min())
    current_price = data.loc[data.index[-1], 'Close']

    #   print(data)
    return current_price

def update_info(ticker):
        data = junction_function(ticker)
        action = data[0]
        trends = data[1]
        current_price = data[2]
        real_time = data[3]
        return action, trends, current_price, real_time
    


def main():
    ticker = input("Enter a ticker: ")

    update_info(ticker)


    




if __name__ == "__main__":
    main()
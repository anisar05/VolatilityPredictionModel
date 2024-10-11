from datetime import date
import pandas_datareader.data as web
from datetime import datetime, timedelta
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from arch import arch_model
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import numpy as np
import yfinance as yf

matplotlib.use('Agg')



def garch_model():
    #Yahoo Finance - Barcalys
    today = date.today()
    start_date = "2015-01-01"
    end_date = today

    barcalys = yf.download('BCS', start = start_date, end = end_date)
    returns = 100*barcalys['Close'].pct_change().dropna()
    plt.figure(figsize=(10,4))
    plt.plot(returns)
    # plt.show()

    plot_pacf((returns**2))
    # plt.show()

    #Can also utilize lag 1 in terms of significance
    model = arch_model(returns, p = 2, q = 2)
    model_fit = model.fit()
    print(model_fit.summary())

    #Rolling Forecast - Volatility Reading
    roll_predictions = []
    size = 365

    for i in range(size):
        train = returns[:-(size-i)]
        model = arch_model(train, p = 2, q = 2)
        model_fit = model.fit(disp = 'off')
        prediction_model = model_fit.forecast(horizon = 1)
        roll_predictions.append(np.sqrt(prediction_model.variance.values[-1,:][0]))

    roll_predictions = pd.Series(roll_predictions, index = returns.index[-365:])
    plt.figure(figsize=(10,4))
    true, = plt.plot(returns[-365:])
    predictors, = plt.plot(roll_predictions)
    # plt.show()

    plt.savefig('static/barclays_stock.png')
    plt.close()

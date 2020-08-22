# This file is for the current COVID-19 situation. 
# This does not show the predicted logisitic regression path, but the predicted peak
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from datetime import date

def logistic_function(x, a=1, b=0, c=1, d=0):
    return a / (1 + np.exp(-c * (x - d))) + b


def exponential_function(x, a=1, b=0, c=0, d=0):
    return a * np.exp(c * (x + d)) + b


def fit_data_to_function(
    x, y, function, plot=True, initial_guess=[1, 1, 1, 1]
):

    params, _ = curve_fit(function, x, y, p0=initial_guess)
    plt.figure(figsize=(16,9))
    plt.plot(x, y, ".", label="Reported cases")
    y_fit = function(x, *params)
    print(r2_score(y, y_fit))
    if plot:
        plt.plot(x, y_fit, linewidth=2,label="Fitted curve")
        plt.xlabel("Days since first confirmed case",size=18)
        plt.ylabel("Cases",size=18)
        plt.grid()
        plt.legend()
        plt.show()
    return params


def daily_increase(data):
    d = []
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i]-data[i-1])
    return d


def plateau(x, y, params, function, diff=10):
    confirmed_now = y[-1]
    confirmed_then = y[-2]
    days = 0
    now = x[-1]
    cases_added = []
    while confirmed_now - confirmed_then > diff:
        days += 1
        confirmed_then = confirmed_now
        confirmed_now = function(now + days, *params)
        cases_added.append(confirmed_now)

    return days, confirmed_now, cases_added


def bell_curve(data1,data2):
  y_inc = daily_increase(data1)
  data2 = data2[1:]
  arr = pd.Series(data2)
  arr_ = pd.Series(y_inc)
  s = pd.concat([arr_, arr])
  plt.figure(figsize=(16,9))
  plt.bar(np.arange(len(s)),s)
  plt.axvline(x=len(arr_), color="red", label="Today")
  plt.xlabel("Days since first confirmed case",size=18)
  plt.ylabel("Daily confirmed cases",size=18)
  plt.legend()
  plt.show()
  return s

def load_deaths(data):
  df1 = df[df["location"]=='Colombia']
  deaths = df1[df1["total_deaths"] > 0]
  deaths = deaths["total_deaths"].values
  x_deaths = np.arange(len(deaths))
  plt.figure(figsize=(16,9))
  plt.plot(x_deaths,deaths,'r',linewidth=3)
  plt.grid()
  plt.xlabel('Days since first confirmed case',size=18)
  plt.ylabel('Number of deaths',size=18)
  plt.show()

df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
df1 = df[df["location"]=="Colombia"]
df2 = df1[df1["total_cases"] > 0]
cols = [1,4]
df2 = df2[df2.columns[cols]]
cases = df2["total_cases"].values
y = np.array(cases)
x = np.arange(len(y))

params = fit_data_to_function(
    x, y, logistic_function, initial_guess=[y[-1], 1, 1, 1]
)
diff=100

days, confirmed, cases_added = plateau(
    x, y, params, logistic_function, diff=diff
)
y_cummulative = daily_increase(cases_added)

peak_day = int(np.array(y_cummulative[1:]).argmax())
day_of_peak = (pd.to_datetime(date.today()) + pd.DateOffset(days=peak_day)).strftime('%Y-%m-%d')
#print(peak_day)
params_table = pd.DataFrame(data=params, index=['a','b','c','d'],columns=['Parameter value'])
if __name__ == "__main__":
    print(params)
    diff = 100
    print(f"{days} days until growth is less than {diff}")
    print(f"Number of cases will be {int(confirmed)}")

import streamlit as st
import pandas as pd
import numpy as np
import covid3
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns

st.title("Portafolio - Arturo Rey")
st.markdown("### Data Scientist")

st.sidebar.title("What project do you wish to see?")

select = st.sidebar.selectbox("Projects", ["COVID-19 en Colombia", "Analysing Mock Data","Video Game Analysis"], key="1")

if select == "COVID-19 en Colombia":
    st.markdown("The coronavirus are viruses that periodically surge in different parts of the world, and can cause respiratory diseases, that can be either mild, moderate or highly serious.")
    st.markdown("COVID-19 has been categorized by the WHO (World Health Organization) as a public health emergency of international concern. There have been confirmed cases in Colombia since March.")
    st.markdown("The virus can be transmitted through particles in the air, either by sneezing or coughing.")
    st.sidebar.markdown("You can see the following project:")
    slider = st.sidebar.slider("Number of cases for a specific date", 0,len(covid3.y)-1)
    st.markdown(f"### Number of confirmed cases in Colombia on day {slider}*.")
    st.write(int(covid3.y[slider]))
    if st.sidebar.checkbox("Show graph for current reported cases", True):
        st.markdown(f"### Current COVID-19 cases in Colombia as of {dt.datetime.today().strftime('%Y-%m-%d')}")
        st.markdown("The following curve is the number of confirmed cases through time. It has been fitted with a Logistic Regression function.")
        covid3.fit_data_to_function(covid3.x,covid3.y,covid3.logistic_function,initial_guess=[covid3.y[-1], 1, 1, 1])
        st.pyplot()
    if st.sidebar.checkbox("Show bell curve", True):
        st.markdown(f"### Current COVID-19 cases in Colombia")
        covid3.bell_curve(covid3.y, covid3.y_cummulative)
        st.pyplot()
        st.write(f'The estimated peak will be on {covid3.day_of_peak}')
    # if st.sidebar.checkbox("Show predicted cases via a Logistic Regression model", True):
    #     st.markdown(f"### Current Logistic Regression prediction for COVID-19 cases in Colombia")
    #     covid2.predicted_graph(covid2.x,covid2.y,covid2.logistic_function)
    #     st.pyplot()
    #     st.write("According to the logistic regression model shown above, Colombia will stop seeing more than 10 cases a day by the 200th day into the pandemic.")
    #     st.write("This model is defined by the following formula: ")
    st.write("Source: https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
    st.markdown(f"*{len(covid3.y)-1} days since the first case was confirmed in Colombia.")   
#     num = st.sidebar.slider("Number of days ahead to predict COVID-19 cases", 0,100)
#     st.sidebar.markdown(int(round(project1.cases_in_days(num))))
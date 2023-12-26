import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Path to the file in your github
file_path = "https://raw.githubusercontent.com/hafidzmf48/Dashboard_Bike_Sharing/main/day.csv"

# Read a CSV file using pandas
data = pd.read_csv(file_path, delimiter=',', encoding='utf-8', header=0)data['suhu'] = data['temp']*(39+8)+(-8)     #39 and -8 was declared as max and min of 'temp' variable
data['kelembaban'] = data['hum']*100        #100 was declared as max values of 'hum' variable
data['speed_angin'] = data['windspeed']*67  #67 was declared as max values of 'windspeed' variable
year_dict = {0 : 2011 , 1 : 2012}
data['yr'] = data['yr'].replace(year_dict)

st.set_option('deprecation.showPyplotGlobalUse', False)

with st.sidebar:
  st.write("**My Profile**")
  foto = 'https://drive.google.com/file/d/1M9FsJd6Ttzguf1B16DfYiLyU2C54ez-q/view?usp=sharing'
  st.image(foto)
  st.write('Hafidz Muhammad Fahri')
  st.write("""
           I am fresh graduate of statistics and have a passion of data visualization.
           Here i'm gonna test my skill by creating dashboard to analyze this dataset""")

#create title and header
st.title("Bike Sharing Data Analyze :bike:")
st.header("Dataset Quick Details", divider='blue')
st.write("""Bike-sharing rental process is highly correlated to the environmental and seasonal settings.
         For instance, weather conditions, precipitation, day of week, season, hour of the day, etc. can affect the rental behaviors.""")
st.subheader("Business Question", divider='blue')
st.write('1. How is the count of bike rent between 2 years?')
st.write('2. Is there any correlation between weather conditions and count of bike rent?')
st.subheader("Visual Analyze", divider='blue')

# create tabs that wiil contain various chart
tab1, tab2, tab3 = st.tabs(['2 year compare','Casual User','Registered User'])

with tab1 :
  st.header("Count of bikes each month between 2 years")
  group_yr = data.groupby(['mnth','yr']).sum().reset_index()
  plt.figure(figsize=(12, 6))
  sns.barplot(data=group_yr, x='mnth', y='cnt', hue='yr', palette='coolwarm')
  plt.xlabel('Months')
  plt.ylabel('Count of Bike Rent')
  plt.legend(title='Year')
  plt.tight_layout()
  st.pyplot()
    
  with st.expander("See explanation"):
    st.write("""
        The chart above shows that over all the count of bike rent in 2012 is higher 
        than 2011 performance. That's a great result, we get significantly more user
        than before.
    """)

with tab2 :
  st.header("Casual User Performance")
  st.bar_chart(data, x='mnth', y='casual')
  with st.expander("See explanation"):
    st.write("""
        From the chart above we can see that:
        The top 3 months of casual user performance is July, May, June.
        And the top 3 of worst performanece is January, February, and December.
    """)

with tab3 :
  st.header("Registered User Performance")
  st.bar_chart(data, x='mnth', y='registered')
  with st.expander("See explanation"):
    st.write("""
        From the chart above we can see that:
        The top 3 months of casual user performance is August, September, June.
        And the top 3 of worst performanece is January, February, and March.
    """)

# try regression to see correlation of weather conditions with bike rent performance

st.header("Advanced Analyze with Regression", divider='blue')
st.subheader("Relation between temperature and humidity with users")
fig, (ax1,ax2) = plt.subplots(ncols=2, figsize=(20,5))
sns.regplot(x=data['temp'], y=data['cnt'], ax=ax1 ,color='red')
sns.regplot(x=data['hum'], y=data['cnt'], ax=ax2)
st.pyplot(fig)
with st.expander("see explanation"):
  st.write("""
           Both on temperature's and humidity's scatterplot, mass of point is grouping
           around regression line, but there are also a lot of point is far from the line.
           So, to make sure, let's see what in correlation heatmap show
           """)

# create correlation between temp and humidity with user using heatmap from seaborn

st.subheader("Correlation Heatmap of Temperature and Humidty with Users")
var1=['temp','hum','cnt']
newdata=data.loc[:, var1]
corr = newdata.corr()
plt.figure(figsize=(15,7))
sns.heatmap(corr, annot=True, annot_kws={'size':10})
st.pyplot()
with st.expander("see explanation"):
  st.write("""
           From the heatmap above, we can see correlation between Temperature and Users is positive,
           so temperature really affect count of bike rent in positive ways, the lower temperature
           decrease the bike users.
           And correlation between Humidity and Users is negative, it means the lower humidity,
           it will increase the bike users.
           """)

text = st.text_area('Feedback')
st.write('Feedback: ', text)

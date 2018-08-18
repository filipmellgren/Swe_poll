#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 21:40:25 2018

@author: filip
"""
import pandas as pd
import wikipedia as wp
import numpy as np
import matplotlib.pyplot as plt

html = wp.page("Opinion polling for the Swedish general election, 2018").html().encode("UTF-8")
polls = pd.read_html(html)[0] # Selects the table at index "0".

# Create a header
polls.columns = polls.iloc[0]
polls = polls.reindex(polls.index.drop(0))

#### Clean up the date values ####
polls["date"] = polls.iloc[:,0].str.slice(-11,) # Limit ourselves to last poll date.
polls["date"] = polls["date"].str.replace("","0") # Changes "" to "0".

# Some values miss day info., I insert the middle of the month to compensate.
polls["date"] = polls["date"].where(polls.iloc[:,-1].str.len() == 11, "15 "+polls["date"])

# One value is of the format "6 June 2016"
polls["date"] = polls["date"].where(polls.iloc[:,-1] != "6 June 2016", "06 Jun 2016")

# Convert our date feature into date format
polls["date"] = pd.to_datetime(polls['date'], 
  format="%d %b %Y", utc=True)

#### Drop some columns ####
polls = polls.drop("Fieldwork date", "columns")
polls = polls.drop("Lead", "columns")
polls = polls.set_index("date")

#### The data is not stored as float numbers, let's correct this.
for party in list(polls)[1:-1]:
    polls[party] = pd.to_numeric(polls[party], errors = "coerce")

#### Eyeball some useful statistics:
polls.head()
polls.describe()

#### Create a smooth average value ####
MA_30 = polls.rolling(30)

#### Set colour scheme
colours = ["crimson", "mediumblue", "gold", "chartreuse", "g", 
           "darkred", "lightskyblue", "midnightblue", "fuchsia"]

#### Build a plot ####
with plt.style.context('seaborn-notebook'):
    #fig = plt.figure()
    fig, ax = plt.subplots()
    for party in np.arange(1,len(list(polls)[1:-1])+1,1): #list(polls)[1:-1]:
        ax.plot(polls.iloc[:,party], linestyle = "none", 
                marker = "o", markersize = 4, alpha = 0.7,
                color = colours[party-1])
    plt.xlabel("Date")
    plt.ylabel("Share")
    plt.title("Opinion development")
    plt.xticks(rotation = 90)
    ax.legend(list(polls)[1:-1],bbox_to_anchor=(1, 1), markerscale = 2)
    plt.locator_params(axis='y', nbins=6)
    for party in np.arange(1,len(list(polls)[1:-1])+1,1): #list(polls)[1:-1]:
        ax.plot(MA_30.mean().iloc[:,party], 
                color = colours[party-1], alpha = 0.5, linewidth = 2)


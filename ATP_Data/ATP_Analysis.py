from pylab import *
import matplotlib.dates as dates
import datetime
import pandas as pd

"""
this takes input (text file) and appends items to a list and then we use pandas to analyze the data
"""

# This is the output of the data fetching script
inp_text = r'C:/Users/Paulo/PycharmProjects/Practice/Python_Mentoring/ATP_Data/Rankings02232015.txt'
inp_text_handler = open(inp_text, 'rt').read() #reads in data

ATP_data_list = []
Analysis_ATP_data_list = []

for line in inp_text_handler.splitlines():
    ATP_data_list.append(line)

for player in ATP_data_list:
    player = player.replace('[', '').replace(']', '').replace("'", '').replace(" ", '').split(',') #works
    # Creates one dataset where all items have the same data.
    # interesting_data = Ranking, FirstName, Lastname, Country, CareerPrizeMoney
    interesting_data = (player[0], player[1], player[2], player[3], int(player[-1]))
    Analysis_ATP_data_list.append(interesting_data)

# This sets pandas to display all of the rows, the length of the dataset
pd.set_option('display.max_rows', len(Analysis_ATP_data_list))

# Use pandas to create a dataframe object
df = pd.DataFrame(Analysis_ATP_data_list, columns=['Ranking',
                                                       'First_Name',
                                                       'Last_Name',
                                                       'Country',
                                                       'Prize_Money'])

#Here I play with pandas. I organize the data in 4 ways:
print(df.sort_index(by='Prize_Money', ascending=False))

print(df.groupby(['Country', 'Ranking', 'First_Name', 'Last_Name'])['Prize_Money'].sum())

print((df.describe()))

print(df.groupby("Country", as_index=False).agg({"Prize_Money": ["sum", "count", "median", "mean"]}))



# Drafts:

# #This is good - Cookbook
# # with open(r'C:/Users/Paulo/PycharmProjects/Practice/ATP_Stats/Full_Ranking_Jan192015.txt', 'wt') as f:
# #     f.write(str(df.sort_index(by='Prize_Money', ascending=False)))
# print(df.sort_index(by='Prize_Money', ascending=False))
#
# # with open(r'C:/Users/Paulo/PycharmProjects/Practice/ATP_Stats/Groupby_Country_General', 'wt') as a:
# #     a.write(str(df.groupby(['Country', 'Ranking', 'First_Name', 'Last_Name'])['Prize_Money'].sum()))
# print(df.groupby(['Country', 'Ranking', 'First_Name', 'Last_Name'])['Prize_Money'].sum())
#
# # with open(r'C:/Users/Paulo/PycharmProjects/Practice/ATP_Stats/Data_Summary', 'wt') as b:
# #     b.write(str(df.describe()))
# print((df.describe()))
#
# # more complicated:
# # with open(r'C:/Users/Paulo/PycharmProjects/Practice/ATP_Stats/Groupby_Country_Details', 'wt') as c:
# #     c.write(str(df.groupby("Country", as_index=False).agg({"Prize_Money": ["sum", "count", "median", "mean"]})))
# print(df.groupby("Country", as_index=False).agg({"Prize_Money": ["sum", "count", "median", "mean"]}))
#

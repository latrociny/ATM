import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly
import pylab
#pylab.show()
import os
import pickle
os.system('cls')

rawData = pd.read_excel(r'C:\Users\DLL\Downloads\raw.xlsx', 
sheet_name = "Data")
type(rawData)
rawData.describe()
rawData.head()
rawData.values
rawData.columns

## Cleaning ##
rawData = rawData.fillna(0)
rawData = rawData.replace('..',0)

## Exploratory analysis ##
rawData[rawData.columns[3]].head()
rawData[rawData.columns[7]].describe()

# Check how many empty values are present
# zero = [0]
# for i in range(0,9):
#     print(i)
    #rawData[rawData.columns[i]].head()
    #rawData[rawData.columns[i]].isin(zero).sum()

# Analysis (above) shows emptys from 2013 - 2017: 62, 66, 68, 92, 211
# I choose to take 2016 (col# 7), to reflect fora balance of
# completeness vs. representativeness of new info
selection = rawData [['Country Name', 'Country Code', 'Series Name', '2016 [YR2016]']]
# Garbage text from 528-532
selection = selection.drop(selection.index[[528,529,530,531,532]])

selection.columns = ['Country', 'Code', 'Series', 'Y2016']
# Moves every 2nd row (ATM values) to a new DF
selectionATM = pd.DataFrame({'Country':selection['Country'].iloc[::2].values,
 'Code':selection['Code'].iloc[::2].values, 
 'Series':selection['Series'].iloc[::2].values,
 'ATM_2016':selection['Y2016'].iloc[::2].values})
selectionGDP = selection.copy()
# Now the ATM related values are dropped
selectionGDP = selectionGDP.drop(selectionGDP.index[::2])
selectionGDP.rename(columns={'Y2016':'GDP_Y2016'}, inplace=True)

result = pd.merge(selectionGDP, selectionATM, how='outer', on=['Code'])
# Checking if the merge occured correctly
# check = result['Country_x'].equals(result['Country_y'])
# Dropping series, these were just carried on till now and could have been deleted earlier
# Values are Automated teller machines (ATMs) (per 100,000 adults) and GDP per capita (current US$)


result =result.drop(['Series_x', 'Series_y', 'Country_y'], axis=1)
result.rename(columns={'Country_x':'Country','ATM_2016':'ATM_2016/10^5 adults'}, inplace=True)
## ATM population is  (number of ATMs)*100,000/adult population in the reporting country. 
# Now the ATMs are per 100,000 adults, which doesn't match with GDP/capita. Need to convert ATMs (like-to-like basis) per capita basis 
# Getting population % from ages 0-14 for 2016
popData = pd.read_excel(r'C:\Users\DLL\Downloads\pop.xlsx', 
sheet_name = "Data")
type(popData)
popData.describe()
popData.head()
popData.values
popData.columns
popData.rename(columns={'2016 [YR2016]':'AdultPop','Country Code':'Code'}, inplace=True)
popData.dtype
popData['AdultPop'] = pd.to_numeric(popData.AdultPop, errors='coerce')
# Since there is no data of adult populations (>18), I assume >15 is adult 
popData.AdultPop = 100 - popData.AdultPop
popData = popData.drop(['Series Name', 'Series Code', 'Country Name'], axis=1)
result = pd.merge(result, popData, how='outer', on=['Code'])
result = result[pd.notnull(result['AdultPop'])]

result.dtypes
result['ATMperCapita'] = result['ATM_2016/10^5 adults'] / 100000 * (result['AdultPop']/100)
result['ATMperCapita'].describe()
result.plot.scatter(x='GDP_Y2016', y='ATMperCapita')
result.plot.scatter(x='GDP_Y2016', y='ATMperCapita', label='Code')
plt.scatter(result.GDP_Y2016, result.ATMperCapita, c=result.Country)

plt.show()


########Playing and learning
test = pd.DataFrame({'a':range(1,11),'b':['m','f','m','m','m','f','m','f','f','f'],'c':np.random.randn(10)})
testSel = test[['a', 'b']]
testDrop = test.drop(test.index[::2])

pd.set_option('max_rows',200)
pd.set_option('max_columns',10)
pd.set_option('display.expand_frame_repr', False)

result.plot.scatter(x='GDP_Y2016', y='ATM_2016')

## Pickling
# Read more at https://www.datacamp.com/community/tutorials/pickle-python-tutorial
dogs_dict = { 'Ozzy': 3, 'Filou': 8, 'Luna': 5, 'Skippy': 10, 'Barco': 12, 'Balou': 9, 'Laika': 16 }
outfile = open('dogs','wb')
pickle.dump(dogs_dict,outfile)
outfile.close()

infile = open('dogs','rb')
new_dict = pickle.load(infile)
infile.close()
# the output/pickle is stored in the path in which the script resides

## Getting the path in which the script resides
import os
import sys
# as a function 
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
get_script_path()
# ordinary command 
os.path.dirname(os.path.realpath(sys.argv[0]))

## Ideas
# Also see correlation b/w nr of ATMs and urbanization
# Ease of doing business vs credit accessibility
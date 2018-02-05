import scholarly
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

n = 600 #number of professors who's pubulication record was extracted from Google Scholar

### Import CSV file containing salaries of Washington State Employees, and remove white spaces in each column
df = pd.read_csv('WaStEmployeeHistSalary.csv')
df['Name'] = df['Name'].str.strip()
df['Affiliation'] = df['Affiliation'].str.strip()
df['Position'] = df['Position'].str.strip()

### Remove rows that are listed as 'Name Withheld'
df = df[df.Name != 'Name Withheld']

### Filter out affiliations that are not Washington State University (the most frequent university in our database)
df = df[df.Affiliation == 'University of Washington']

### Filter out positions that are not titled "Professor"
df = df[df.Position == 'PROFESSOR'].reset_index()

### Import CSV file containing publication record from Google Scholar
df_gscholar = pd.read_csv('gscholar_final.csv')

### Extract Salaries from df, and append to df_gscholar

salary_2012 = df['2012'][0:n]
salary_2013 = df['2013'][0:n]
salary_2014 = df['2014'][0:n]
salary_2015 = df['2015'][0:n]
salary_2016 = df['2016'][0:n]
salary_sum = salary_2012 + salary_2013 + salary_2014 + salary_2015 + salary_2016


df_gscholar['2012'] = salary_2012
df_gscholar['2013'] = salary_2013
df_gscholar['2014'] = salary_2014
df_gscholar['2015'] = salary_2015
df_gscholar['2016'] = salary_2016
df_gscholar['Sum of 5 Year Salaries'] = salary_sum



### Filter out NA
df_gscholar.dropna(how='any', inplace=True)

##df_gscholar = df_gscholar.drop([0])
print df_gscholar


### Plot Salaries vs. Total Citations
##sns.pairplot(df_gscholar)
g = sns.regplot(x="5 year h-index", y="Sum of 5 Year Salaries", data=df_gscholar, fit_reg=False)
g.set_ylim(-1000000,4000000)
plt.show()


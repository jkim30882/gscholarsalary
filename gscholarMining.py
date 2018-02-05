import scholarly
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time


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

### Create a new dataframe for our google scholar query
fname = 'gscholar6.csv'
df_gscholar = pd.DataFrame(columns=['Name','Total Citations', 'h-index', '5 year h-index', 'i10-index', '5 year i10-index'])
df_gscholar.to_csv(fname)

# Data mining from google scholar. Go through all the names in df, and extract publication record of each individual from google scholar
start_time = time.time()
aff = 'University of Washington'
n = len(df)
with open(fname, 'a') as f:
    for index in range(500, 600):
        print "Searching Number:", index+1, '/', n
        name = df.Name[index]
        print name, "in",  aff
        search_query = scholarly.search_author(name + ',' + aff)
        author = next(search_query, None)
        if author is None:
            row = [name, 'NA', 'NA', 'NA', 'NA', 'NA']
            df_gscholar.loc[index] = row
            continue
        else:
            author = author.fill()
            row = [name, author.citedby, author.hindex, author.hindex5y, author.i10index, author.i10index5y]
            df_gscholar.loc[index] = row
    df_gscholar.to_csv(f,header=False)
elapsed_time = time.time() - start_time
print time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
print df_gscholar
print df_gscholar.describe()

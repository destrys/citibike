import numpy as np
import pandas as pd
import csv
from datetime import datetime

def insertTemp(df,tempfile):
    """Inserts a Temperature Column in a given DataFrame from tempfile"""
    temps = {}

    f = open(tempfile,'r')
    reader = csv.reader(f,delimiter=' ',skipinitialspace=True)
    reader.next()
    for line in reader:
        temp_time = datetime.strptime(line[2],'%Y%m%d%H%M').replace(minute=0)
        temp_value = line[21]
        if not '*' in temp_value:
            temps[temp_time] = int(temp_value)

    tempdf = pd.Series(temps).reindex(df.index)
    df['temp'] = tempdf
    
    tempbins = [40,50,60,70,80,]
    for i in xrange(24*7):
        df['w'+str(i)+'t40'] = np.logical_and(df.weekhour == i,df.temp < 40)
        for j in xrange(1,5):
            tempbool = np.logical_and(df.temp >= tempbins[j-1],df.temp < tempbins[j])
            df['w'+str(i)+'t'+str(tempbins[j])] = np.logical_and(df.weekhour == i,tempbool)
        df['w'+str(i)+'t100'] = np.logical_and(df.weekhour == i, df.temp >= 80)

    return None

from datetime import datetime
import re
import numpy as np
from collections import defaultdict
import pandas as pd

def loadCapital(filelist):
    """Loads Data from CapitalBikes, output DataFrame"""

    data = {}
    
    for filename in filelist:
        f = open(filename,'r')
        f.next()

        if '2011' in filename:
            out_stat_indx = 3
            in_stat_indx = 4
            out_time_indx = 1
            in_time_indx = 2
        elif '2012-1' in filename or '2012-2' in filename:
            out_stat_indx = 4
            in_stat_indx = 7
            out_time_indx = 2
            in_time_indx = 5
        else:
            out_stat_indx = 3
            in_stat_indx = 6
            out_time_indx = 1
            in_time_indx = 4

        for line in f:
            sptline = line.split(',')
            if '2011' in filename:
                try:
                    out_station = re.search('\((.....)\)',sptline[out_stat_indx]).group(1)
                except AttributeError:
                    out_station = ''
                try:
                    in_station = re.search('\((.....)\)',sptline[in_stat_indx]).group(1)
                except AttributeError:
                    in_station = ''
            else:
                out_station = sptline[out_stat_indx]
                in_station = sptline[in_stat_indx]

            out_time = datetime.strptime(sptline[out_time_indx],'%m/%d/%Y %H:%M').replace(minute=0)
            in_time = datetime.strptime(sptline[in_time_indx],'%m/%d/%Y %H:%M').replace(minute=0)

            if out_station != '':
                if out_station in data.keys():
                    data[out_station][out_time] -= 1
                else:
                    data[out_station] = defaultdict(int)
                    data[out_station][out_time] = -1
            if in_station != '':
                if in_station in data.keys():
                    data[in_station][in_time] += 1
                else:
                    data[in_station] = defaultdict(int)
                    data[in_station][in_time] = 1
        f.close()
    newdata = {}
    for station in data.keys():
        newdata[station] = pd.Series(data[station])

    for station in newdata.keys():
        if station[6:] == 'in':
            newdata[station[0:5]+'_net'] = newdata[station] - newdata[station[0:5]+'_out']

    df = pd.DataFrame(newdata)

# Insert a column for each 'weekhour' which is Boolean...
    df['weekhour'] = df.index.hour + df.index.weekday*24
    for item in set(df['weekhour']):
        for month in range(12):
            df['w'+str(item)+'m'+str(month)] = np.logical_and(df['weekhour'] == item,df.index.month == month)

# This will be one of the features
# I could also add a column for each month...2

    return df

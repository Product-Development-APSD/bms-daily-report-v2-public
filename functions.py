# import package
import pandas as pd
import seaborn as sns
import numpy as np

import math
import datetime
import requests
import io
import base64

import matplotlib.pylab as plt
## Function to collect data
def collect_data(DATE, TERMINAL):
    ARR = []
    print('Collecting Data Terminal:', TERMINAL)

    ## Generate series of time
    start = datetime.datetime(int(DATE[:4]), int(DATE[6:7]), int(DATE[8:]))
    end = datetime.datetime(int(DATE[:4]), int(DATE[6:7]), int(DATE[8:]), 23, 0, 0)
    step = datetime.timedelta(hours=1)

    date = []

    while start <= end:
        date.append(start.strftime('%Y-%m-%d %H:%M:%S'))
        start += step
    date = pd.to_datetime(pd.Series(date), format='%Y-%m-%d %H:%M:%S')

    hours = []
    for i in range(len(date[:])):
        hours.append(date[i].strftime("%H:%M"))

    ## Retrieve data from URL
    url = f'https://developer.angkasapura2.co.id/fids_central/integration/data_scheduled4?branchCodeList=CGK&getterminalap2={TERMINAL}&getcategorycode=ALL&all_search={DATE}&datas=FIDS&search='
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df_ = df_list[0]
    df = df_[:-1]
    print('status: finish collecting data', DATE, '\n')

    ## Store data in Dataframe
    Dataset = pd.DataFrame()
    Dataset['TIME'] = hours
    Dataset['ARR'] = df['ARR']

    ## Define mean, mean+sd, and mean-std
    mean = np.round(Dataset['ARR'].mean(),3)
    meanplus = np.round(Dataset['ARR'].mean() + math.sqrt(np.var(Dataset['ARR'])),3)
    meanmin =  np.round(Dataset['ARR'].mean() - math.sqrt(np.var(Dataset['ARR'])),3)

    ## list time with ARR > mean+std
    list_ovtime = Dataset['TIME'][Dataset['ARR'] > meanplus].values
    
    ## Get Time for ARR > mean
    time_ = []
    res = Dataset[Dataset['ARR'] > mean]
    time_.append(res['TIME'].values[0])
    time_.append(res['TIME'].values[-1])

    ## Create list of Dictionary
    dictData = []
    for j in range(len(Dataset['TIME'].values)):
        D = {'TIME': Dataset['TIME'][j],
            'ARRIVAL FLIGHT': int(Dataset['ARR'][j])}
        dictData.append(D)

    return list(dictData[6:]), Dataset, time_, list_ovtime, mean, meanplus, meanmin

## Function to Generate Picture
def generate_graph(df, terminal, date, hari_ini):
    
    mean = df['ARR'].mean()
    err = math.sqrt(np.var(df['ARR']))

    sns.set(style="darkgrid")
    sns.relplot(
        data=df[6:], 
        x="TIME", y="ARR",
        height=5, aspect=3.5, 
        kind="line",
        label=f"Est. Arrival Flight T{terminal}", marker='o', color='darkmagenta'
    ).set(
        title=f"Data Scheduled Arrival Flight Terminal {terminal} CGK\nPada hari {hari_ini}\n",
        ylabel="Scheduled Arrival Flight",
        xlabel="Waktu"
    )
    plt.xticks(df['TIME'][6:], rotation=34)
    plt.axhline(df['ARR'].mean(), linestyle=':', color='orange', label=f'mean = {np.round(mean,2)}')
    plt.axhline(df['ARR'].mean()+math.sqrt(np.var(df['ARR'])), linestyle=':', color='maroon', label=f'mean + std.err = {np.round(mean+err,2)}')
    plt.axhline(df['ARR'].mean()-math.sqrt(np.var(df['ARR'])), linestyle=':', color='forestgreen', label=f'mean - std.err = {np.round(mean-err,2)}')
    plt.legend(loc='upper left')
    plt.rcParams.update({"figure.dpi": 144})

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    print(f'success to generate graph T{terminal}') 

    return image_base64

# Function to generate text from list of time
def generate_text(list_time):
    list_temp = []
    for i in list_time:
        list_temp.append(f"- {i}\n")
    text = ''''''.join(list_temp)
    return text


def get_info(df, terminal):
    err = math.sqrt(np.var(df['ARR']))

    rslt = df[df['ARR'] > (df['ARR'].mean()+err)]
    for i in rslt['TIME'].values:
        print(f'- {i}')
    print(f"Di Terminal {terminal} pada rentang waktu tersebut  memerlukan perhatian khusus oleh tim yang bertugas.")
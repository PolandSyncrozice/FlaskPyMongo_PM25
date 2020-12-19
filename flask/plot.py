import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import json


def toBarplot(data):

    city = "Bangkok"
    df = pd.DataFrame(data)
    df = df.loc[df['pm25']!=' ']
    df = df[['date','pm25']]

    df['date'] = pd.to_datetime(df.date)
    df['pm25'] = pd.to_numeric(df.pm25)

    df_2018 = df.loc[(df['date'].dt.year == 2018) & (df['date'].dt.month >= 10)]
    df_2019 = df.loc[(df['date'].dt.year == 2019)]
    df_2020 = df.loc[(df['date'].dt.year == 2020) & (df['date'].dt.month <= 12)]
    df = df_2018.append(df_2019.append(df_2020), ignore_index=True)

    df = df.groupby([df['date'].dt.year.rename('year'), df['date'].dt.month.rename('month')])['pm25'].apply(lambda x: (x>100).sum()).reset_index()

    month_to_short = {1: "Jan",
                    2: "Feb",
                    3: "Mar",
                    4: "Apr",
                    5: "May",
                    6: "Jun",
                    7: "Jul",
                    8: "Aug",
                    9: "Sep",
                    10: "Oct",
                    11: "Nov",
                    12: "Dec"}
    df['month'] = df['month'].map(month_to_short)
    df['year'] = df['year'].astype(str)
    df['month'] = df['month'].astype(str)

    df['month_year'] = df['month'] + " - " + df['year']

    ax = df.set_index('month_year')['pm25'].plot(kind='bar',figsize=(19, 10),color='cadetblue',rot=45, fontsize=14)
    plt.title("Historical PM2.5 > 100 Per Month ("+ city +")", y=1.013, fontsize=22)
    plt.ylabel("Count of PM2.5 > 100", labelpad=16, fontsize=16)
    plt.xlabel("", labelpad=16, fontsize=16)

    for p in ax.patches:
        ax.annotate("%d" % p.get_height(), (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='center', fontsize=16, color='black', rotation=0, xytext=(0, 7),
                    textcoords='offset points')
        
    figure = ax.get_figure()    
    figure.savefig('./'+'static/city/'+city+'_bar.png', dpi=150)

def toHeatplot(data):

    city = "Bangkok"
    df = pd.DataFrame(data)
    df = df.loc[df['pm25']!=' ']
    df = df[['date','pm25']]

    df['date'] = pd.to_datetime(df.date)
    df['pm25'] = pd.to_numeric(df.pm25)

    df = df.sort_values('date')

    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['year'] = df['date'].dt.year

    month_to_short = {1: "Jan",
                    2: "Feb",
                    3: "Mar",
                    4: "Apr",
                    5: "May",
                    6: "Jun",
                    7: "Jul",
                    8: "Aug",
                    9: "Sep",
                    10: "Oct",
                    11: "Nov",
                    12: "Dec"}
    df['month'] = df['month'].map(month_to_short)

    df['year'] = df['year'].astype(str)
    df['month'] = df['month'].astype(str)
    df['month_year'] = df['month'] + " - " + df['year']

    cats = []
    for x in pd.unique(df['month_year']):
        cats.append(x)

    df_2018 = df.loc[(df['date'].dt.year == 2018) & (df['date'].dt.month >= 10)].reset_index(drop=True)
    df_2019 = df.loc[(df['date'].dt.year == 2019)].reset_index(drop=True)
    df_2020 = df.loc[(df['date'].dt.year == 2020) & (df['date'].dt.month <= 12)].reset_index(drop=True)
    df = df_2018.append(df_2019.append(df_2020), ignore_index=True)
    
    df = df.pivot(index='month_year', columns='day', values='pm25')
    
    df.index = pd.CategoricalIndex(df.index, categories= cats)
    df.sort_index(level=0, inplace=True)

    sns.palplot(sns.diverging_palette(1, 1, n = 19))
    plt.figure(figsize =(40,15))
    sns.set(font_scale = 2)
    ax = sns.heatmap(df,annot=True, fmt=".0f", cmap="YlOrRd", linewidths=0.05, vmin=0, vmax=200)
    figure = ax.get_figure()    
    figure.savefig('./static/city/'+city+'_heat.png', dpi=150)
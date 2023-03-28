import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.mode.chained_assignment = None 
sns.set_theme(style="ticks", font_scale=0.8)
def data_processing(url):
    data = (
        pd.read_csv(url,low_memory=False)
        .loc[:, ["region_group","country","year","Location","literacy_1524_no"]]
        .dropna(subset="literacy_1524_no")
        .reset_index()
        .drop(columns = ["index"])
        .rename(columns = {"literacy_1524_no" : "literacy_rates"})
    )
    
    functions = {'country': 'first','year': 'first','literacy_rates': 'sum','region_group' : 'first'}
    data_processed = (
        data.groupby(["country","year"]).agg(functions)
    )
    
    return data_processed

def plotting(data):
    counts = data.country.value_counts()
    data = data[data.country.isin(counts.index[counts.gt(2)])]
    regions = data.region_group.unique()
    dictionary = {}
    for i in regions:
        df = data.loc[data["region_group"]==i]
        dictionary[i] = df
    
    return dictionary

def lineplot(dictionary):
    for i in range(6):
        grid = sns.FacetGrid(list(dictionary.values())[i], col="country", hue="country", palette="tab20c", col_wrap=5, height=2.5)
        grid.map(plt.plot, "year", "literacy_rates", marker="o")
        grid.set(xticks=np.arange(1998,2017))
        grid.set_xticklabels(np.arange(1998,2017), rotation=90)
        grid.fig.subplots_adjust(top=0.8)
        grid.fig.suptitle(list(dictionary.keys())[i])
        
    return

def more_processing(dictionary):
    data_plot1 = pd.DataFrame()
    data_plot2 = pd.DataFrame()
    for i in range(6):
        list(dictionary.values())[i].reset_index(drop = True, inplace = True)
        first_values = list(dictionary.values())[i].groupby(["country"]).agg({'country': 'first','year': 'min','literacy_rates': 'first',"region_group" : 'first'})
        last_values = list(dictionary.values())[i].groupby(["country"]).agg({'country': 'first','year': 'max','literacy_rates': 'last',"region_group" : 'first'})
        plot_values = first_values[["country"]]
        plot_values["percentage change"] = (last_values.literacy_rates-first_values.literacy_rates)/(first_values.literacy_rates)*100
        plot_values.reset_index(drop = True, inplace = True)
        temp = pd.DataFrame([[list(dictionary.keys())[i],plot_values["percentage change"].mean()]], columns = ["region_group","Average percentage change"])
        data_plot1 = pd.concat([data_plot1,plot_values],join="outer")
        data_plot2 = pd.concat([data_plot2,temp],join="outer")
        
    return data_plot1, data_plot2
    


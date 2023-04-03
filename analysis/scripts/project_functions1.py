#importing necessary packages and making changes to packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.mode.chained_assignment = None 
sns.set_theme(style="ticks", font_scale=0.8)

#Basic data processing to only select required columns from dataset, drop NA values and reset index
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

#creates a returns dictionary of dataset based on region group and in each dataset are countries with 3 or more years of entries
def plotting(data):
    counts = data.country.value_counts()
    data = data[data.country.isin(counts.index[counts.gt(2)])]
    #save this dataframe as excel file for tableu
    regions = data.region_group.unique()
    dictionary = {}
    for i in regions:
        df = data.loc[data["region_group"]==i]
        dictionary[i] = df
    
    return dictionary

#creates line graphs for each country in each region based dataframe to compare literacy rates over time
def lineplot(dictionary):
    for i in range(6):
        grid = sns.FacetGrid(list(dictionary.values())[i], col="country", hue="country", palette="tab20c", col_wrap=5, height=2.5)
        grid.map(plt.plot, "year", "literacy_rates", marker="o")
        grid.set(xticks=np.arange(1997,2017,5))
        grid.fig.subplots_adjust(top=0.8)
        grid.fig.suptitle(list(dictionary.keys())[i])
        
    return
#creates and returns two dataframes, the first being all the countries and the percentage change in literacy rates, and the second being the average change in literacy rates of each region based on the countries in that region
def more_processing(dictionary):
    data_plot1 = pd.DataFrame()
    data_plot2 = pd.DataFrame()
    data_plot3 = pd.DataFrame()
    for i in range(6):
        list(dictionary.values())[i].reset_index(drop = True, inplace = True)
        first_values = list(dictionary.values())[i].groupby(["country"]).agg({'country': 'first','year': 'min','literacy_rates': 'first',"region_group" : 'first'})
        last_values = list(dictionary.values())[i].groupby(["country"]).agg({'country': 'first','year': 'max','literacy_rates': 'last',"region_group" : 'first'})
        max_values = list(dictionary.values())[i].groupby(["country"]).agg({'country': 'first','year': 'first','literacy_rates': 'max',"region_group" : 'first'})
        plot_values = first_values[["country"]]
        plot_values["percentage change"] = (last_values.literacy_rates-first_values.literacy_rates)/(first_values.literacy_rates)*100
        plot_values2.reset_index(drop = True, inplace = True)
        plot_values2 = first_values[["country"]]
        plot_values2["percentage change"] = (max_values.literacy_rates-first_values.literacy_rates)/(first_values.literacy_rates)*100
        plot_values.reset_index(drop = True, inplace = True)
        temp = pd.DataFrame([[list(dictionary.keys())[i],plot_values["percentage change"].mean()]], columns = ["region_group","Average percentage change"])
        data_plot1 = pd.concat([data_plot1,plot_values],join="outer")
        data_plot2 = pd.concat([data_plot2,plot_values2],join="outer")
        data_plot3 = pd.concat([data_plot3,temp],join="outer")
        
    return data_plot1, data_plot2, data_plot3

#Plots a bar chart of percentage change of literacy rates in each country
def barplot1(data1,data2):
    fig, axes = plt.subplots(1, 2, figsize=(10,5))
    sns.barplot(ax=axes[0],data = data1, x="percentage change", y="country", width = 1)
    axes[0].set(title= "Percentage change in Literacy Rates between first and last record", xticks= np.arange(-200,3800,400))
    axes[0].axvline(color="black");
    sns.barplot(ax=axes[1],data = data2, x="percentage change", y="country", width = 1)
    axes[1].set(title= "Percentage change in Literacy Rates between first and max record", xticks= np.arange(-200,3800,400))
    axes[1].axvline(color="black");
    
    return

#Plots a bar chart of average percentage change in literacy rates of each region
def barplot2(data):
    plot = sns.barplot(data = data, x="region_group", y="Average percentage change", hue = "region_group",width = 1)
    plot.set(xticks=[], xlabel="", yticks=np.arange(-100,1000,50), ylabel="Percentage change", title = "Average Percentage change of Literacy rates of different regions");
    plot.axhline(color="black");
    return
    


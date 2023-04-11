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
    data.to_csv("../data/processed/dataset1_1.csv")
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
#creates and returns five dataframes
#first: the countries and the percentage change in literacy rates between first and last values
#second: the countries and the percentage change in literacy rates between first and max values
#third: the average change in literacy rates of each region based on the countries in that region between first and last values
#fourth:  the average change in literacy rates of each region based on the countries in that region between first and max values
#fifth: the intial average litracy rates of eac region
def more_processing(dictionary):
    data_plot1 = pd.DataFrame()
    data_plot2 = pd.DataFrame()
    data_plot3 = pd.DataFrame()
    data_plot4 = pd.DataFrame()
    data_plot5 = pd.DataFrame()
    for i in range(6):
        list(dictionary.values())[i].reset_index(drop = True, inplace = True)
        first_values = list(dictionary.values())[i].groupby(["country"]).agg({'country': 'first','year': 'min','literacy_rates': 'first',"region_group" : 'first'})
        first_values_2 = list(dictionary.values())[i].groupby(["region_group"]).agg({"region_group" : 'first','literacy_rates': 'mean'})
        last_values = list(dictionary.values())[i].groupby(["country"]).agg({'country': 'first','year': 'max','literacy_rates': 'last',"region_group" : 'first'})
        max_values = list(dictionary.values())[i].groupby(["country"]).agg({'country': 'first','year': 'first','literacy_rates': 'max',"region_group" : 'first'})
        plot_values = first_values[["country"]]
        plot_values["change"] = (last_values.literacy_rates-first_values.literacy_rates)/(first_values.literacy_rates)
        plot_values = plot_values.assign(percentage_change = lambda x: x.change*100)
        plot_values.reset_index(drop = True, inplace = True)
        plot_values2 = first_values[["country"]]
        plot_values2["change"] = (max_values.literacy_rates-first_values.literacy_rates)/(first_values.literacy_rates)
        plot_values2 = plot_values2.assign(percentage_change = lambda x: x.change*100)
        plot_values2.reset_index(drop = True, inplace = True)
        temp = pd.DataFrame([[list(dictionary.keys())[i],plot_values["percentage_change"].mean()]], columns = ["region_group","Average percentage change"])
        temp2 = pd.DataFrame([[list(dictionary.keys())[i],plot_values2["percentage_change"].mean()]], columns = ["region_group","Average percentage change"])
        data_plot1 = pd.concat([data_plot1,plot_values],join="outer")
        data_plot2 = pd.concat([data_plot2,plot_values2],join="outer")
        data_plot3 = pd.concat([data_plot3,temp],join="outer")
        data_plot4 = pd.concat([data_plot4,temp2],join="outer")
        data_plot5 = pd.concat([data_plot5,first_values_2],join="outer")
        
    data_plot1.to_csv("../data/processed/dataset1_2.csv")
    data_plot3.to_csv("../data/processed/dataset1_3.csv")

        
    return data_plot1, data_plot2, data_plot3, data_plot4, data_plot5

#Plots a bar charts of percentage change of literacy rates in each country
def barplot1(data1,data2):
    fig, axes = plt.subplots(1, 2, figsize=(9,5), sharey = True)
    fig.suptitle("Percentage Change in Literacy Rates Between First and Last/Max Record")
    sns.barplot(ax=axes[0],data = data1, x="percentage_change", y="country", width = 1)
    axes[0].set(title = "Between First and Last")
    axes[0].axvline(color="black");
    sns.barplot(ax=axes[1],data = data2, x="percentage_change", y="country", width = 1)
    axes[1].set(title = "Between First and Max")
    axes[1].axvline(color="black");
    return

#Plots a bar charts of average percentage change in literacy rates of each region and intial average literacy of each region
def barplot2(data1,data2,data3):
    plot1 = sns.barplot(data = data3, x="region_group", y="literacy_rates", hue = "region_group",width = 1)
    plot1.set(xticks=[], title = "Intial Average Literacy Rates", xlabel = "")
    plt.legend(bbox_to_anchor=[2, 1], loc = "upper right", title = "region group")
    
    fig, axes = plt.subplots(1, 2, figsize=(9,5), sharey = True)
    fig.suptitle("Average Percentage Change in Literacy Rates Of Different Regions")
    sns.barplot(ax=axes[0], data = data1, x="region_group", y="Average percentage change",width = 1)
    axes[0].set(xticks=[], xlabel="", yticks=np.arange(-100,1000,50), ylabel="Percentage Change", title = "Between First and Last");
    axes[0].axhline(color="black");
    sns.barplot(ax=axes[1], data = data2, x="region_group", y="Average percentage change",width = 1)
    axes[1].set(xticks=[], xlabel="", yticks=np.arange(-100,1000,50), ylabel="Percentage Change", title = "Between First and Max");
    axes[1].axhline(color="black");
    return
    


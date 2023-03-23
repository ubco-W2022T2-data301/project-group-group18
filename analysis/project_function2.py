import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#load and set data
def set_data(path):
    data = (
        pd.read_csv(path,low_memory=False)
        .loc[:,["income_group","region_group","literacy_1524_m", "Sex","Location","Wealth","comp_upsec_v2_m", "comp_prim_v2_m", "comp_lowsec_v2_m","year"]]
        .dropna(subset="literacy_1524_m")
        .reset_index()
        .drop(columns = ["index"])
    )
    return data

#make barplot
def barplot(dataset):
    plot = (
        sns.barplot(data = dataset, y = dataset["region_group"], hue = dataset["income_group"], x = dataset["literacy_1524_m"])
    .set( title = "Literacy Rates compared to Income Groups", xlabel = "Literacy Rates Ages 15-24", ylabel = "Regions")
    #sns.move_legend(plot, bbox_to_anchor=(1.5, 1), loc = "upper right")
    #plot.legend(bbox_to_anchor=(2, 1))
    )
        return

#make boxplots
def boxplot_UpSec(dataset):
    plot = (
        sns.boxplot(data = dataset, x = "comp_upsec_v2_m", y = "income_group")
        .set(title = "% of People who Completed Upper Secondary School Based on Different Income Groups", xlabel = "% of People who Completed Upper Secondary School", ylabel = "Income Groups")
    )
    return

def boxplot_LoSec(dataset):
    plot = (
        sns.boxplot(data=dataset, y="income_group", x="comp_lowsec_v2_m")
        .set(title = "% of People who Completed Lower Secondary School Based on Different Income Groups", xlabel = "% of People who Completed Lower Secondary School", ylabel = "Income Groups")
    )
    return

def boxplot_Pri(dataset):
    plot = (
        sns.boxplot(data=dataset2, y="income_group", x="comp_prim_v2_m")
        .set(title = "% of People who Completed Primary School Based on Different Income Groups", xlabel = "% of People who Completed Primary School", ylabel = "Income Groups")
    )
    return

#make violinplots
def violinplot(dataset):
    plot = (
        sns.violinplot(data=dataset2, x="literacy_1524_m", y="income_group", hue="Sex", split=True)
        .set(title = "Literacy Rates (Ages 15-25) Across Different Income Groups Based on Sex", xlabel = "Literacy Rates (Ages 15-24)", ylabel = "Income Groups")
    )
    return

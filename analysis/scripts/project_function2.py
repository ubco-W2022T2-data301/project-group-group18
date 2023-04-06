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
    data.to_csv("../data/processed/data2.csv")
    return data


#make barplot comparing literacy rate for each region group incremented by income group
def barplot(dataset):
    plot = (
        sns.barplot(data = dataset, y = dataset["region_group"], hue = dataset["income_group"], x = dataset["literacy_1524_m"], palette = "Set2")
    .set( title = "Literacy Rates compared to Income Groups", xlabel = "Literacy Rates Ages 15-24", ylabel = "")
    )
    plt.legend(bbox_to_anchor=[2, 1], loc = "upper right")
    return

#make ridgeline plots 
def ridgeline1(dataset):
    plot1 = sns.FacetGrid(dataset, row="Wealth", hue="Wealth", aspect=3.5, height = 1.3, palette = "Set2")
    plot1.map(sns.kdeplot, "comp_upsec_v2_m", bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=.75)
    plot1.map(sns.kdeplot, "comp_upsec_v2_m", clip_on=False, color="w", lw=2, bw_adjust=0.5)
    plot1.set(xlabel = "% of People Who Completed Upper Secondary School", ylabel = "Literacy Rate")
    plot1.fig.subplots_adjust(top=0.8)
    plot1.fig.suptitle("% of People Who Completed Upper Secondary School per Quintiles 1-5 (poorest-richest)")
    return
    
def ridgeline2(dataset):
    plot2 = sns.FacetGrid(dataset, row="Wealth", hue="Wealth", aspect=3.5, height = 1.3, palette = "Set2")
    plot2.map(sns.kdeplot, "comp_lowsec_v2_m", bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=.75)
    plot2.map(sns.kdeplot, "comp_lowsec_v2_m", clip_on=False, color="w", lw=2, bw_adjust=.5)
    plot2.set(xlabel = "% of People Who Completed Lower Secondary School", ylabel = "Literacy Rate")
    plot2.fig.subplots_adjust(top=0.8)
    plot2.fig.suptitle("% of People Who Completed Lower Secondary School per Quintiles 1-5 (poorest-richest)")
    return
    
def ridgeline3(dataset):
    plot3 = sns.FacetGrid(dataset, row="Wealth", hue="Wealth", aspect=3, height = 1.3, palette = "Set2")
    plot3.map(sns.kdeplot, "comp_prim_v2_m", bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=.75)
    plot3.map(sns.kdeplot, "comp_prim_v2_m", clip_on=False, color="w", lw=2, bw_adjust=.5)
    plot3.set(xlabel = "% of People Who Completed Primary School", ylabel = "Literacy Rate")
    plot3.fig.subplots_adjust(top=0.8)
    plot3.fig.suptitle("% of People Who Completed Primary School per Quintiles 1-5 (poorest-richest)")
    return


#make boxplots
def boxplots(dataset):
    sns.set(font_scale = 1.5)
    fig, axes = plt.subplots(1, 3, figsize=(25, 10),sharey=True)
    fig.suptitle('% of People Who Completed Different School Levels Based on Income Groups')
    plot1 = sns.boxplot(ax=axes[2], data=dataset, x = "comp_upsec_v2_m", y = "income_group", hue = "Sex", palette = "Set2").set(xlabel = "% of People Who Completed Upper Secondary School", ylabel = "")
    plot2 = sns.boxplot(ax=axes[1], data=dataset, x = "comp_lowsec_v2_m", y = "income_group", hue = "Sex", palette = "Set2").set(xlabel = "% of People Who Completed Lower Secondary School", ylabel = "")
    plot3 = sns.boxplot(ax=axes[0], data=dataset, x = "comp_prim_v2_m", y = "income_group", hue = "Sex", palette = "Set2").set(xlabel = "% of People Who Completed Primary School", ylabel = "")
    return


#make violinplots
def violinplot(dataset):   
    plot = (
        sns.violinplot(data=dataset, x="literacy_1524_m", y="income_group", hue="Sex", split=True, palette = "Set2")
        .set(title = "Literacy Rates (Ages 15-25) Across Different Income Groups Based on Sex", xlabel = "Literacy Rates (Ages 15-24)", ylabel = "Income Groups")
    )
    return

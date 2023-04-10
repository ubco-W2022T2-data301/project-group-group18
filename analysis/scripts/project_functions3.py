import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joypy
from joypy import joyplot
from pandas.api.types import CategoricalDtype
import plotly.express as px
sns.set_theme(style="ticks",
              font_scale=1.3,
             )


def load_and_process(url_or_path_to_csv_file,dtype):
    data = pd.read_csv(url_or_path_to_csv_file,dtype={"Region": "object", "Ethnicity": "object","Religion": "object","Language": "object"})
    a= len(data.columns)
    df = (data
          .drop(data.iloc[:,62:a],axis=1)
          .drop(data.iloc[:,37:44],axis=1)
          .dropna(subset=['Sex'])
          .reset_index(drop=True)
         )
    return df

def region(df):
    f, axes = plt.subplots(ncols=3,sharex='col', sharey='row')
    plt.rcParams["figure.figsize"] = [10.00,10.00]
    plt.rc('axes', labelsize=10)
    plt.title("Gender Disparities in Literacy Rates across Different Regions and Education Levels",loc='right',fontsize=20)
    my_pal = {sex: '#eb4d4b' if sex == "Female" else '#686de0' for sex in df["Sex"].unique()}
    sns.violinplot(x=df['comp_prim_v2_m'],y=df['region_group'].sort_values(),hue=df['Sex'],ax=axes[0],palette=my_pal)
    sns.violinplot(x=df['comp_lowsec_v2_m'],y=df['region_group'].sort_values(),hue=df['Sex'],ax=axes[1],palette=my_pal)
    sns.violinplot(x=df['comp_upsec_v2_m'],y=df['region_group'].sort_values(),hue=df['Sex'],ax=axes[2],palette=my_pal)
    axes[0].get_legend().remove()
    axes[1].get_legend().remove()
    axes[2].legend(bbox_to_anchor=[1,0.9],loc='upper left',title='Sex')
    axes[0].set(ylabel=None,xlabel="Completed primary")
    axes[1].set(ylabel=None,xlabel="Completed lower secondary")
    axes[2].set(ylabel=None,xlabel="Completed upper secondary")
    plt.savefig('../images/1.png',bbox_inches = 'tight')
    plt.show()
    sns.despine(trim=True, left=True)
    
def wrangling2(df):
    result_df = (df[df['Sex'] == 'Male'][['literacy_1524_m', 'Religion']].rename(columns={'literacy_1524_m': 'Male'})
             .dropna(subset=['Religion','Male'])
             .merge(df[df['Sex'] == 'Female'][['literacy_1524_m', 'Religion']].rename(columns={'literacy_1524_m': 'Female'})
                    .dropna(subset=['Religion','Female']),how='outer', on='Religion')
             .dropna()
             .groupby('Religion')
             .filter(lambda x: x['Male'].nunique() > 1 and x['Female'].nunique() > 1)
             .reindex(columns=['Religion','Male','Female'])
                )
    return result_df

def plot_religion(df):
    df=df.dropna(subset=['Religion','literacy_1524_m'])
    plt.figure()
    ax,fig = joyplot(data=df[['Religion','literacy_1524_m']],
            by=df['Religion'],
            column=['literacy_1524_m'],
            alpha = 0.85,
            figsize=(12,20))
    plt.rc('axes', labelsize=16)
    plt.title('Literacy Rate among certain Religions',fontsize=20)
    plt.xlabel("Literacy Rate")
    plt.savefig('../images/2.png',bbox_inches = 'tight')
    plt.show()
    
def religion(result_df):
    plt.figure()
    ax,fig = joyplot(data=result_df[['Male','Female','Religion']],
            by=result_df['Religion'],
            column=['Male','Female'],
            color=['#686de0','#eb4d4b'], 
            legend=True,
            alpha = 0.85,
            figsize=(12,15)
                )
    plt.rc('axes', labelsize=16)
    plt.title('Literacy Rate among Genders of certain Religions',fontsize=20)
    plt.xlabel("Literacy Rate")
    plt.savefig('../images/3.png',bbox_inches = 'tight')
    plt.show()
    
def bar(pivot):
    fig, ax = plt.subplots()
    pivot.plot(kind="barh", width=0.8, color=['#eb4d4b','#686de0'], ax=ax)
    ax.set_title("Literacy Rate by Wealth and Gender")
    ax.set_xlabel("Literacy Rate")
    ax.set_ylabel("Wealth")
    ax.legend(title="Gender")
    plt.savefig('../images/4.png',bbox_inches = 'tight')
    plt.show()


def stackedbar(a):
    #creating space for the number of quintile graphs
    fig, ax = plt.subplots(3, 2, figsize=(12, 12))
    
    #creating a stacked bar chart for each quintile
    for i, quintile in enumerate(sorted(a['Wealth'].unique())):
        # filter the data to only include the current quintile
        quintile_data = a[a['Wealth'] == quintile]
    
        # group the data by year and sex, and calculate the mean literacy rate
        grouped_data = quintile_data.groupby(['year', 'Sex'])['literacy_1524_m'].mean().unstack()
    
        # create the stacked area chart
        ax[i // 2, i % 2].stackplot(grouped_data.index, grouped_data.values.T, labels=grouped_data.columns,colors=['#eb4d4b','#686de0'])
        # grouped_data.plot.area(ax=ax[i], stacked=True)
    
        # set the title and axis labels
        ax[i // 2, i % 2].set_title(f'{quintile}')
        ax[i // 2, i % 2].set_xlabel('Year')
        ax[i // 2, i % 2].set_ylabel('Literacy Rate')
    
        # set the x axis limits
        ax[i // 2, i % 2].set_xlim([a['year'].min(), a['year'].max()])
    
        # add a legend
        ax[i // 2, i % 2].legend(title='Sex')
    ax[2,1].remove()
    # adjust the layout of the subplots
    fig.tight_layout()
    fig.suptitle("Analysis of Wealth and Literacy Rate over the years")
    # show the plot
    plt.tight_layout()
    plt.savefig('../images/5.png',bbox_inches = 'tight')
    plt.show()

def style_polar_axis(ax):
    # Change the initial location of the 0 in radians
    ax.set_theta_offset(np.pi / 2)
    
    # Move in clock-wise direction 
    ax.set_theta_direction(-1)

    # Remove all spines
    ax.set_frame_on(False)

    # Don't use tick labels for radial axis
    ax.set_xticklabels([])
    
    # Set limits for y axis
    ax.set_ylim([0, 4.5])
    # Set ticks for y axis. These determine the grid lines.
    ax.set_yticks([0, 1, 2, 3, 4, 4.5])
    # But don't use tick labels
    ax.set_yticklabels([])
    
    # Set grid with some transparency
    ax.grid(alpha=0.4)

    return ax

def add_labels_polar_axis(ax, color):
    # Define the characteristics of the bbox behind the text we add
    bbox_dict = {
        "facecolor": "w", "edgecolor": color, "linewidth": 1, 
        "boxstyle": "round", "pad": 0.15
    }
    gender = ["male", "female"]
    # Iterate over types of gender and add the labels
    for idx, gen in enumerate(gender):
        ax.text(
            0, idx, gen, color=color, ha="center", va="center",
            fontsize=11, bbox=bbox_dict
        )
    return ax
def plot_circular(axes,melted):
    WEALTH_PALETTES = ["#81C4CA", "#468D96", "#103128", "#FA6E90", "#FCB16D"]
    axes_flattened = axes.ravel()
    wealth = melted['Wealth'].unique()
    
    # Iterate over wealth quintiles and plots
    for i, quintile in enumerate(wealth):
        # Select data for the given quintile
        d = melted[melted['Wealth'] == quintile]
        
        # Select plot
        ax = axes_flattened[i]
        
        # Only for the first panel, add label for vertical axis
        if i == 0:
            ax.set_ylabel("Gender", loc="top")
        
        # Adjust style of the plot
        ax = style_polar_axis(ax)
        
        # Multiply the proportion by the 2pi, the complete rotation 
        proportions = d["literacy_rate"].values * (2 * np.pi)
        
        # Positions for the lines on the radial
        y_pos = np.arange(len(proportions))
        
        # Construct the line for each type of plastic creating a grid for the x and y values
        x = np.linspace(0, proportions, num=200)
        y = np.vstack([y_pos] * 200)

        # Select color
        color = WEALTH_PALETTES[i]
        
        # And finally, plot the rounded lines
        ax.plot(x, y, lw=6, color=color, solid_capstyle="round")
        
        # Add title
        ax.set_title(quintile, pad=10, color="0.3")
        
        # Add labels on top of the lines
        ax = add_labels_polar_axis(ax, color)
    return axes

def print_radial(melted):
    # Initialize layout
    fig, axes = plt.subplots(3, 2, figsize=(8, 12), subplot_kw={"projection": "polar"})

    # Create chart! 
    axes=axes.flatten()[:len(melted['Wealth'].unique())]
    axes = plot_circular(axes,melted)

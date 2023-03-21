import pandas as pd
import numpy as np
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


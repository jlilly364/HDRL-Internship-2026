from itertools import chain
import numpy as np
import os
from pathlib import Path
import pandas as pd
import re

class spase_helio_compare:

    def __init__(self,s):
        pass

def shortResourceDiff(save=False):
    """
    Compare short_name ('ID' on HelioData) in the yml file against SPASE 
    ResourceName column of the spreadsheet and show the differences
    """
    Path.cwd()
    # Read in SPASE observatory name spreadsheet as dataframe
    excel_path = Path.cwd() / 'spase_helio_compare/SPASE_Observatory_Names.xlsx'
    spase_df = pd.read_excel(excel_path)
    #print(spase_df.head)

    # Read in HelioData table as dataframe
    helioData = Path.cwd() / 'spase_helio_compare/helioData.csv'
    helio_df = pd.read_csv(helioData)

    # Get indices where 'short_name' and 'ResourceName' differ
    ind_short_diff = ~helio_df['short_name'].isin(spase_df['ResourceName'])

    # Create new dataframe of mismatched observatory names and write to file 
    shortRes_df = pd.concat([helio_df['short_name'].loc[ind_short_diff],
                    spase_df['ResourceName'].loc[ind_short_diff]],axis=1)
    if save==True:
        shortRes_df.to_csv('spase_helio_compare/short_Resource_diff.csv',index=False)

    return(shortRes_df)

def longAlternateCompare():
    # Read in SPASE observatory name spreadsheet as dataframe
    excel_path = Path.cwd() / 'spase_helio_compare/SPASE_Observatory_AltNames.xlsx'
    spase_df = pd.read_excel(excel_path)

    # Read in HelioData table as dataframe
    helioData = Path.cwd() / 'spase_helio_compare/helioData.csv'
    helio_df = pd.read_csv(helioData)

    """#Convert list that is represented as a string into list
    https://stackoverflow.com/questions/74746796/cannot-understand-why-eval-is-passed-in-as-an-argument-i-e-df-col-name-app"""

    spase_df['AlternateName'] = spase_df['AlternateName'].apply(eval)
    print(spase_df['AlternateName'][1940])
    print(helio_df['long_name'][1940])
    

#spase_helio_compare()
#longAlternateCompare()
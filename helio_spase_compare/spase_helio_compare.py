from itertools import chain
import numpy as np
import os
from pathlib import Path
import pandas as pd
import re

def shortResourceCompare():
    """
    Compare short_name ('ID' on HelioData) in the yml file against SPASE 
    ResourceName column of the spreadsheet and show the differences
    """
    # Read in SPASE observatory name spreadsheet as dataframe
    excel_path = Path.cwd() / 'spase_helio_compare/SPASE_Observatory_AltNames.xlsx'
    spase_df = pd.read_excel(excel_path)
    #print(spase_df.head)

    # Read in HelioData table as dataframe
    helioData = Path.cwd() / 'spase_helio_compare/helioData.csv'
    helio_df = pd.read_csv(helioData)

    """for j, short_name in enumerate(helio_df['short_name']):
        if short_name == spase_df['ResourceName'][j]:
            print(f'{short_name} matches {spase_df['ResourceName'][j]}')
        else:
            print(f'{short_name} DOES NOT MATCH {spase_df['ResourceName'][j]}')"""

    # Get indices where 'short_name' and 'ResourceName' differ
    ind_short_diff = ~helio_df['short_name'].isin(spase_df['ResourceName'])

    # Create new dataframe of mismatched observatory names and write to file 
    new_df = pd.concat([helio_df['short_name'].loc[ind_short_diff],
                    spase_df['ResourceName'].loc[ind_short_diff]],axis=1)
    new_df.to_csv('NEW_COMPARE.csv',index=False)

def longAlternateCompare():
    """
    #Convert list that is represented as a string into list
    https://stackoverflow.com/questions/74746796/cannot-understand-why-eval-is-passed-in-as-an-argument-i-e-df-col-name-app"""

    #spase_df['AlternateName'] = spase_df['AlternateName'].apply(eval)

shortResourceCompare()
from itertools import chain
import numpy as np
import os
from pathlib import Path
import pandas as pd
import re

class spase_helio_compare:

    def __init__(self):
        # Read in SPASE observatory name spreadsheet as dataframe
        self.excel_path = Path.cwd() / 'spase_helio_compare/SPASE_Observatory_Names.xlsx'

        self.spase_df = pd.read_excel(self.excel_path)

        # Read in HelioData table as dataframe
        self.helioData = Path.cwd() / 'spase_helio_compare/helioData.csv'
        self.helio_df = pd.read_csv(self.helioData)

    def shortResourceCompare(self,diff=False,save=False):
        """
        Compare short_name ('ID' on HelioData) in the yml file against SPASE 
        ResourceName column of the spreadsheet and show the differences
        """

        if diff == True:
            # Get indices where 'short_name' and 'ResourceName' differ
            ind_short_diff = ~self.helio_df['short_name'].isin(self.spase_df['ResourceName'])

            # Create new dataframe of mismatched observatory names and write to file 
            shortRes_df = pd.concat([self.helio_df['short_name'].loc[ind_short_diff],self.spase_df['ResourceName'].loc[ind_short_diff]],axis=1)
            if save==True:
                shortRes_df.to_csv('spase_helio_compare/short_Resource_diff.csv',index=False)

        return(self.spase_df['ResourceName'],self.helio_df['short_name'])

    def longAlternateCompare(self,diff=False,save=False):
        """Compare long_name ('Name' on HelioData) in the yml file against SPASE AlternateName column of the spreadsheet and show the differences"""

        """Convert list that is represented as a string into list
        (https://stackoverflow.com/questions/74746796/cannot-understand-why-eval-is-passed-in-as-an-argument-i-e-df-col-name-app)"""
        self.spase_df['AlternateName'] = self.spase_df['AlternateName'].\
            apply(eval)

        if diff == True:
            # Get indices where 'long_name' and 'AlternateName' differ
            ind_long_diff = ~self.helio_df['long_name'].isin(self.spase_df['ResourceName'])

            # Create new dataframe of mismatched observatory names and write to file 
            shortRes_df = pd.concat([self.helio_df['long_name'].loc[ind_long_diff],self.spase_df['ResourceName'].loc[ind_long_diff]],axis=1)
            if save==True:
                shortRes_df.to_csv('spase_helio_compare/short_Resource_diff.csv',index=False)

        return(self.spase_df['AlternateName'],self.helio_df['long_name'])
    
    def fullComparison(self):
        # Call shortResourceDiff function
        spaseResourceNames,helioShortNames = self.shortResourceCompare()

        # Call longAlternateDiff function
        spaseAlternateNames,helioLongNames = self.longAlternateCompare()

        # Combine rows into new dataframe and write it to csv file
        full_df = pd.concat([spaseResourceNames,helioShortNames,
                             spaseAlternateNames,helioLongNames],axis=1,
                             keys=['SPASE_ResourceName','HelioData_short_name',
                                'SPASE_AlternateName', 'HelioData_long_name'])
        full_df.to_csv('spase_helio_compare/all_spase_helioData_names.csv',index=False)
    
# Instantiate class
comparison = spase_helio_compare()

# Call fullComparison funtion
comparison.fullComparison()
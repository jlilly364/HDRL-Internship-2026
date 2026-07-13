from itertools import chain
import numpy as np
import os
from pathlib import Path
import pandas as pd
import re

class spase_helio_compare:

    def __init__(self):
        # Read in SPASE observatory name spreadsheet as dataframe
        self.excel_path = Path.cwd() / 'spase_helio_compare/excel/SPASE_Observatory_Names.xlsx'

        self.spase_df = pd.read_excel(self.excel_path)

        # Read in HelioData table as dataframe
        self.helioData = Path.cwd() / 'spase_helio_compare/csv/helioData.csv'
        self.helio_df = pd.read_csv(self.helioData)

    def shortResourceCompare(self,diff=False,save=False):
        """
        Compare short_name ('ID' on HelioData) in the yml file against SPASE 
        ResourceName column of the spreadsheet and show the differences
        """

        if diff == True:
            # Get indices where 'short_name' and 'ResourceName' differ
            ind_short_diff = ~self.helio_df['short_name'].isin(self.spase_df['ResourceName'])

            # Create new dataframe of differing short and Resource names
            shortRes_df = pd.concat([self.helio_df['short_name'].loc[ind_short_diff],self.spase_df['ResourceName'].loc[ind_short_diff]],axis=1,keys=['HelioData_short_name','SPASE_ResourceName'])

            # Write to file
            if save==True:
                shortRes_df.to_csv('spase_helio_compare/csv/short_Resource_diff.csv',index=False)

                shortRes_df.to_excel('spase_helio_compare/excel/short_Resource_diff.xlsx', index=False)


        return(self.spase_df['ResourceName'],self.helio_df['short_name'])

    def longAlternateCompare(self,diff=False,save=False):
        """Compare long_name ('Name' on HelioData) in the yml file against SPASE AlternateName column of the spreadsheet and show the differences"""

        """Convert list that is represented as a string into list
        (https://stackoverflow.com/questions/74746796/cannot-understand-why-eval-is-passed-in-as-an-argument-i-e-df-col-name-app)"""
        #self.spase_df['AlternateName'] = self.spase_df['AlternateName'].apply(eval)

        # Look for differences in long_name and AlternateName columns
        if diff == True:
            # Create mask where long_names don't appear in AlternateName list
            match_mask = [longName not in altNames for longName, altNames in zip(self.helio_df['long_name'], self.spase_df['AlternateName'])]

            # Create new dataframe of differing long and Alternate names
            longAlt_df = pd.concat([self.spase_df['AlternateName'][match_mask],self.helio_df['long_name'][match_mask]],axis=1,keys=['HelioData_long_name','SPASE_AlternateName'])
            
            # Write to file
            if save==True:
                longAlt_df.to_csv('spase_helio_compare/csv/' \
                'long_Alternate_diff.csv',index=False)

                longAlt_df.to_excel('spase_helio_compare/excel/' \
                                    'long_Alternate_diff.xlsx', index=False)

        return(self.spase_df['AlternateName'],self.helio_df['long_name'])
    
    def fullComparison(self,save=False):
        # Call shortResourceDiff function
        spaseResourceNames,helioShortNames = self.shortResourceCompare()

        # Call longAlternateDiff function
        spaseAlternateNames,helioLongNames = self.longAlternateCompare()

        # Combine rows into new dataframe and write it to csv file
        full_compare_df = pd.concat([helioShortNames,spaseResourceNames, helioLongNames,spaseAlternateNames],axis=1,
                             keys=['HelioData_short_name',
                                   'HelioData_long_name',
                                   'SPASE_AlternateName', 'SPASE_ResourceName'])
        # Write to file
        if save==True:
            full_compare_df.to_csv('spase_helio_compare/csv/all_helioData_spase_names.csv',index=False)

            full_compare_df.to_excel('spase_helio_compare/excel/all_helioData_spase_names.xlsx',index=False)

        return(full_compare_df)
    
# Instantiate class
comparison = spase_helio_compare()

# Call functions
#comparison.shortResourceCompare(diff=True,save=True)
#comparison.longAlternateCompare(diff=True,save=True)
comparison.fullComparison(save=True)
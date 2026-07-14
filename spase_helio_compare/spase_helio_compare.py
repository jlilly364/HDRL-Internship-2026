from pathlib import Path
import pandas as pd

class spase_helio_compare:
    """Compare Observatory naming conventions between SPASE and 
    HelioData (as of July 2026)
    
    HelioData 'short_name' corresponds to SPASE 'ResourceName' and 
    HelioData 'long_name' corresponds to SPASE 'AlternateName', but the
    correspondence is not 1-to-1. This class of functions generates
    comparisons between them, either individually or all together.
    """

    def __init__(self):
        """Initialize class with HelioData and SPASE name databases"""

        # Read in SPASE observatory name spreadsheet as dataframe
        self.excel_path = Path.cwd() / 'spase_helio_compare/excel/SPASE_Observatory_Names.xlsx'

        self.spase_df = pd.read_excel(self.excel_path)

        # Read in HelioData table as dataframe
        self.helioData = Path.cwd() / 'spase_helio_compare/csv/helioData.csv'
        self.helio_df = pd.read_csv(self.helioData)

    def shortResourceCompare(self,diff=False,save=False):
        """Compare short_name (HelioData 'ID') to SPASE 'ResourceName'
        
        :param diff: User choice to save file showing differences, 
                        defaults to = False
        :type diff: boolean 
        :param save: User choice to save comparison file, 
                        defaults to False
        :type save: boolean

        :return: SPASE ResourceNames and HelioData short_names
        :rtype: pd.DataFrame
        """

        # Create file with short_names and ResourceNames that differ
        if diff:
            # Get indices where 'short_name' and 'ResourceName' differ
            ind_short_diff = ~self.helio_df['short_name']\
                                .isin(self.spase_df['ResourceName'])

            # Create dataframe by combining masked columns
            shortRes_df = pd.concat([self.helio_df['short_name']
                                     .loc[ind_short_diff],
                                     self.spase_df['ResourceName']
                                     .loc[ind_short_diff]],axis=1,
                                     keys=['HelioData_short_name',
                                           'SPASE_ResourceName'])

            # Write to file
            if save:
                shortRes_df.to_csv('spase_helio_compare/csv/short_Resource_diff.csv',
                                   index=False)

                shortRes_df.to_excel('spase_helio_compare/excel/short_Resource_diff.xlsx',
                                     index=False)

        return(self.spase_df['ResourceName'],self.helio_df['short_name'])

    def longAlternateCompare(self,diff=False,save=False):
        """Compare long_name (HelioData 'Name') to SPASE 'AlternateName'
        
        :param diff: User choice to save file showing differences, 
                        defaults to = False
        :type diff: boolean 
        :param save: User choice to save comparison file, 
                        defaults to False
        :type save: boolean

        :return: SPASE AlternateNames and HelioData long_names
        :rtype: pd.DataFrame
        """

        """Convert list that is represented as a string into list
        (https://stackoverflow.com/questions/74746796 cannot-understand-why-eval-is-passed-in-as-an-argument-i-e-df-col-name-app)"""
        #self.spase_df['AlternateName']=self.spase_df['AlternateName']\
            #.apply(eval)

        # Create file with long_names and AlternateNames that differ
        if diff:
            # Create mask where long_names don't appear in 
            # AlternateName list
            match_mask = [longName not in altNames for longName, altNames in 
                          zip(self.helio_df['long_name'], 
                              self.spase_df['AlternateName'])]

            # Create new dataframe of differing long and Alternate names
            longAlt_df = pd.concat([self.helio_df['long_name'][match_mask],
                                    self.spase_df['AlternateName'][match_mask]]
                                    ,axis=1,keys=['HelioData_long_name',
                                                  'SPASE_AlternateName',])
            
            # Write to file
            if save:
                longAlt_df.to_csv('spase_helio_compare/csv/' \
                'long_Alternate_diff.csv',index=False)

                longAlt_df.to_excel('spase_helio_compare/excel/' \
                                    'long_Alternate_diff.xlsx', index=False)

        return(self.spase_df['AlternateName'],self.helio_df['long_name'])
    
    def fullComparison(self,save=False):
        """Generate and combine DataFrames for all naming conventions
        
        :param save: User choice to save comparison file, 
                        defaults to False
        :type save: boolean

        :return: Full DataFrame with all Observatory name comparisons
        :rtype: pd.DataFrame
        """
        
        # Call shortResourceDiff function
        spaseResourceNames,helioShortNames = self.shortResourceCompare()

        # Call longAlternateDiff function
        spaseAlternateNames,helioLongNames = self.longAlternateCompare()

        # Combine rows into new dataframe with appropriate column names
        full_compare_df = pd.concat([helioShortNames,spaseResourceNames, 
                                     helioLongNames,spaseAlternateNames],
                                     axis=1,
                             keys=['HelioData_short_name',
                                   'SPASE_ResourceName',
                                   'HelioData_long_name',
                                   'SPASE_AlternateName'])
        # Write to file
        if save:
            full_compare_df.to_csv('spase_helio_compare/csv/all_helioData_\
                                   spase_names.csv',index=False)

            full_compare_df.to_excel('spase_helio_compare/excel/all_helioData_\
                                     spase_names.xlsx',index=False)

        return(full_compare_df)

if __name__ == "__main__":    
    # Instantiate class
    comparison = spase_helio_compare()

    # Call functions
    comparison.shortResourceCompare(diff=True,save=True)
    comparison.longAlternateCompare(diff=True,save=True)
    comparison.fullComparison(save=True)
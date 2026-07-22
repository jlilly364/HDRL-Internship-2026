from pathlib import Path
import pandas as pd


class spase_helio_update:
    """Compare Observatory naming conventions between SPASE and
    HelioData (as of July 2026)

    HelioData 'short_name' corresponds to SPASE 'ResourceName' and
    HelioData 'long_name' corresponds to SPASE 'AlternateName', but the
    correspondence is not 1-to-1. This class of functions generates
    comparisons between them, either individually or all together.
    """

    def __init__(self):
        """Initialize class with databse of HelioData and SPASE
        Mission/Observatory names"""

        self.all_names = Path.cwd() /"spase_helio_compare/csv/all_helioData_spase_names.csv"
        self.all_names_df = pd.read_csv(self.all_names)

    """def shortResourceCompare(self,diff=False,save=False):
        #Compare short_name (HelioData 'ID') to SPASE 'ResourceName'
        
        :param diff: User choice to save file showing differences, 
                        defaults to = False
        :type diff: boolean 
        :param save: User choice to save comparison file, 
                        defaults to False
        :type save: boolean

        :return: SPASE ResourceNames and HelioData short_names
        :rtype: pd.DataFrame
        #
        

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
    
    """

    def longAlternateUpdate(self, save=False):
        """Add and/or move long_name (HelioData 'Name') to first element
        of  SPASE 'AlternateName' list

        :param save: User choice to save comparison file,
                        defaults to False
        :type save: boolean

        :return: SPASE AlternateNames and HelioData long_names
        :rtype: pd.DataFrame
        """

        # Extract long_name columns
        longNames = self.all_names_df["HelioData_long_name"]

        """Convert list that is represented as a string into list
        (https://stackoverflow.com/questions/74746796/cannot-understand\
        -why-eval-is-passed-in-as-an-argument-i-e-df-col-name-app)"""
        altNames = self.all_names_df["SPASE_AlternateName"]
        altNames = altNames.apply(eval)

        # Check for presence and location of long_name in AlternateNamelist
        for i in self.all_names_df.index:
            # If AlternateName list is empty, use long_name
            if altNames.at[i] == [""]:
                print(f"AlternateName list empty. Using long_name={longNames[i]}\n")
                altNames.at[i] = [longNames[i]]

            # If longName isn't first element of AlternateName list...
            elif longNames[i] != altNames[i][0]:
                # If longName not present at all, include as 1st element
                if longNames[i] not in altNames[i]:
                    print(f"long_name ('{longNames[i]}') not in AlternateName\
                            list. Putting it in front")
                    altNames[i].insert(0, longNames[i])

                # If longName present, but not first, move it to front
                elif longNames[i] in altNames[i]:
                    # Find the index of longName and move it to front
                    idx = altNames[i].index(longNames[i])
                    altNames[i].insert(0, altNames[i].pop(idx))
                    print(f"long_name present at index={idx}. Moving to front")
            else:
                print("long_name matches first element of AlternateName list!\n")

        # Create new dataframe of differing long and Alternate names
        longAlt_update_df = pd.concat([longNames, altNames],axis=1,
                                      keys=["HelioData_long_name",
                                            "SPASE_AlternateName"])

        # Write to file
        if save:
            longAlt_update_df.to_csv("spase_helio_compare/csv/long_Alternate_update.csv", index=False)

            longAlt_update_df.to_excel("spase_helio_compare/excel/long_Alternate_update.xlsx", index=False)

        # return(self.spase_df['AlternateName'],self.helio_df['long_name'])"""


if __name__ == "__main__":
    # Instantiate class
    comparison = spase_helio_update()

    comparison.longAlternateUpdate(True)

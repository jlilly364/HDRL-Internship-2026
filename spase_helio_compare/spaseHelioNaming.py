from rapidfuzz import fuzz, distance
from pathlib import Path
import pandas as pd

class spaseHelioNaming:
    """Compare Observatory naming conventions between SPASE and 
    HelioData (as of July 2026)
    
    HelioData 'short_name' corresponds to SPASE 'ResourceName' and 
    HelioData 'long_name' corresponds to SPASE 'AlternateName', but the
    correspondence is not 1-to-1. This class of functions generates
    comparisons between them, either individually or all together.
    """

    def __init__(self,spaseField,nameFile="all_spase_helioData_names.csv"):
        """Initialize class with HelioData and SPASE name databases
        
        :param spaseField: SPASE name field of interest
        :type spaseField: string
        """

        # Read in file with all current HelioData and SPASE names
        self.allNames = Path.cwd() / f"spase_helio_compare/csv/{nameFile}"
        self.allNames_df = pd.read_csv(self.allNames)

        # Initialize name of SPASE and HelioData field
        self.spaseField = spaseField
        self.helioField = ""
        if self.spaseField == ("Resource"):# or "ResourceID"
            self.helioField = "short"
        elif self.spaseField == "Alternate":
            self.helioField = "long"
        else:
            raise ValueError("Not a valid SPASE naming field")
        print(self.spaseField,self.helioField)

    def spaseHelioCompare(self,save=False):
    #def shortResourceCompare(self,diff=False,save=False):
        """Compare short_name (HelioData 'ID') to SPASE 'ResourceName'
        
        :param save: User choice to save comparison file, 
                        defaults to False
        :type save: boolean

        :return: SPASE ...Names and HelioData ..._names
        :rtype: pd.DataFrame
        """

        resourceIDs = self.allNames_df["SPASE_ResourceID"]
        spaseNames = self.allNames_df[f'HelioData_{self.helioField}_name']
        helioNames = self.allNames_df[f'SPASE_{self.spaseField}Name']

        indMask = []     
        j = 0   
        # Get indices where names differ
        indMask = ~self.allNames_df[f'HelioData_{self.helioField}_name']\
                    .isin(self.allNames_df[f'SPASE_{self.spaseField}Name'])
        # for spaseName, helioName in zip(spaseNames,helioNames):
        #     spaseName_clean = spaseName.replace(" ", "").replace("-", "").replace("/", "")
        #     helioName_clean = helioName.replace(" ", "").replace("-", "").replace("/", "")

        #     if spaseName_clean != helioName_clean:
        #         j += 1
        #         print(f"{spaseName} != {helioName}")
        # print(f"{j} names that differ by more than hyphen,slash, or space")

        
        # Create DataFrame with SPASE and HelioData names that differ
        masked_df = pd.concat([resourceIDs.loc[indMask],
                               spaseNames.loc[indMask],
                               helioNames.loc[indMask]],
                               axis=1,keys=["SPASE_ResourceID",
                                            f'SPASE_{self.spaseField}Name',
                                            f'HelioData_{self.helioField}_name'])

        # Write to file
        if save:
            masked_df.to_csv(f'spase_helio_compare/csv/{self.spaseField}_{self.helioField}_diff.csv',
                                index=False)
            print("Comparison file successfully generated")

            """compare_df.to_excel(f'spase_helio_compare/excel/\
                                {self.spaseField}_{self.helioField}_diff.xlsx',
                                index=False)"""

        #return(indMask)

    def spaseHelioUpdate(self,save=False):
        """Add and/or move long_name (HelioData 'Name') to first element
        of  SPASE 'AlternateName' list

        :param save: User choice to save comparison file,
                        defaults to False
        :type save: boolean

        :return: Updated SPASE names
        :rtype: pd.DataFrame
        """

        # Initialize lists of SPASE ResourceIDs & names and HelioData names
        resourceIDs = self.allNames_df["SPASE_ResourceID"]
        spaseNames = []
        helioNames = self.allNames_df[f"HelioData_{self.helioField}_name"]

        if self.spaseField == "Alternate":
            """Convert list that is represented as a string into list
            (https://stackoverflow.com/questions/74746796/cannot-understand\
            -why-eval-is-passed-in-as-an-argument-i-e-df-col-name-app)"""
            spaseNames = self.allNames_df[f"SPASE_{self.spaseField}Name"].apply(eval)

            # Check for presence and location of long_name in
            # AlternateName list
            for i in self.allNames_df.index:

                # If AlternateName list is empty, use long_name
                if spaseNames.at[i] == [""]:
                    print(f"{self.spaseField}Name list empty. Using {self.helioField}={helioNames[i]}\n")
                    spaseNames.at[i] = [helioNames[i]]

                # If longName isn't first element of AlternateName list...
                elif helioNames[i] != spaseNames[i][0]:

                    # If longName not present at all, include as 1st element
                    if helioNames[i] not in spaseNames[i]:
                        print(f"{self.helioField} ('{helioNames[i]}') not in\
                              {self.spaseField}Name list. Putting it in front")
                        spaseNames[i].insert(0, helioNames[i])

                    # If longName present, but not first, move it to front
                    elif helioNames[i] in spaseNames[i]:
                        # Find the index of longName and move it to front
                        idx = spaseNames[i].index(helioNames[i])
                        spaseNames[i].insert(0, spaseNames[i].pop(idx))
                        print(f"{self.helioField} present at index={idx}. Moving to front")
                else:
                    print(f"{self.helioField}_name matches first element of {self.spaseField}Name list!\n")

            # Create new dataframe of differing Alternate and long names
            updated_df = pd.concat([resourceIDs,spaseNames,helioNames],axis=1,
                                    keys=["SPASE_ResourceID",
                                          f"SPASE_{self.spaseField}Name",
                                          f"HelioData_{self.helioField}_name"])

        elif self.spaseField == "Resource":
            spaseNames = self.allNames_df[f"SPASE_{self.spaseField}Name"]

            for i in self.allNames_df.index[:100]:
                if helioNames[i] != spaseNames[i]:
                    #spaseNames.at[i] = helioNames[i]
                    if helioNames[i] not in spaseNames[i]:
                        charDiff = distance.Levenshtein.distance(helioNames[i],spaseNames[i])
                        if charDiff > 1:
                            print(f"{helioNames[i]} | {spaseNames[i]} (charDiff = {charDiff})")
                            spaseNames.at[i] = helioNames[i]
                        #print(f">Character diff = {distance.Levenshtein.distance(helioNames[i],spaseNames[i])}\n")
                    """
                        if distance.Levenshtein.distance(helioNames[i],spaseNames[i]):
                            print(f"\n>{self.helioField}_name ('{helioNames[i]}') not in {self.spaseField}Name ('{spaseNames[i]}').\n")
                    else:
                        print(f"\n{self.helioField}_name ('{helioNames[i]}') different than {self.spaseField}Name ('{spaseNames[i]}').\n")"""
                else:
                    print(f"Match! {self.helioField}_name ('{helioNames[i]}') same as {self.spaseField}Name ('{spaseNames[i]}').")

            # Create new dataframe of differing Resource and short names
            updated_df = pd.concat([spaseNames,helioNames],axis=1,
                                    keys=[f"SPASE_{self.spaseField}Name",
                                          f"HelioData_{self.helioField}_name"])
        
        # Write to file
        if save:
            updatedFile = f"{self.spaseField}_{self.helioField}_update.csv"
            updated_df.to_csv(f"spase_helio_compare/csv/TEST_{updatedFile}",index=False)

if __name__ == "__main__":    
    # Instantiate class
    #comparison = spaseHelioNaming(spaseField="Alternate")
    comparison = spaseHelioNaming(spaseField="Resource")

    # Call functions
    comparison.spaseHelioCompare(save=True)
    #INDMAX = comparison.spaseHelioCompare(save=False)
    #print(len(INDMAX))
    #comparison.spaseHelioUpdate(save=True)
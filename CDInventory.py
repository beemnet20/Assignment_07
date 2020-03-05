#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# BWorkeneh, 2020-Feb-26, completed the TODOs in the starter code 
# BWorkeneh, 2020-Mar-4, added Exception Handling 
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """ Processing the information in memory """
    @staticmethod
    def add_cd(table):
        """ function to add a CD to the inventory
        Tells user to enter an integer if a value that cannot be type cast to 
        integer is entered
        Args:
            table: the list of dictionaries containing the CD entries
            
        Returns: 
            the modified list of dictionaries with new etries of CDs
        """
        
        try:
            strID = input('Enter ID: ').strip()
            intID = int(strID)
       
        except ValueError as e:
            print('<<< custom error message \nThat is not an integer!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep= '\n')
            print('\n Enter an integer for the ID: ')
            strID = input('Enter ID: ').strip()
            intID = int(strID)
        #it is possible to add custom exception handling for repeated CD ID
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        # Add item to the table
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
        table.append(dicRow)
        return table
    @staticmethod
    def delete_cd(table, ID):
        """ function to delete an entry from the inventory
        
            Args:
                table: the list of dictionaries containing the CD entries
                ID: the integer ID of the CD to be deleted
                
            Returns: 
                the modified list of dictionaries with the entry containing the ID removed
            """

        # search thru table and delete CD
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == ID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return table 

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        If the file does not exist it creates it by using Exception handling

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try: 
            objFile = open(file_name, 'r')
        except FileNotFoundError as e:
            print('<<< custom error message \n the file is not found')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep= '\n')
            print('Creating ', file_name)
            objFile = open(file_name, 'w')# create the file
            objFile.close()
        objFile = open(file_name, 'r') # re-opening incase there was a FileNotFoundError 
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close() 
               

    @staticmethod
    def write_file(file_name, table):
        """Function to write data that is in a list of dictionaries to a text file
        
        Reads the data from the list of dictionaries and writes into a file identified by file_name ad
        rows of comma delimited items. 
        
        Args:
            file_name(string): name of file used to write the data to
            table( list of dict): 2D data structure (list of dicts) that holds the data during runtime 
            
        Returns: 
            None.
        """
        # write mode used to open the file, will create the file if it is not found, no exception hadndling necessary
        objFile = open(file_name, 'w')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()
    


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        # the condition of the while loop below is sort of a custom exception handling
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')


# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        lstTbl = DataProcessor.add_cd(lstTbl) # pass list of dictionaries to the add_cd function to have new entries appended 
        IO.show_inventory(lstTbl)  
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # get Userinput for which CD to delete
        # display Inventory to user
        IO.show_inventory(lstTbl)
        # ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        lstTbl = DataProcessor.delete_cd(lstTbl, intIDDel) # pass the list of dictionaries and ID to the delete_cd function to have entries removed 
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
       # IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')





#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
    # DBiesinger, 2030-Jan-01, Created File
    # Jerry Hsish, 2022-Mar-03, Modified
    # Jerry Hsieh, 2022-Mar-10, Add Structured error handling
    # Jerry Hsieh, 2022-Mar-12, Add Binary Data storage
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    # 3.3.1 Ask user for new ID, CD Title and Artist
    # Store CD ID/title/Artist, return 2D-table lstTbl
    def add_file(intID, strTitle, stArtist):
        """Function to add CD data to memory
        Args:
            intID, strTitle, stArtist
        Returns:
            table: 2D lsit of dict
        """
        # 3.3.2 Add item to the table
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
        lstTbl.append(dicRow)
        for row in lstTbl:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        return lstTbl
        pass

    def delete_file(table):
        """Function to delete CD data row from memory
        """
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user      
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        # Delete the row which matches the input ID value
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        #Error Handling when user input wrong CD ID for deletion
        try:
            if blnCDRemoved == True:
                print('The CD number ',intIDDel,' was removed')
            if blnCDRemoved == False:
                raise Exception
        except Exception:
            print('Could not find this CD! Try to delete again!')
        return table

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to read stored binary data
        Args:
            file_name (string): name of file used to read the data from
            table: list of dict
        Returns:
            table: 2D lsit of dict
        """
        table.clear()  
        # load binary data from .dat file
        with open(file_name,'rb') as file:
           table = pickle.load(file)
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function to save binary data
        Args:
            file_name (string): name of file used to save the data
        Returns:
            None
        """
        # 3.6.1 Display current inventory and ask user for confirmation to save
        # Error Handling if user doesnt enter anything
        while True:
            try:
                strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
                if not strYesNo:
                    raise Exception
                break
            except Exception:
                print('Didn\'t enter anything! Type again!!')
        # 3.6.2 Process choice 'y'
        # save data in binary form
        if strYesNo == 'y':
            with open(file_name,'wb') as file:
                pickle.dump(table, file, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """
        Displays a menu of choices to the user
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection
        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        
        #Error Handling if user doesnt enter anything in [l, a, i, d, s, x]
        while True:
            try:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
                if (choice == 'a') or (choice == 'l') or(choice == 'i') or(choice == 'd') or(choice == 's') or(choice == 'x'):
                    break
                else: raise Exception
            except Exception:
                print('invalid choice!! try again!!')
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
    # define CD input as a function, in class IO, return 3 ID/Title/Artist.
    def CDInput():
        """User Enter CD data
        Returns: intID, strTitle,stArtist
        """
        while True:
            strID = input('Enter ID: ').strip()
            #Error Handling if user enter non-numeric value
            try:
                intID = int(strID)
                break
            except ValueError:
                print('This is not an integer! Enter again!')
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, stArtist

# 1. When program starts, read in the currently saved Inventory
# Error Hadling if no CDInventory.dat file found
while True:
    flag = False      # Use flag to decide when to break the loop
    try:
        FileProcessor.read_file(strFileName, lstTbl)
    except FileNotFoundError:
        print('File Not Found!!!\n')
        break
    else:
        # 2. start main loop
        while True:
        # 2.1 Display Menu to user and get choice
            IO.print_menu()
            strChoice = IO.menu_choice()
        # 3. Process menu selection
        # 3.1 process exit first
            if strChoice == 'x':
                flag = True           #if flag==True, break the loop
                break
        # 3.2 process load inventory
            if strChoice == 'l':
                print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
                strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled:\n')
                if strYesNo.lower() == 'yes':
                    print('reloading...')
                    lstTbl = FileProcessor.read_file(strFileName, lstTbl)
                    IO.show_inventory(lstTbl)
                else:
                    input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                continue  # start loop back at top.
        # 3.3 process add a CD
        # Everytine we call IO.CDInput, it will return 3 values(ID/title/artist)
        # Then use .add_file to process these 3 values (add function)
            elif strChoice == 'a':
                D1,D2,D3 = IO.CDInput()
                DataProcessor.add_file(D1,D2,D3)
                continue  # start loop back at top.
        # 3.4 process display current inventory
            elif strChoice == 'i':
                IO.show_inventory(lstTbl)
                continue  # start loop back at top.
        # 3.5 process delete a CD
        # Call .delete_file to process delete function
            elif strChoice == 'd':
                DataProcessor.delete_file(lstTbl)
                continue  # start loop back at top.
        # 3.6 process save inventory to file
        # Call .write_file to process save function
            elif strChoice == 's':
                FileProcessor.write_file(strFileName, lstTbl)
                continue  # start loop back at top.
        # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
            else:
                print('General Error')
    if flag == True:             # if user enter 'x', flag==True then break all while loop
            break





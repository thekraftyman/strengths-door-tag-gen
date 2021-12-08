# gui.py
# By: thekraftyman

import tkinter as tk
from tkinter import filedialog

class GeneratorGUI:
    '''
    container class for the door tag generator in GUI form
        built using tkinter
    '''

    def __init__( self ):
        self._components = {}
        self._created = False

    def _create( self ):
        # Create the gui object
        self.window = tk.Tk()

        # Set the title
        self.window.title('Strengths Door Tag Generator')

        # Set the main label
        self._components['csv_label'] = tk.Label( self.window, text="CSV Tag Generator", font=("Arial Bold", 20) )
        self._components['csv_label'].grid(column=0,row=0)

        # Add the infile label
        self._components['infile_label'] = tk.Label( self.window, text="Input CSV File: ")
        self._components['infile_label'].grid(column=0,row=1)

        # Add the infile text box
        self._components['infile_entry'] = tk.Entry( self.window, width=30 )
        self._components['infile_entry'].grid(column=1,row=1)

        # Add the infile file browser button
        self._components['infile_browser'] = tk.Button( self.window, text="Browse", command=self.update_infile )
        self._components['infile_browser'].grid(column=2,row=1)

        # Add the outfile label
        # ...

        # Add the outfile text box
        # ...

        # Add the outfile file browser
        # ...

        # Add the "Fronts" checkbox
        # ...

        # Add the "Generate" button
        # ...

        # set created to true
        self._created = True

    def update_infile( self ):
        ''' updates the infile entry box with the results from browse_csv '''
        filename = self.browse_csv()
        ndel = len(self._components['infile_entry'].get())
        self._components['infile_entry'].delete(0,ndel)
        self._components['infile_entry'].insert(0,filename)

    def browse_csv( self ):
        '''
        Browse for a csv file, returns string of full path to file
        '''
        filename = filedialog.askopenfilename(
            parent=self.window,
            title="Select CSV to Import Data From",
            filetypes=[("CSV Files","*.csv")]
        )
        return filename

    def browse_pdf( self ):
        '''
        Place to save pdf file, returns full path to file
        '''
        filename = filedialog.asksaveasfilename(
            parent=self.window,
            title="Select PDF Destination and Name",
            filetypes=[("PDF Files","*.pdf")]
        )
        return filename

    def run( self ):
        # Start the window main loop
        if not self._created:
            self._create()
        self.window.mainloop()

if __name__ == '__main__':
    gui = GeneratorGUI()
    gui.run()

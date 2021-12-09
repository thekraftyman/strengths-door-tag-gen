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
        self._components['csv_label'].grid(column=1,row=0)

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
        self._components['outfile_label'] = tk.Label( self.window, text="Output PDF File: ")
        self._components['outfile_label'].grid(column=0,row=2)

        # Add the outfile text box
        self._components['outfile_entry'] = tk.Entry( self.window, width=30 )
        self._components['outfile_entry'].grid(column=1,row=2)

        # Add the outfile file browser
        self._components['outfile_browser'] = tk.Button( self.window, text="Browse", command=self.update_outfile )
        self._components['outfile_browser'].grid(column=2,row=2)

        # Add the "Fronts" checkbox
        self._components['fronts_var'] = tk.IntVar()
        self._components['fronts_checkbox'] = tk.Checkbutton( self.window, variable=self._components['fronts_var'] )
        self._components['fronts_checkbox'].grid(column=0,row=3)

        # "Fronts" Label
        self._components['fronts_label'] = tk.Label( self.window, text="Only generate front sides (for single-side printing)" )
        self._components['fronts_label'].grid(column=1,row=3)

        # Add the "Generate" button
        self._components['generate_button'] = tk.Button( self.window, text="Generate", command=self.generate )
        self._components['generate_button'].grid(column=0, row=4)

        # Add completion text (blank by default)
        self._components['completion_var'] = tk.StringVar()
        self._components['completion_label'] = tk.Label( self.window, textvariable=self._components['completion_var'] )
        self._components['completion_label'].grid( column=1,row=4 )

        # set created to true
        self._created = True

    def update_completion_text( self, text ):
        ''' updates the completion label with a given text '''
        self._components['completion_var'].set( text )

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

    def update_outfile( self ):
        ''' updates the outfile entry box with the result from browse_pdf '''
        filename = self.browse_pdf()
        ndel = len( self._components['outfile_entry'].get() )
        self._components['outfile_entry'].delete(0,ndel)
        self._components['outfile_entry'].insert(0,filename)

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

    def generate( self ):
        '''
        Generate pdf. To be overridden by child class
        '''
        pass

    def run( self ):
        # Start the window main loop
        if not self._created:
            self._create()
        self.window.mainloop()

if __name__ == '__main__':
    gui = GeneratorGUI()
    gui.run()

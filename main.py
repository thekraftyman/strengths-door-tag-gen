# main.py
# By: thekraftyman

from src.gui import GeneratorGUI
from src.tag import Tag
from src.page import Page
from src.data_reader import DataEngine
from os import path

class StrengthsGUI( GeneratorGUI ):
    ''' gui that incorperates the generators for tags and pages '''

    def generate( self ):
        '''
        Generate the pdf
        '''
        # Get the input file
        infile = self.infile

        # Check that the file exists
        if not path.exists( infile ):
            raise Exception(f"File specified does not exist: {infile}")

        # Get the output name
        outfile = self.outfile

        # Check that it doesn't already exist
        if path.exists( outfile ):
            raise Exception( f"Output file already exists: {outfile}" )

        # Process using DataEngine
        de = DataEngine( infile )

        # Iterate through DataEngine to generate the tags/pages
        sets = []
        for i in range( 0, len(de)-1, 2 ):
            td1  = de[i]
            tag1 = Tag(
                first_name=td1['First Name'],
                last_name=td1['Last Name'],
                t1=td1['Talent 1'],
                t2=td1['Talent 2'],
                t3=td1['Talent 3'],
                t4=td1['Talent 4'],
                t5=td1['Talent 5']
            )
            tag1.generate_tag()

            td2 = de[i+1]
            tag2 = Tag(
                first_name=td2['First Name'],
                last_name=td2['Last Name'],
                t1=td2['Talent 1'],
                t2=td2['Talent 2'],
                t3=td2['Talent 3'],
                t4=td2['Talent 4'],
                t5=td2['Talent 5']
            )
            tag2.generate_tag()

            page = Page()
            page.generate_pages( tag1, tag2 )
            sets.append( page )

        # Flatten pages array
        pages = []
        for page in sets:
            pages.append( page.page1 )
            pages.append( page.page2 )

        # Save the pdf
        pages[0].save( outfile, save_all=True, append_images=pages[1:] )

        # Update the label on the gui
        self.update_completion_text( "File Saved!" )

if __name__ == "__main__":
    gui = StrengthsGUI()
    gui.run()

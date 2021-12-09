# page.py
# By: thekraftyman

from PIL import Image, ImageFont, ImageDraw, ImageOps

class Page:
    ''' Page container used to compile tag(s) into a printable document '''

    # Globals for this class
    page_width = 1584 #792 # 11"
    page_height = 1224 #612 # 8.5"

    def __init__(self):
        self.size = (self.page_width, self.page_height)
        self.generated = False

    def generate_pages( self, tag1, tag2 ):
        ''' generate the pages, return a tuple of 2 images '''
        # create the blank template
        page1 = Image.new( 'RGB', self.size, color='white' )

        # calculate margins and paste
        margin = round( (self.size[0] - tag1.size[0]) / 2 )
        page1.paste( tag1.front , (margin, margin) )

        # put second tag on
        y2 = round(self.size[1] - tag2.size[1]- margin)
        page1.paste( tag2.front, (margin, y2))

        # create a second page
        page2 = Image.new( 'RGB', self.size, color='white' )

        page2.paste( tag1.back, (margin, margin) )
        page2.paste( tag2.back, (margin, y2) )

        self.page1, self.page2 = page1, page2 # save to object

        self.generated = True # allow for saving

    def save_tags( self, save_name, save_back=True ):
        ''' takes 2 tags and saves them to a pdf '''
        if not self.generated:
            raise Exception( "You must generate the pages before saving" )

        # save and return if not putting second page on
        if not save_back:
            self.page1.save( save_name )
            return

        self.page1.save( save_name, save_all=True, append_images=[self.page2] )

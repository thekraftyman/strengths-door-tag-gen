# tag.py
# By: thekraftyman

from PIL import Image, ImageFont, ImageDraw, ImageOps
import os
class Tag:
    ''' Tag container. Generates the pdf for a given individual '''
    # Globals for the class
    page_width = 792
    page_height = 612
    if os.path.isdir( 'img' ):
        img_path = 'img/'
    elif os.path.isdir( '../img' ):
        img_path = '../img/'
    else:
        raise Exception( "Could not find image directory from", os.pwd() )
    img_extension = '.jpg'

    # tag info
    #tag_size     = ( 730, 201 )
    tag_size     = ( 1460, 402 )
    border_width = round( tag_size[0] * 0.004109589 )
    border_color = "#231F20" # rgb(35,31,32)
    font_color   = "#353132" # rgb(53,49,50)

    # image dimensions
    str_img_size         = ( int(tag_size[0]/5) , round(tag_size[1] * 0.84577) )
    str_image_total_size = ( tag_size[0], str_img_size[1] )

    # text box info
    tb_pos       = ( round( tag_size[0] * 0.005479 ), round(tag_size[1] * 0.88059) )
    tb_font_size = round( tag_size[0] * 0.028767 )
    tb_size      = ( tag_size[0], int(tag_size[1]-str_img_size[1]) )
    tb_offset    = ( tb_pos[0], abs(int( (tb_size[1]-tb_font_size)/2 )-3) )
    font = 'Moonglade'
    if os.path.exists( f'{font}.ttf' ):
        tb_font = f'{font}.ttf'
    elif os.path.exists( f'fonts/{font}.ttf' ):
        tb_font = f'fonts/{font}.ttf'
    elif os.path.exists( f'../fonts/{font}.ttf' ):
        tb_font = f'../fonts/{font}.ttf'
    else:
        raise Exception( f"Cannot load font: {font}" )

    # tag back default
    tag_back_name = "strengths_tag_back.png"


    def __init__( self, first_name=None, last_name=None, t1=None, t2=None, t3=None, t4=None, t5=None, tag_back_path=None ):
        self.first_name = first_name
        self.last_name = last_name
        self.talent_1 = t1
        self.talent_2 = t2
        self.talent_3 = t3
        self.talent_4 = t4
        self.talent_5 = t5
        self.tag = None
        self._tag_back_path = None
        self._tag_back = None

    @property
    def tag_front( self ):
        return self.tag

    @property
    def tag_back( self ):
        if not self._tag_back:
            self._load_tag_back()

        return self._tag_back

    def needs_data( self ):
        ''' checks if data needs to be populated. Returns boolean '''
        if self.first_name and self.last_name and self.talent_1 and self.talent_2 and self.talent_3 and self.talent_4 and self.talent_5:
            return False
        return True

    def get_strength_img( self, strength ):
        ''' returns the path to an image from a corresponding strength string '''
        # make sure the strength starts with a capital
        strength = strength[0].upper() + strength[1:]
        fname = self.img_path + strength + self.img_extension
        if os.path.exists( fname ):
            return fname
        else:
            raise Exception( "Could not find file" ,fname )

    def generate_tag( self, save=False ):
        '''generates the tag'''
        # check for data
        if self.needs_data():
            print( "Tag required data before generation" )
            return

        # get generated components
        strengths_image = self._generate_strengths_image()
        textbox = self._generate_textbox()

        # Add border to textbox
        textbox = ImageOps.expand( textbox, border=(0, self.border_width, 0, 0), fill=self.border_color)

        # combine generated components
        tag = Image.new( 'RGB', self.tag_size )
        tag.paste( strengths_image, (0, 0) )
        tag.paste( textbox, (0, self.str_image_total_size[1] ) )

        # Add border to entire tag
        tag = ImageOps.expand( tag, border=self.border_width, fill=self.border_color)

        ## FOR DEBUGGING ---------
        #tag.show()
        ## -----------------------

        # save the tag to the object
        self.tag = tag

        # save the image (if save is set to a string)
        if save:
            tag.save( save )

    def _generate_strengths_image( self ):
        ''' to be called by self.generate_tag. Returns a PIL image of all of the strengths side by side'''
        # get assets
        strengths = [ self.talent_1, self.talent_2, self.talent_3, self.talent_4, self.talent_5 ]
        str_img_paths = [ self.get_strength_img( strength ) for strength in strengths ]
        strengths_images = [ Image.open( image ) for image in str_img_paths ]

        # scale the assets to the correct dimensions
        strengths_images = [ image.resize( self.str_img_size ) for image in strengths_images ]

        # Concatinate the images to make one large image of strengths
        strengths_image = Image.new( 'RGB', self.str_image_total_size )
        for i, img in enumerate(strengths_images):
            x_offset = self.str_img_size[0] * i
            strengths_image.paste( img, (x_offset, 0))

        # return the image
        return strengths_image

    def _generate_textbox( self ):
        ''' generates a textbox with the first/last name called by self.generate_tag. Returns a PIL image.'''
        name = self.first_name.strip() + ' ' + self.last_name.strip()

        # create image
        img = Image.new( 'RGB', self.tb_size, color='white' )

        # add text
        draw = ImageDraw.Draw( img )
        font = ImageFont.truetype( self.tb_font, self.tb_font_size )
        draw.text( self.tb_offset, name, self.font_color, font=font)

        # return the image
        return img

    def _load_tag_back( self ):
        ''' loads the back of the tag and scales to the same size as the font '''
        if self._tag_back_path:
            # already given
            tb_path = self._tag_back_path
        else:
            # guess with default
            if os.path.exists( f'{self.tag_back_name}' ):
                tb_path = f'{self.tag_back_name}'
            elif os.path.exists( f'img/{self.tag_back_name}' ):
                tb_path = f'img/{self.tag_back_name}'
            elif os.path.exists( f'../img/{self.tag_back_name}' ):
                tb_path = f'../img/{self.tag_back_name}'
            else:
                raise Exception( "Could not load tag back's image")

        # Load the image
        tag_back = Image.open( tb_path )

        # Resize to the same size of the front tag
        tag_back = tag_back.resize( self.tag_size )

        # save to object
        self._tag_back = tag_back

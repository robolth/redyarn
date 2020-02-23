
import sys
import base64

import numpy as np
import skimage
from skimage import io, transform

import argparse

from PIL import Image
from PIL.ExifTags import TAGS


def scale_image(image=np.zeros((100,100)), 
                new_width=100,
                ascii_block_size=(2,3)):
    
    """Resizes image so that the final  ascii version will 
    have the same aspect ratio.
    http://www.cs.umd.edu/Outreach/hsContest98/questions/node4.html
    """
   
    original_width, original_height = image.shape
    aspect_ratio = original_height / float(original_width)
    w,h = ascii_block_size
    new_height = int(h/w * aspect_ratio * new_width)

    return skimage.transform.resize(image, (new_width, new_height))


def image2ascii(image=np.zeros((100,100)),new_width=100):
    
    def float2char(x=.1):
        ASCII_CHARS = [ 'W','X','@','0','#', '+', ';', ':', '"','.',' ']
        ASCII_CHARS = [ 'W','X','N','V', '=', '/', '>', '"','.',' ']
        num_chars = len(ASCII_CHARS)
        return ASCII_CHARS[ int(num_chars*x) ]
    
    #this is going to get called on an ndarray of float so vectorize
    float2char = np.vectorize(float2char)
    
    image = scale_image(image, new_width=new_width)
    
    #rescale so that we don't go past the end of ASCII_CHARS
    #float2char yields an ndarray of str 
    #we have to flatten to a single str
    rows = ["".join(row) for row in float2char(.999*image) ]
    return "\n".join(rows)

def get_ascii_conversion(file, new_width=100):
    # Source: https://github.com/macbuse/ascii-art/blob/master/ascii_with_numpy.ipynb

    image = np.zeros((200,200))
    
    try:
        image = skimage.io.imread(file, as_gray=True)
    except Exception as e:
        print("Unable to open image file.")
        print(e)
        return
   
    image_ascii = image2ascii(image, new_width=new_width)

    return image_ascii


def process_coords(coord):
   coord_deg = 0
   
   for count, values in enumerate(coord):
      coord_deg += (float(values[0]) / values[1]) / 60**count
   return coord_deg


def get_exif_data(file):

    img_file = Image.open(file)
    exif_data = img_file._getexif()

    width, height = img_file.size

    exif_output = {'width': width, 'height': height}

    if exif_data is not None:
        for name, value in exif_data.items():

            tag_name = TAGS.get(name, name)

            if tag_name is not 'MakerNote' and isinstance(tag_name, str):

                if isinstance(value, bytes):
                    value = value.decode('ascii')
                elif isinstance(value, str):
                    value = value

                exif_output[tag_name] = value

    return exif_output




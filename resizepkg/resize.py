#Using Pillow, the (currently - 10/06) maintained PIL library
#https://pillow.readthedocs.io/en/3.1.x/reference/Image.html 
from PIL import Image
import sys
import os 

#You can specify the mode e.g. 'L' will make it black and white
#mode and color can be exposed in later versions in main function 
def square_image (image_file, mode='RGB',  color = 'black'):
	image = Image.open(image_file)
	x,y = image.size
	if (x == y):
		print ('Image is already square - dimensions: ' + int_tup_to_str(image.size))	
		exit()
	size = max(x, y)
	squared = Image.new(mode , (size, size), color)
	#The tuple specifies the top left corner where the original image will be pasted 
	squared.paste(image, ((size - x)//2, (size-y)//2))
	squared.show()
	print ('Squared image created by padding the current image - new dimensions: ' + int_tup_to_str(squared.size))
	return save_image(image_file, squared)
	

def int_tup_to_str(tup):
	return '(' + ','.join(str(dim) for dim in tup) + ')'

def save_image (file_name, squared):
    image_file_name, ext = sep_extension (file_name)
    ext = 'PNG'
    squared_image_file_name = image_file_name + '_squared'
    print ('squared_image_file_name is ' + squared_image_file_name + ' and extension is ' + ext)
    squared.save(squared_image_file_name, ext)
    return squared_image_file_name

def sep_extension(file_name):
        file_name, ext = os.path.splitext(file_name)
        ext = ext.split('.')[1]
        return file_name, ext


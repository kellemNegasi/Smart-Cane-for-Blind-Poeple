import cv2
import numpy as np
import os
from PIL import Image
from resizeimage import resizeimage

path = 'E:/Haar Training Data/positive'
basewidth = 32
directory = os.fsencode(path)
current_directory = os.getcwd()
dest_directory ='E:/Haar Training Data/pos'
def edit_pos_images():
	if not os.path.exists(dest_directory):
			os.makedirs(dest_directory)
	for image in os.listdir(directory):
		file_name = os.fsdecode(image)
		current_image_path=path+'/'+str(file_name)
		dest_image_path = str(dest_directory)+'/'+file_name
		img = Image.open(current_image_path)
		wpercent = (basewidth/float(img.size[0]))
		hsize = int((float(img.size[1])*float(wpercent)))
		img = img.resize((basewidth,hsize), Image.ANTIALIAS)
		gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		gray.save(dest_image_path)
		# cv2.imwrite(dest_image_path,resized_img)
		print('writing the file'+current_image_path+'to'+dest_image_path)
	print('resizing completed succesfully')
edit_pos_images()

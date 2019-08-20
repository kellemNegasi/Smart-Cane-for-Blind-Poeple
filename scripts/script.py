import os
import numpy as np
import cv2


def create_pos_n_neg():
  current_directory = os.getcwd()
  pos =os.path.join(current_directory,r'pos')
  neg =dest_directory =os.path.join(current_directory,r'neg')
  for img in os.listdir(pos):
    file_name = os.fsdecode(img)
    current_image_path='pos'+'/'+str(file_name)
    Img =cv2.imread(current_image_path)
    h,w,c = Img.shape
    line = 'pos'+'/'+img+' 1 0 0 '+str(w)+' '+str(h)+'\n'
    with open('info.dat','a') as f:
      f.write(line)
  for img in os.listdir(neg):
    line = 'neg'+'/'+img+'\n'
    with open('bg.txt','a') as f:
      f.write(line)
create_pos_n_neg()

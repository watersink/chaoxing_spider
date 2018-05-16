#coding:utf-8
import cv2
import string
import random
import numpy as np

from keras.models import load_model


characters = string.ascii_uppercase+ string.ascii_lowercase
#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
width, height, n_len, n_class = 140, 50, 4, len(characters)


def decode(y):
    y = np.argmax(np.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])

def process(model,img_name):
    img=cv2.imread(img_name)
    img=img.astype(np.float32)/255
    img=cv2.resize(img,(width,height))
    img = img.reshape(1, height, width, 3)
    y_pred = model.predict(img)
    return decode(y_pred)
    
if __name__=="__main__":
    model=load_model("cnn.h5")
    img_name="./data/NTMY.jpg"
    y_pred=process(model,img_name)
    print("ori: ",img_name.split("/")[-1].split(".")[0],"pre: ",y_pred)

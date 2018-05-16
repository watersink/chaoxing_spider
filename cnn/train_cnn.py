# coding:utf-8
import numpy as np
import random
import string
import cv2
import matplotlib.pyplot as plt

from keras.models import *
from keras.layers import *

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

characters = string.ascii_uppercase + string.ascii_lowercase
# ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

width, height, n_len, n_class = 140, 50, 4, len(characters)


def init_model():
    input_tensor = Input((height, width, 3))
    x = input_tensor
    for i in range(3):
        x = Convolution2D(32 * 2 ** i, 3, 3, activation='relu')(x)
        x = Convolution2D(32 * 2 ** i, 3, 3, activation='relu')(x)
        x = MaxPooling2D((2, 2))(x)

    x = Convolution2D(32 * 2 ** 4, 2, 2, activation='relu')(x)


    x = Flatten()(x)
    x = Dropout(0.25)(x)
    x = [Dense(n_class, activation='softmax', name='c%d' % (i + 1))(x) for i in range(n_len)]
    model = Model(input=input_tensor, output=x)
    return model



def load_images(image_path="./data/"):

    images_label_list = []
    picnames = os.listdir(image_path)
    for i in range(0, len(picnames)):
            images_label_list.append([image_path + picnames[i], picnames[i][:-4]])

    return images_label_list,images_label_list

def generate_data(images_label_list,batch_size=8):
    pic_num_class = 4
    while True:
        X_image = []
        Y_label = []
        count = 0
        for image_label in images_label_list:

            img = cv2.imread(image_label[0])
            img = cv2.resize(img, (width,height))
            img = img.astype('float32') / 255.0
            X_image.append(img)


            Y_label.append(image_label[1])
            count += 1
            if count == batch_size:
                count = 0
                out_image = np.asarray(X_image).reshape(batch_size, height, width,3)

                out_label = [np.zeros((batch_size, n_class), dtype=np.uint8) for i in range(pic_num_class)]
                for i in range(len(Y_label)):
                    for j, ch in enumerate(Y_label[i]):
                        out_label[j][i,:] = 0
                        out_label[j][i,characters.find(ch)] = 1
                
                yield (out_image, out_label)
                X_image = []
                Y_label = []



def train_model():
    images_label_list_train, images_label_list_val = load_images()
    model = init_model()
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    print("begin training")
    history=model.fit_generator(generate_data(images_label_list_train), samples_per_epoch=8, nb_epoch=50,
                        validation_data=generate_data(images_label_list_val), nb_val_samples=8)
    model.save('cnn.h5')


    plt.plot(history.history['loss'],color="blue",label="train loss")
    plt.plot(history.history['val_loss'],color="red",label="val loss")
    plt.legend(loc='upper right')
    plt.xlabel("steps")
    plt.ylabel("loss")
    plt.show()




if __name__ == "__main__":
    train_model()
    
import numpy as np
import tensorflow as tf
from os import walk
import os
from os.path import join
from shutil import copyfile
from queue import Queue
import cv2

gpu_available = tf.test.is_gpu_available()
print("GPU Available: ", gpu_available)


def get_train_data():
    # TODO: change to handle entire batch
    data = convert_to_LAB()
    l_images = data[:, :, :, 0]
    ab_images = data[:, :, :, 1:]
    labels = get_labels(ab_images)
    return l_images, ab_images, labels


def get_labels(ab_img):
    """
    Calculate labels to be passed into loss function
    :param ab_img: ab channels of images, shape (num_images, 2)
    :return: labels to pass into loss function
    """
    pass

def walk_data2():
    """
    walk through data set directory
    :return: None, you should save all images to one directory
    """
    all_files = []
    data_dir = "SUN2012/Images/"
    for root, subfolder, files in walk(data_dir):
        for file in files:
            if file.endswith('.jpg'):
                all_files.append(join(root, file))
                copyfile(join(root, file), join("preprocessed/", file))

    print(all_files)
    return all_files

def walk_data():
    """
    walk through data set directory
    :return: list of absolute paths to images
    """
    imgs = list()
    q = Queue()
    initial_itms = os.listdir("./data/SUN2012/Images/")
    print(initial_itms)
    for itm in initial_itms:
        q.put(os.path.abspath(itm))

    while not q.empty():
        itm = q.get()
        # checking if item is a file anf ends in jpeg/ jpg
        if os.path.isfile(itm) and itm[len(itm)- 5:] == '.jpg':
            print("added to queue")
            imgs.append(itm)
        # checking if item is a directory
        if os.path.isdir(itm):
            itms = os.listdir(itm)
            # adding all the items in the directory to the queue
            for path in itms:
                # putting absolute value in queue 
                q.put(os.path.abspath(path))
    return imgs

def convert_to_LAB():
    """
    read images from the directory saved by walk_date, convert to LAB and store as npy
    :return: a numpy array
    """
    jpegs = walk_data2()
    lab = []
    for img in jpegs:
        im = cv2.imread(img)
        lab_im = cv2.cvtColor(im.astype('uint8'), cv2.COLOR_RGB2LAB)
        lab.append(lab_im)


    lab = np.asarray(lab)
    return lab

# print(convert_to_LAB().shape)

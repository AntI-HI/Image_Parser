import os
from pathlib import Path
from PIL import Image
import argparse
import csv


# In csv part user has to type two flags. One is csv path, other one is the image path.
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--csv", required=False, help="Enter the csv path located in using -csv flag..")
ap.add_argument("-i", "--img", required=False, help="Enter the image path located in using -img flag..")
args = vars(ap.parse_args())

''' Function Section '''

# Reads the csv file in default path and pulls the requisite parameters e.g. fileNames, objects, etc...
def read_csv(csvPath='data/train_labels.csv'):

    first_iter = True     # First iteration is redundant due to the Header stuff. So we should skip the first iteration

    with open(csvPath, 'r') as csvFile:     # Default csv location.

        reader = csv.reader(csvFile)

        for row in reader:

            if first_iter == False:

                fileNames.append(row[0])    # First row indicates the fileNames.
                objects.append(row[3])      # Third row indicates the object names.
                xmin.append(int(row[4]))    # Fourth row indicates the xmin.
                ymin.append(int(row[5]))    # Fifth row indicates the ymin.
                xmax.append(int(row[6]))    # Sixth row indicates the xmax.
                ymax.append(int(row[7]))    # Seventh row indicates the ymax.

            first_iter = False

    csvFile.close()

    return fileNames, objects, xmin, ymin, xmax, ymax


# Reads the given image file in given csv.
def read_particular_file_in_csv(csvPath,imageName):

    iteration_break = False

    with open(csvPath, 'r') as csvFile:     # Default csv location.

        reader = csv.reader(csvFile)

        for row in reader:

            if imageName.__eq__(row[0]):

                iteration_break = True
                fileNames.append(row[0])
                objects.append(row[3])
                xmin.append(int(row[4]))
                ymin.append(int(row[5]))
                xmax.append(int(row[6]))
                ymax.append(int(row[7]))

            elif iteration_break == True: break

    csvFile.close()

    return fileNames, objects, xmin, ymin, xmax, ymax


# This function traverse the specified path and create a list of images.
def read_images_from_path(path_of_img):

    entries = Path(path_of_img)
    imagelist = []

    for entry in entries.iterdir():

        entry = os.path.splitext(entry)

        if entry[1] == '.png' or entry[1] == 'jpg':  # Make sure it is an image file.

            entry = entry[0] + entry[1]
            imagelist.append(entry)

    return imagelist


# Crops the given image and saves as JPG.
def crop_given_image(path_of_image):

    for j in range(0, len(xmin)):

        img = Image.open(path_of_image)
        box = (xmin[j], ymin[j], xmax[j], ymax[j])
        crop = img.crop(box)
        dirName = objects[j]

        pat = path_of_image.split('\\')
        path_ = '\\'.join(pat[:-1])

        # Save as JPG
        if not os.path.exists(path_ + '\\' + dirName):
            os.mkdir(path_ + '\\' + dirName)
        crop.save(path_ + '\\' + dirName + '\\' + fileNames[j].split('.png')[0] + '_' + str(j + 1) + '.jpg', 'JPEG')


# Crops the images in given directory and saves as JPG.
def crop_images(path_images):

    i = 0
    prev_Name = str(fileNames[0])
    for j in range(0, len(fileNames)):

        if not prev_Name.__eq__(fileNames[j]):
            i = 0
            prev_Name = fileNames[j]

        img = Image.open(path_images + '/' + fileNames[j])
        box = (xmin[j], ymin[j], xmax[j], ymax[j])
        crop = img.crop(box)
        dirName = objects[j]

        # Save as JPG
        if not os.path.exists(path_images + '/' + dirName):
            os.mkdir(path_images + '/' + dirName)
        crop.save(path_images + '/' + dirName + '/' + fileNames[j].split('.png')[0] + '_' + str(i + 1) + '.jpg', 'JPEG')
        i += 1


''' Running Section '''


# Global Variables
fileNames = []
objects = []
xmin = []
ymin = []
xmax = []
ymax = []

if args['csv'] != None and args['img'] != None:  # User has to type both arguments otherwise default path will be on.

    path_csv = args['csv']
    path_img = args['img']
    path_ = path_csv

else: path_ = None

if path_ == None:   # If user doesn't give any argument than preidentified path will activated.

    fileNames, objects, xmin, ymin, xmax, ymax = read_csv()
    path_ = 'data/train'    # Default image path.
    imagelist = read_images_from_path(path_)
    crop_images(path_)

else:   # If user gives both argument.

    path_img = str(path_img)

    if len(path_img.split('.')) == 2:   # If user specify the particular image.

        if path_img.split('.')[1] == 'png' or path_img.split('.')[1] == 'jpg':

            length = len(path_img.split('.')[0].split('\\'))
            imageName = path_img.split('\\')[length - 1]
            fileNames, objects, xmin, ymin, xmax, ymax = read_particular_file_in_csv(path_csv,imageName)
            crop_given_image(path_img)

    else:   # If user doesn't specify any image file than it will traverse the given directory.

        fileNames, objects, xmin, ymin, xmax, ymax = read_csv(path_csv)
        imagelist = read_images_from_path(path_img)
        coords = xmin, ymin, xmax, ymax
        crop_images(path_img)

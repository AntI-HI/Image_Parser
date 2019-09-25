import os
from pathlib import Path
from PIL import Image
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=False, help="Enter the path located in using -p flag..")
args = vars(ap.parse_args())


''' Function Section '''


# Default path name located at project file.
def read_from_path(path_='data/train/'):      # This function reads the specified path and create two file name keeper list. One is xml keepers other one is image keepers.
    entries = Path(path_)
    xmllist = []
    imagelist = []

    for entry in entries.iterdir():

        entry = os.path.splitext(entry)
        if entry[1] == '.xml':
            entry = entry[0] + entry[1]
            xmllist.append(entry)
        elif entry[1] == '.png' or entry[1] == 'jpg':
            entry = entry[0] + entry[1]
            imagelist.append(entry)
    return xmllist, imagelist

def take_the_coordinates_from_xml(index):

    xmin = []  # keeps the start point x coordinates of particular xml
    ymin = []  # keeps the start point y coordinates of particular xml
    xmax = []  # keeps the ending point x coordinates of particular xml
    ymax = []  # keeps the ending point y coordinates of particular xml

    xmlwords = create_xmlwords_in_given_index(index)    # keeps the xml line by line

    for j in range(0, get_total_object_number_in_xml(xmlwords)):
        coords = get_x_and_y_coords(xmlwords, j)
        xmin.append(coords[0])
        ymin.append(coords[1])
        xmax.append(coords[2])
        ymax.append(coords[3])

    return xmin, ymin, xmax, ymax


# Seperates the xmllist line by line and appends to xmlwords list.
def create_xmlwords_in_given_index(index):
    xmlwords = []
    for line in open(xmllist[index]):
        listWords = line.split("\t")
        xmlwords.append(listWords)
    return xmlwords


# Seperates the given xmllist line by line and appends to xmlwords list.
def create_xmlwords_in_given_xml(fileName):
    xmlwords = []
    for line in open(fileName + '.xml'):
        listWords = line.split("\t")
        xmlwords.append(listWords)
    return xmlwords


# Crops the image with given coordinates and saves as JPG.
def crop_image_in_given_index(coords, index, imagelist):

    xmin, ymin, xmax, ymax = coords

    object_names = parse_Object_Names(create_xmlwords_in_given_index(index))
    img = Image.open(imagelist[index])

    for j in range(0, len(xmin)):
        box = (xmin[j], ymin[j], xmax[j], ymax[j])
        crop = img.crop(box)
        dirName = object_names[j]


        # Save as JPG
        if not os.path.exists(dirPath + '\\' + dirName):
            os.mkdir(dirPath + '\\' + dirName)

        if not imagelist[index].__contains__(dirPath):
            crop.save(dirPath + '\\' + dirName + '\\' + imagelist[index].split('\\')[2].split('.png')[0] + '_' + str(j + 1) + '.jpg', 'JPEG')
        else:
            leng = len(imagelist[index].split('\\'))
            crop.save('\\'.join(imagelist[index].split('.png')[0].split('\\')[:-1]) + '\\' + dirName + '\\' + imagelist[index].split('\\')[leng-1].split('.')[0] + '_' + str(j + 1) + '.jpg', 'JPEG')


# Crops the specified image with given argument and save as JPG.
def crop_image_in_given_path(path_, objects):

    img = Image.open(path_)
    num_of_index = len(path_.split('\\'))
    list_of_path_ = path_.split('\\')

    for j in range(0, len(xmin)):
        box = (xmin[j], ymin[j], xmax[j], ymax[j])
        crop = img.crop(box)
        dirName = objects[j]

        dirPath2 = dirPath
        dirPath2 = dirPath2.split('\\')

        localdir = []
        for i in range(0, len(dirPath2)-1):
            localdir.append(dirPath2[i] + '/')

        localdir = "".join(localdir)

        # Save as JPG
        if not os.path.exists(localdir + dirName):
            os.mkdir(localdir + dirName)

        crop.save(localdir + '/' + dirName + '/' + list_of_path_[num_of_index - 1].split('.png')[0] + '_' + str(j + 1).upper() + '.jpg', 'JPEG')


def get_total_object_number_in_xml(xmlwords):
    # The formula that can find the number of object depending on xml's number of line.
    return int((len(xmlwords) - 20) / 12) + 1


def get_x_and_y_coords(xmlwords,j):
    # The formula that can find the labeled object's x and y coordinates.
    return int(xmlwords[12 * j + 19][3].split('<xmin>')[1].split('</xmin>')[0]),\
           int(xmlwords[12 * j + 20][3].split('<ymin>')[1].split('</ymin>')[0]),\
           int(xmlwords[12 * j + 21][3].split('<xmax>')[1].split('</xmax>')[0]),\
           int(xmlwords[12 * j + 22][3].split('<ymax>')[1].split('</ymax>')[0])


# Parses the object names in xml words
def parse_Object_Names(xmlwords):
    objects = []
    for i in range(0, get_total_object_number_in_xml(xmlwords)):
        objects.append(xmlwords[12 * i + 14][2].split('<name>')[1].split('</name>')[0])

    return objects


''' Running Section '''


path_ = args['path']

if path_ != None:   # If user gives an argument

    dirPath = str(path_)

    if len(dirPath.split('.')) == 2:    # If given argument includes the image file
        dirlist = dirPath.split('.')
        if dirlist[1] == 'png' or dirlist[1] == 'jpg':

            xmin = []
            ymin = []
            xmax = []
            ymax = []

            xmlwords = create_xmlwords_in_given_xml(dirlist[0])

            for j in range(0, get_total_object_number_in_xml(xmlwords)):
                coords = get_x_and_y_coords(xmlwords, j)
                xmin.append(coords[0])
                ymin.append(coords[1])
                xmax.append(coords[2])
                ymax.append(coords[3])

            coords = xmin, ymin, xmax, ymax
            objects = parse_Object_Names(xmlwords)
            crop_image_in_given_path(path_, objects)

    else:    # if given argument only includes the path that keeps the images.
        xmllist, imagelist = read_from_path(path_)      # returns two file keeper lists.
        for index in range(0, len(xmllist)):
            coords = take_the_coordinates_from_xml(index)
            crop_image_in_given_index(coords, index, imagelist)

else:   # If user doesn't give any argument than Default path will be activated.
    xmllist, imagelist = read_from_path()
    dirPath = 'data/train/'     # Default path if there is no argument

    for index in range(0, len(xmllist)):
        coords = take_the_coordinates_from_xml(index)
        crop_image_in_given_index(coords, index, imagelist)
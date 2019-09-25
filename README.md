# Image Parser

Image Parser is a python code that takes a directory path as input argument and parse all the images in this file respect to their .xml file's object coordinates and seperate their object names to their own files. You can also specify any particular image file to be parsed with giving the image's full path in argument.

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install argparse
```
After that you have to import those packages
```python
import os
from pathlib import Path
from PIL import Image
import argparse
```

## Usage
### For Parse_with_xml:
You have three possible condition. You just don't give any arguments than default path will be activated or you give argument only the directory where the images contained which program will traverse all the image files or give the image's full path that has been specified along with its extension in order to parse it specifically.
```
python Parse_with_xml.py
```
In this option our program will only use the default path that is located at your project file named data\train.
```
python Parse_with_xml.py -p D:\DATASET\train
```
In this option our program will use the directory we give and traverse all the images to be parsed.
```
python Parse_with_xml.py -p D:\DATASET\train\image.png
```
In this option our program will parse the specified image file located at given directory. Note that you should also type the extension of image file.
### For Parse_with_csv:
You have also three possible condition. If You just don't give any arguments than default path will be activated or you give csv path and along with the directory where the images contained which program will traverse all the image files or you give csv path and along with image's full path that has been specified along with its extension in order to parse it specifically. Note that whenever you want to type arguments for this program, You have to type both of the arguments. Otherwise default path will be activated.
```
python Parse_with_csv
```
In this option our program will only use the default paths. csv path is data/train_labels.csv. img path is data\train.
```
python Parse_with_csv -c D:\DATASET\train_labels.csv -i D:\DATASET\train
```
In this option our program will use two different paths. First flag specifies where your csv file is. Other flag specifies where the image files hold so program will parse all the images in this directory.
```
python Parse_with_csv -c D:\DATASET\train_labels.csv -i D:\DATASET\train\image.png
```
In this option our program will use two different paths. First flag specifies where your csv file is. Other flag specifies where the image file hold so program will parse only this image. Note that you should also type the extension of image file.

## Running the Test
You're gonna see the parsed images in image directory with all the parsed objects has its own directories.
![Screenshot__131_](/uploads/6bdc03c2a44c294f571c0c909815a906/Screenshot__131_.png)
![Screenshot__132_](/uploads/4de70d83da846cc00586edae573f2bd0/Screenshot__132_.png)
![Screenshot__133_](/uploads/2208e1bbbbf98e0557280c2fe782df52/Screenshot__133_.png)

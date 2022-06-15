from distutils.file_util import write_file
from PIL import Image as im
import numpy as np

FileName = str(input("Enter image name : "))
# Since the reccomended format for Steganography is .bmp
FileFormat = "bmp"

# Try to check if file exist and .bmp format
try:
    BaseImage = im.open(f"BaseImage\{FileName}.{FileFormat}")
except FileNotFoundError:
    # Try to check if file exist on ConvertedImage Folder
    try:
        BaseImage = im.open(f"ConvertedImage\{FileName}.{FileFormat}")
    except FileNotFoundError:
        # Catch exception if file exist on BaseImage folder but not .bmp format
        try:
            DesiredFormat = str(input("Enter the Image format :"))
            BaseImage = im.open(f"BaseImage\{FileName}.{DesiredFormat}")
            BaseImage.save(f"ConvertedImage\{FileName}.{FileFormat}")
        # If file not exist, raise exception
        except FileNotFoundError:
            raise Exception("File not exist")

SecretMessage = str(input("Enter the secret message : "))

# Empty Array to storing Binary form of the Message
ArrayMessage = []

# Secret Message
for i in SecretMessage:
    # Change every Message char to Ascii form, then change it to Binary form
    AsciiMsg = ord(i)
    BitMsg = bin(AsciiMsg).replace("b", "")

    ArrayMessage.append(BitMsg)

print(ArrayMessage)

CoverImage = BaseImage.load()

ImageSize = BaseImage.size

# Array for storing the value of RGB, in every pixel in the picture
StegoImage = []

for x in range(ImageSize[0]):
    for y in range(ImageSize[1]):
        StegoImage.append(CoverImage[x, y])

f = open("StegoImage.txt", "w")
f.write(str(StegoImage))
f.close

while True:
    UserKey = int(
        input(
            "1. Red\n2. Green\n3. Blue\nEnter your choice where to put the message : "
        )
    )
    if UserKey > 3 or UserKey < 1:
        print("Number incorrect, please choose number according to the color")
    else:
        break

# Array for storing converted bit
NewStego = []

for indexArray in range(len(ArrayMessage)):
    for sizeArray in range(len(ArrayMessage[indexArray])):
        StegoBit = bin(StegoImage[sizeArray][UserKey - 1]).replace("b", "")

        # Reverse the Array
        StegoBin = StegoBit[::-1]

        # Adding the binary number till reaching 8-bit
        while len(StegoBin) < 8:
            StegoBin += "0"

        StegoBit = StegoBin[::-1]

        # Change array to List to edit the content
        ListBit = list(StegoBit)

        # Change str to int
        for n in range(len(ListBit)):
            ListBit[n] = int(ListBit[n])

        ListBit[7] = int(ArrayMessage[indexArray][sizeArray])

        NewStego.append(ListBit)

# Convert Bin to Decimal
BitContainer = []
for indexBin in range(len(NewStego)):
    BinContainer = ""

    for sizeBin in range(len(NewStego)):
        BinContainer = str(NewStego[indexBin][sizeBin])
    BinContainer = int(BinContainer, 2)
    BitContainer.append(BinContainer)

for m in range(len(BitContainer)):
    ListStegoImage = list(StegoImage[m])
    if UserKey == 1:
        ListStegoImage = (BitContainer[m], StegoImage[0][1], StegoImage[0][2])
    if UserKey == 2:
        ListStegoImage = (StegoImage[0][0], BitContainer[m], StegoImage[0][2])
    if UserKey == 3:
        ListStegoImage = (StegoImage[0][0], StegoImage[0][1], BitContainer[m])
    StegoImage[m] = tuple(ListStegoImage)

print(type(StegoImage))

f = open("StegoedImage.txt", "w")
f.write(str(StegoImage))
f.close

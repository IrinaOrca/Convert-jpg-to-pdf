import os
from PIL import Image


def del_filesJpg(myFolder):
    for CurrentyFile in os.listdir(myFolder):
        PathCurrentyFile = os.path.join(myFolder, CurrentyFile)
        if PathCurrentyFile.find(".jpg") != -1 or PathCurrentyFile.find(".JPG") != -1:
            os.remove(PathCurrentyFile)    


def find_files(myFolder):

    if myFolder == "":
        return []

    myListFilesIpg = []
    for CurrentyFile in os.listdir(myFolder):
        PathCurrentyFile = os.path.join(myFolder, CurrentyFile)
        if PathCurrentyFile.find(".jpg") != -1 or PathCurrentyFile.find(".JPG") != -1:
            myListFilesIpg.append(PathCurrentyFile)
    return myListFilesIpg


def save_filePdf(myFolder, MyFilePdf, myListFilesIpg):

    if myFolder == "":
        return

    ListMyImages = []

    myImageFist = 0
    for i in range(len(myListFilesIpg)):
        if myImageFist == 0:
            myImageFist = Image.open(myListFilesIpg[i])
            myImageFistConverted = myImageFist.convert('RGB')
        else:
            myImage = Image.open(myListFilesIpg[i])
            myImageConverted = myImage.convert('RGB')
            ListMyImages.append(myImageConverted)

    if myImageFist != 0: 
        PathNewFile = myFolder + "/" + MyFilePdf + ".pdf"
        myImageFistConverted.save(PathNewFile, save_all=True, append_images=ListMyImages)
        return PathNewFile

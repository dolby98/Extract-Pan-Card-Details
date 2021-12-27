import cv2
import pytesseract
import os
from PIL import Image
import re
import pandas as pd


def findword(textlist, wordstring): #Returns list just after it finds the PAN CARD NUMBER title.Number would be in the returned list
    lineno = -1
    for wordline in textlist:
        xx = wordline.split( )
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno+1:]
            return textlist
    return textlist

def pan_read_data(text): #Running everytime for every person detail from list
    name = None
    pan = None
    nameline = []
    panline = []
    allPanInfo = [] #Stores all pan card info of a single person in list as elements after line breaks
    lines = text.split('\n') #Splitting data on change of line
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        allPanInfo.append(s)
    isPan = False #Flag to maintain a check if it's a pan card or not

    allPanInfo = list(filter(None, allPanInfo)) #Removing any blank space words

    #For loop is to Find line index for title
    for wordline in allPanInfo:
        xx = wordline.split('\n')
        #Matching the words in line using ReGex to find words similar to INCOME TAX DEPARTMENT
        if ([w for w in xx if re.search('(INCOMETAXDEPARWENT|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
            lineno = allPanInfo.index(wordline) #Storing line No when regex match found
            isPan = True #Setting flag as true for identifying as Pan Card
            break

    allPanInfo = allPanInfo[lineno+1:] #Next search for name and pancard in list will be ahead of this line no since this was the heading for pan card and read first(top to bottom).

    if(isPan): #Executes only if the image is a pan card
        #Person PAN number
        allPanInfo = findword(allPanInfo, '(Pormanam|Number|umber|Account|ccount|count|Permanent|ermanent|manent|wumm)$') #Calls function findword with regex expression for pan card number title
        panline = allPanInfo[0]
        pan = panline.rstrip()
        pan = pan.lstrip()
        pan = pan.replace(" ", "")
        pan = pan.replace("\"", "")
        pan = pan.replace(";", "")
        pan = pan.replace("%", "L")
        panlist = panline.split()
        pannumber = "Length Invalid"
        for pan in panlist:
            if pan.isalnum() and len(pan)==10:
                pannumber = pan #Pan Card Id saved
                break
        
        NumberList.append(pannumber) #Appending pancard number to NumberList 
        
        #Person Name
        allPanInfo = findword(allPanInfo, '(ama|Name|ame|name|Nam|Nama)$') #Calls function findword with regex expression for Name

        name = allPanInfo[0]
        name = name.rstrip()
        name = name.lstrip()
        pan = pan.replace("|", "")
        name = name.replace("8", "B")
        name = name.replace("0", "D")
        name = name.replace("6", "G")
        name = name.replace("1", "I")

        name = re.sub('[^a-zA-Z] +', ' ', name) 
        name = name.split()

        fullName = ' '.join(name[:2]) #Join First Name and Surname

        NameList.append(fullName) #Appending pancard number to NameList
    
def writeCsv(name,number):
    dict = {'Full Name': name, 'Pan Card ID': number} #Create a dictionary with name and number
    df = pd.DataFrame(dict) #Convert to dataframe
    print(df) #Printing dataframe
    df.to_csv(r'D:\Projects\ExtractPanDetails\PanDetails.csv') #Convert to csv and save 


#Main start of file
path_to_tesseract = r"D:\apps\teseract\tesseract.exe" 
path = "D:\\Projects\\ExtractPanDetails\\PanImages" #Specifying directory for images
pytesseract.pytesseract.tesseract_cmd=path_to_tesseract

allPanDetails = [] #Creating a list to store all details extracted from all pan card images

for imageName in os.listdir(path):
    inputPath = os.path.join(path,imageName)
    img = Image.open(inputPath)
    text = pytesseract.image_to_string(img,lang='eng')
    allPanDetails.append([text])    #Appending details for each person card

NameList = [] #List to store names extracted from pan card
NumberList = [] ##List to store pan car number extracted from pan card

for person in allPanDetails:
    pan_read_data(person[0])
    
writeCsv(NameList,NumberList) #Save details as records in dataframe and then into a csv file



# Extract-Pan-Card-Details

The PanImages folder has a bunch of pan card images on which we will run our .py file and extract data.
Aim is to extract all details for all images and associate pan card number to corresponding name.

The panimg.py file is run and following are steps it follows:
  1.Picks up all images and extracts data(OCR) using tesseract and saves the data into a list
  2.For each persons data we run the function pan_read_data. It preprocess the text, extracts name and id and stores into respective lists.
  3.Then we call a function writeCsv which creates a dataframe with the data of Name and Pan card number. And finally this is saved into a csv format. A generated csv is uploaded     as well for reference.

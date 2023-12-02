# Business Card OCR Application

## Problem Statement

The task is to develop a Streamlit application that facilitates the extraction of relevant information from business cards using easyOCR. The extracted information includes the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code. Additionally, the application should allow users to save this information, along with the uploaded business card image, into a database. The database should support multiple entries, each with its own business card image and extracted information.

## 1. Install Required Packages

Make sure to have the following packages installed:

```bash
# Install Python
install python
```

# Required Python Packages
```
pip install pandas
pip install streamlit
pip install sqlalchemy
pip install PyMySQL
pip install numpy
pip install streamlit-option-menu
pip install Pillow
```

# Install PyTorch and easyocr
```
install pytorch https://pytorch.org/
pip install easyocr
```

## 2. Design User Interface
Create a user-friendly interface using Streamlit, incorporating widgets like file uploader, buttons, and text boxes to guide users through the process.

## 3. Implement Image Processing and OCR
Utilize easyOCR for extracting relevant information from the business card image.

## 4. Display Extracted Information
Present the extracted information in an organized manner within the Streamlit GUI, using widgets like tables, text boxes, and labels.

##  5. Implement Database Integration
Integrate a database management system (SQLite or MySQL) to store extracted information and associated business card images. Utilize SQL queries for creating tables, inserting, updating, and retrieving data.


## Run the application using the following command
```
streamlit run ./home.py
```
This will launch the Streamlit application, allowing you to upload business card images, extract information, and store it in the integrated database


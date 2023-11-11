import streamlit as st 
import mysql.connector
from sqlalchemy import create_engine,text,MetaData,Table,update
from PIL import Image
from streamlit_option_menu import option_menu
import easyocr
import re
import pymysql
import numpy as np
from numpy import asarray
import pandas as pd


st.set_page_config(page_title="Bizcard",layout="wide")
st.title("Bizcard Data extraction")
#st.markdown("<style>div.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True)
 

# establish the connection to sql server 
@st.cache_data
def create_Database():
    mydb = mysql.connector.connect(host="localhost", user="root",password="")
    mycursor = mydb.cursor(buffered=True) 
    print("connection is established")
    try :
        mycursor.execute("CREATE DATABASE bizcard")
        print("Database is created successfully")
        #setting the engine
    except :
        pass
          

def create_table():
    cnx = create_engine('mysql+pymysql://root:@localhost/bizcard')
    with cnx.connect() as mycursor:
        try:
            table_query=text("CREATE TABLE IF NOT EXISTS user_details (Name VARCHAR(255), Position VARCHAR(255), Contact VARCHAR(255), Card_name VARCHAR(255), Mail VARCHAR(255), Website VARCHAR(255), Address VARCHAR(255), Pincode VARCHAR(255))")
            mycursor.execute(table_query)
        except Exception as e:
            print(f"Error in data loading: {e}")



def load_data(table):
    cnx = create_engine('mysql+pymysql://root:@localhost/bizcard')
    try:
        table.to_sql('user_details', con=cnx, if_exists='append', index=False)
        st.success("Data has been stored!!!")
    except Exception as e:
           print(f"Error in data loading: {e}")
        
            



def retrive_data(): 
    cnx = create_engine('mysql+pymysql://root:@localhost/bizcard')
    with cnx.connect() as mycursor:
        try :
            pd_query = pd.read_sql('SELECT * FROM user_details', mycursor)
            return pd_query
        except  Exception as e:
            st.write(f"Error: {e}")
            
    
    
@st.cache_data
def get_data_image(result):
    Pincode = ''
    contact_num = []
    mail_id = ''
    website = ''
    Address = ""
    
    a1 = []
    
    
    #1 name ,position
    name = result[0][1].upper()
    position = result[1][1]
    a1.append(name)
    a1.append(position)

    
    #2 pincode
    for i in result:
        x = i[1]
        pin= re.findall("\d",x)
        if len([*pin]) == 6:
            Pincode ="".join(pin)
     
    # contact nu,ber 
    for i in result:
        x =i[1]
        phone = re.findall("\d",x)
        if len(*[phone])==10:
            contact_num .append("".join(phone))
        elif "+" in x:
            contact_num.append(x)
    #3     
    for i in result:
        x =i[1]
        if "@" in x:
                mail_id =x
    
            
    #6   
    pattern1 = r"\bwww\w*\b"  
    pattern2 = r"\.com\b"  
    a = []
    for i in result:
        x =i[1]
        website1 = re.findall(f'{pattern1}',x,flags=re.IGNORECASE)
        website2 = re.findall(f'{pattern2}',x)
        if "@" not in x and (website1 or website2):
            a1.append(x)
            a.append(x)
    website = ".".join(a).replace(" ",".")
    
    
    #7
    b = []
    for i in result:
        x = i[1]
        address = re.findall(r"\W",x)
        if (" " in address) and len(address)!= 0:
            cm1 = re.findall("\S[a-zA-Z]+",x)
            a1.append(" ".join(cm1))
           
            v = re.findall(r"\w",x)
            v1 = "".join(v)
            c = re.findall(r"\d",x)
             
            
            if len(c) != 0:
                b.append(x)
                
    Address = ",".join(b).replace(";",",").replace(" ","")
    
    
    c_name = []
    for i in result :
        x=i[1]
        company_name = re.findall("[a-zA-Z]+",x,flags=re.IGNORECASE)
        name_c = " ".join(company_name)
        if name_c not in a1:
            q = ".".join(company_name)
            if "com" not in name_c:
                if name_c not in a1:
                    c_name.append(name_c)
                    
    company_name = " ".join(c_name)
    



    return name,position,mail_id,contact_num,website,Address, Pincode,company_name
            
@st.cache_data
def read_image(img):
    reader = easyocr.Reader(["en"],gpu=False)
    result = reader.readtext(img)
    out = get_data_image(result)
    return out
    
 
   
def upload_image(imagefile):
    
    
    if imagefile is not None:
        
        image = Image.open(imagefile)
        numpydata = asarray( image)
        out = read_image(numpydata)
        name = [out[0]]
        Position = [out[1]]
        mail = [out[2]]
        contact = [",".join(out[3])]
        website = [out[4]]
        Address = [out[5]]
        Pincode = [out[6]]
        card_name = [out[7]]
            
        card_table = pd.DataFrame({"Name":name,"Position":Position,"Contact":contact,"Card_name":card_name,"Mail":mail,"Website":website,"Address":Address,"Pincode":Pincode}) 
        return card_table   
    else:
        st.write("upload the correct image")
   
   
def show_data(values):
    series_valu = values.iloc[0,:]
    name =  series_valu.iloc[0]
    st.write("Name : ", series_valu.iloc[0])
    st.write("Position : ", series_valu.iloc[1])
    st.write("Contact : ", series_valu.iloc[2])
    st.write("Card_name : ", series_valu.iloc[3])
    st.write("Mail : ", series_valu.iloc[4])
    st.write("Website : ", series_valu.iloc[5])
    st.write("Address : ", series_valu.iloc[6])
    st.write("Pincode : ", series_valu.iloc[7])
    return name  



def delete_info(names):
    cnx = create_engine('mysql+pymysql://root:@localhost/bizcard')
    with cnx.connect() as mycursor:
        if st.button("Delete"):
            sql_query =  "DELETE FROM user_details WHERE NAME=:name"
            val={"name":names}
            mycursor.execute(text(sql_query),val)
            mycursor.commit()
            st.success("Record Deleted")
            return "a"
    


def update_info(name,values):
    cnx = create_engine('mysql+pymysql://root:@localhost/bizcard')
    with cnx.connect() as mycursor:
        #name = st.text_input("Enter the name ")
        option = st.selectbox("Select Field to edit",["None","Position","Contact","Card_name","Mail","Website","Address"])
        if option =="Position":
            Position = st.text_input("Enter the Position ") 
            if len(Position)!=0:
                if st.button("Update"):
                    sql_query = "UPDATE user_details SET Position=:position where  Name =:name"
                    val = {"position":Position,"name":name}
                    mycursor.execute(text(sql_query),val)
                    mycursor.commit()
                    return "a"
                                   
                    
            else:
                st.write("Enter the Value")
                
        elif option =="Contact":
            Contact = st.text_input("Enter the Contact ") 
            if len(Contact)!=0:
                if st.button("Update"):
                    sql_query = "UPDATE user_details SET Contact=:Contact where  Name =:name"
                    val = {"Contact":Contact,"name":name}
                    mycursor.execute(text(sql_query),val)
                    mycursor.commit()
                    return "a"
            else:
                st.write("Enter the Value")
                
                
        if option =="Card_name":
            Card_name  = st.text_input("Enter the Card_name ")
            if len(Card_name)!=0:
                if st.button("Update"):
                    sql_query = "UPDATE user_details SET Card_name=:Card_name where  Name =:name"
                    val = {"Card_name":Card_name,"name":name}
                    mycursor.execute(text(sql_query),val)
                    mycursor.commit()
                    return "a"
            else:
                st.write("Enter the Value")
               
                
        elif option =="Mail":
            Mail  = st.text_input("Enter the Mail ID ") 
            if len(Mail)!=0:
                if st.button("Update"):
                    sql_query = "UPDATE user_details SET Mail=:Mail where  Name =:name"
                    val = {"Mail":Mail,"name":name}
                    mycursor.execute(text(sql_query),val)
                    mycursor.commit()
                    return "a"
            else:
                st.write("Enter the Value")
                
        elif option =="Website":
            Website = st.text_input("Enter the Website ") 
            if len(Website)!=0: 
                if st.button("Update"):
                    sql_query = "UPDATE user_details SET Website=:Website where  Name =:name"
                    val = {"Website":Website,"name":name}
                    mycursor.execute(text(sql_query),val)
                    mycursor.commit()
                    return "a"
            else:
                st.write("Enter the Value")       
                
        elif option =="Address":
            Address = st.text_input("Enter the Address ") 
            if len(Address)!=0: 
                if st.button("Update"):
                    sql_query = "UPDATE user_details SET Address=:Address where  Name =:name"
                    val = {"Address":Address,"name":name}
                    mycursor.execute(text(sql_query),val)
                    mycursor.commit()  
                    return "a" 
            else:
                st.write("Enter the Value")              
    
        
    
   
def set_sidebar():
    Selected = option_menu(
        menu_title=None,
        options=["Upload","Edit","Delete"],
        orientation="horizontal")
    
    if Selected == "Upload":
        st.subheader("Upload the image")
        st.write("Retrived Data")
        imagefile = st.file_uploader("Choose a Image file [JPG or PNG]")
        if imagefile is not None:
            card_table = upload_image(imagefile)  
            c1,c2 =st.columns(2)
            with c1:
                image = Image.open(imagefile)
                newsize = (700,500)
                im1 = image.resize(newsize)
                st.image(im1, caption='Image')
            with c2:
                v = st.data_editor(card_table)
                st.write("click the button to store the data")
                if st.button ("Submit"):
                    data_frame = pd.DataFrame(v)
                    load_data(data_frame)
                    #st.success("The data is stored.....")
            
        else:
            cl2,cl2,cl3 = st.columns(3)
            with cl2:
                st.write("upload the  image !!!!")
    
    elif Selected == "Edit":
        st.subheader(" view and Edit the Data")
        data =  retrive_data()
        #st.data_editor(data)
        cl1,cl2,cl3 = st.columns(3)
        with cl1:
            try :
                option = st.selectbox("Select the Name",data["Name"].unique(),index=None)
                if option is not None :
                    values = data.loc[(data['Name'] ==option)]
                    st.subheader("Before Update")
                    name = show_data(values)        
           # st.write(values)
                    with cl2 :
                        a = update_info(name,values)
                    with cl3:
                        try :
                            if len(a) != 0:
                                data =  retrive_data()
                                values = data.loc[(data['Name'] ==option)]
                                st.subheader("Updated Value")
                                show_data(values)
                        except :
                            st.write("")
            except:
                st.write("The Table has no values ")
                         
    elif Selected == "Delete":
        st.subheader(" Delete  Data")
        data =  retrive_data()
        #st.data_editor(data)
        cl1,cl2,cl3 = st.columns(3)
        with cl1:
            option = st.selectbox("Select the Name",data["Name"].unique(),index=None)
            values = data.loc[(data['Name'] ==option)]
            st.subheader(" Records Info")
            st.table(data["Name"])
        with cl2:    
            if option is not None:
                st.subheader("Selected Record info")
                name = show_data(values)
                b = delete_info(name)
        with cl3:
            try :
                if len(b) != 0:
                    data =  retrive_data()
                    values = data.loc[(data['Name'] ==option)]
                    st.subheader("Records After Deleted")
                    st.table(data["Name"])
                else:
                    st.write("Select the Record to Delete")
            except :
                st.write("")
            
set_sidebar()

    

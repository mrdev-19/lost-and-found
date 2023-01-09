import streamlit as st
from streamlit_option_menu import option_menu
import database as db
#---------------------------------------------------
# page config settings:

page_title="Lost and Found Portal"
page_icon=":mag:"
layout="centered"

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(page_title+" "+page_icon)

#--------------------------------------------------
#hide the header and footer     

hide_ele="""
        <style>
        #Mainmenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
        """
st.markdown(hide_ele,unsafe_allow_html=True)
#---------------------------------------------------
curlogin=""
def log_sign():
    selected=option_menu(
        menu_title=None,
        options=["Login","Signup","Admin"],
        icons=["bi bi-link-45deg","bi bi-arrow-bar-up ","bi-person-badge-fill"],
        orientation="horizontal"
    )
    global submit
    if(selected=="Login"):
        with st.form("Login",clear_on_submit=True):
            st.header("Login")
            username=st.text_input("Username")
            password=st.text_input("Password",type="password")
            submit=st.form_submit_button()
            if(submit):
                if(username=="" or password==""):
                    st.warning("Enter your login credentials")
                else:
                    if(db.authenticate(username,password)):
                        st.session_state["curlogin"]=username
                        st.session_state["key"]="main"
                        st.experimental_rerun()
                    else:
                        st.error("Please check your username / password ")
            
    elif(selected=="Signup"):
         with st.form("Sign Up",clear_on_submit=True):
            st.header("Sign Up")
            email=st.text_input("Enter your email")
            number=st.text_input("Enter your Mobile Number")
            username=st.text_input("Enter your username")
            password=st.text_input("Enter your password",type="password")
            submit=st.form_submit_button()
            if(submit):
                dev=db.fetch_all_users()
                usernames=[]
                emails=[]
                numbers=[]
                for user in dev:
                    usernames.append(user["key"])
                    emails.append(user["email"])
                    numbers.append(user["number"])
                if(username in usernames):
                    st.error("Username already exists!\nTry another username !")
                elif(email in emails):
                    st.error("email already exists!\nTry with another email !")
                elif(number in numbers):
                    st.error("Phone number already exists\nTry with another number")
                elif(len(password)<=6):
                    st.error("Password cannot be less than 6 characters")
                else:
                    db.insert_user(username,password,email,number)
                    st.success("Signed Up Successfully")

    elif selected=="Admin":
        with st.form("Admin Login",clear_on_submit=True):
            st.header("Admin Login")
            username=st.text_input("Username")
            password=st.text_input("Password",type="password")
            submit=st.form_submit_button()
            if(submit):
                if(username=="" or password==""):
                    st.warning("Enter your login credentials")
                else:
                    if(db.ad_authenticate(username,password)):
                        st.session_state["curlogin"]=username
                        st.session_state["key"]="adminmain"
                        st.experimental_rerun()
                    else:
                        st.error("Please check your username / password ")
def main():
    selected=option_menu(
            menu_title=None,
            options=["Lost","Found"],
            icons=["bi bi-search","bi bi-box"],
            orientation="horizontal"
        )
    if(selected=="Lost"):
        
        with st.form("Lost entry form_@dev_mr",clear_on_submit=True):
            st.header("Lost Item Form")
            date=st.date_input("Enter the date on which the object is Lost")
            name=st.text_input("Enter the name of the object Lost",placeholder="Phone etc.")
            place=st.text_input("Where was it lost ?",placeholder="Atrium / XLab etc.")
            mailid=st.text_input("Email !",placeholder="yourname@org.com")
            other=st.text_input("Any other relevant details? ",placeholder="Colour / Size / Specifications etc.")
            submitted=st.form_submit_button("Submit data")
            lof="lost"
            if(submitted):
                if(name=="" or place==""):
                    st.error("Enter All Required Fields")
                else:
                    db.insert_entry(st.session_state["curlogin"],str(date),name,place,mailid,other,lof)
                    st.success("Form Submitted Successfully")

    elif(selected=="Found"):
        with st.form("found_entry_form@devmr",clear_on_submit=True):
            st.header("Found Item Form")
            date=st.date_input("Enter the date on which the object is found")
            name=st.text_input("Enter the name of the object found",placeholder="Phone etc.")
            place=st.text_input("Where is it found ?",placeholder="Atrium / XLab etc.")
            mailid=st.text_input("Email !",placeholder="yourname@org.com")
            other=st.text_input("Any other relevant details? ",placeholder="Colour / Size / Specifications etc.")
            lof="found"
            submitted=st.form_submit_button("Submit data")
            if(submitted):
                #write the data inputted to database:
                db.insert_entry(st.session_state["curlogin"],str(date),name,place,mailid,other,lof)
                st.success("Form Submitted Successfully")

def admin():
    selected=option_menu(
            menu_title=None,
            options=["Lost","Found"],
            icons=["bi bi-search","bi bi-box"],
            orientation="horizontal"
        )
    if(selected=="Lost"):
        st.warning("Submit a form only after making sure the item is not in the dropdown list")
        items=["Select an Item"]
        lost=db.all_found()
        for user in lost:
            if(user["status"]==""):
                items.append(user["name"])
        option=st.selectbox(
            "Found Items List : ",
            tuple(items),
            0
        )
        dev={}
        for user in lost:
            if(user["name"]==option):
                with st.form("ClaimLostObject@mrdev19",clear_on_submit=True):
                    st.subheader("Found Items List")
                    st.write("Item : "+user["name"])
                    st.write("Place Where it is Lost : "+user["place"])
                    st.write("Other Details : "+user["other"])
                    
                    rollnumb=st.text_input("Enter the roll of the student to whom it was returned")
                    check=st.checkbox("The item is returned to the owner")        
                    sub=st.form_submit_button("Returned Successfully")
                    if(sub and check and rollnumb):
                        return db.f_change_status(user["key"],rollnumb)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        with st.form("Lost entry form_@dev_mr",clear_on_submit=True):
            st.header("Lost Item Form")
            date=st.date_input("Enter the date on which the object is Lost")
            name=st.text_input("Enter the name of the object Lost",placeholder="Phone etc.")
            place=st.text_input("Where was it lost ?",placeholder="Atrium / XLab etc.")
            mailid=st.text_input("Email !",placeholder="yourname@org.com")
            other=st.text_input("Any other relevant details? ",placeholder="Colour / Size / Specifications etc.")
            submitted=st.form_submit_button("Submit data")
            lof="lost"
            if(submitted):
                if(name=="" or place==""):
                    st.error("Enter All Required Fields")
                else:
                    db.insert_entry(st.session_state["curlogin"],str(date),name,place,mailid,other,lof)
                    st.success("Form Submitted Successfully")

    elif(selected=="Found"):
        st.warning("Submit a form only after making sure the item is not in the dropdown list")
        items=["Select an Item"]
        found=db.all_lost()
        for user in found:
            if(user["status"]==""):
                items.append(user["name"])
        option=st.selectbox(
            "Lost items list",
            tuple(items),
            0
        )
        dev={}
        for user in found:
            if(user["name"]==option):
                with st.form("ReturnFoundObject@dev",clear_on_submit=True):
                    st.subheader("Return Found Item")
                    st.write("Item : "+user["name"])
                    st.write("Place Where it is found : "+user["place"])
                    st.write("Other Details : "+user["other"])
                    st.write("The Item belongs to "+user["username"])
                    st.markdown('<a href="mailto:'+user["email"]+'">Contact</a>', unsafe_allow_html=True)
                    # st.write("You can contact him\her at "+user["number"])
                    rollnum=st.text_input("Enter the roll number of the student whom it was returned by ",placeholder="")
                    sub=st.form_submit_button("Return The Item to the Owner")
                    if(sub and rollnum):
                        return db.l_change_status(user["key"],rollnum)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        with st.form("found_entry_form@devmr",clear_on_submit=True):
            st.header("Found Item Form")
            date=st.date_input("Enter the date on which the object is found")
            name=st.text_input("Enter the name of the object found",placeholder="Phone etc.")
            place=st.text_input("Where is it found ?",placeholder="Atrium / XLab etc.")
            mailid=st.text_input("Email !",placeholder="yourname@org.com")
            other=st.text_input("Any other relevant details? ",placeholder="Colour / Size / Specifications etc.")
            lof="found"
            submitted=st.form_submit_button("Submit data")
            if(submitted):
                #write the data inputted to database:
                db.insert_entry(st.session_state["curlogin"],str(date),name,place,mailid,other,lof)
                st.success("Form Submitted Successfully")
    

if "key" not in st.session_state:
    st.session_state["key"] = "log_sign"

if st.session_state["key"] == "log_sign":
    log_sign()

elif st.session_state["key"] == "adminmain":
    admin()

elif st.session_state["key"] == "main":
    main()

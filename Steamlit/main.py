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
        options=["Login","signup"],
        icons=["bi bi-link-45deg","bi bi-arrow-bar-up "],
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
            
    elif(selected=="signup"):
        with st.form("Sign Up",clear_on_submit=True):
            st.header("Sign Up")
            email=st.text_input("Enter your email")
            username=st.text_input("Enter your username")
            password=st.text_input("Enter your password",type="password")
            submit=st.form_submit_button()
            if(submit):
                dev=db.fetch_all_users()
                usernames=[]
                emails=[]
                for user in dev:
                    usernames.append(user["key"])
                    emails.append(user["email"])
                if(username in usernames):
                    st.error("Username already exists!\nTry another username !")
                elif(email in emails):
                    st.error("email already exists!\nTry with another email !")
                elif(len(password)<=6):
                    st.error("Password cannot be less than 6 characters")
                else:
                    db.insert_user(username,password,email)
                    st.success("Signed Up Successfully")

def main():
    selected=option_menu(
            menu_title=None,
            options=["Lost","Found","Lost Items","Found Items"],
            icons=["bi bi-search","bi bi-box","bi bi-bullseye","bi bi-award"],
            orientation="horizontal"
        )
    if(selected=="Lost"):
        st.warning("Before Submitting a form make sure to check for your item in the 'Lost Items' coulmn")
        with st.form("Lost entry form",clear_on_submit=True):
            st.header("Lost Portal")
            date=st.date_input("Enter the date on which the object is Lost")
            name=st.text_input("Enter the name of the object Lost",placeholder="...")
            place=st.text_input("Where was it lost ?",placeholder="...")
            number=st.text_input("Enter Your Mobile Number ",placeholder="...")
            other=st.text_input("Any other relevant details? ",placeholder="...")
            submitted=st.form_submit_button("Submit data")
            lof="lost"
            if(submitted):
                if(name=="" or place==""):
                    st.error("Enter All Required Fields")
                else:
                    db.insert_entry(st.session_state["curlogin"],str(date),name,place,number,other,lof)
                    st.success("Data Saved Successfully")

    elif(selected=="Found"):
        st.warning("Before Submitting a form make sure to check for your item in the 'Found Items' coulmn")
        with st.form("found_entry_form",clear_on_submit=True):
            st.header("Found Portal")
            date=st.date_input("Enter the date on which the object is found")
            name=st.text_input("Enter the name of the object found",placeholder="...")
            place=st.text_input("Where is it found ?",placeholder="...")
            number=st.text_input("Enter Your Mobile Number ",placeholder="...")
            other=st.text_input("Any other relevant details? ",placeholder="...")
            lof="found"
            submitted=st.form_submit_button("Submit data")
            if(submitted):
                #write the data inputted to database:
                db.insert_entry(st.session_state["curlogin"],str(date),name,place,number,other,lof)
                st.success("Data Saved Successfully")

    elif(selected=="Lost Items"):
        items=["Select an Item"]
        lost=db.all_found()
        for user in lost:
            if(user["status"]==""):
                items.append(user["name"])
        option=st.selectbox(
            "Claim a Lost Item : ",
            tuple(items),
            0
        )
        dev={}
        for user in lost:
            if(user["name"]==option):
                with st.form("Claim Lost Object",clear_on_submit=True):
                    st.subheader("Claim Lost Item")
                    st.write("Item : "+user["name"])
                    st.write("Place Where it is Lost : "+user["place"])
                    st.write("Other Details : "+user["other"])
                    check=st.checkbox("I Accept that this claim is legit")
                    sub=st.form_submit_button("Claim")
                    if(sub and check):
                        st.write("Your Item was found by "+user["username"]+" You can contact him\her at "+user["number"])
                        st.warning("The Contact will be shown only once for security reasons , kindly note the contact details")
                        return db.f_change_status(user["key"],st.session_state["curlogin"])


    elif(selected=="Found Items"):
        items=["Select an Item"]
        found=db.all_lost()
        for user in found:
            if(user["status"]==""):
                items.append(user["name"])
        option=st.selectbox(
            "Return a Found Item : ",
            tuple(items),
            0
        )
        dev={}
        for user in found:
            if(user["name"]==option):
                with st.form("Return Found Object",clear_on_submit=True):
                    st.subheader("Return Found Item")
                    st.write("Item : "+user["name"])
                    st.write("Place Where it is found : "+user["place"])
                    st.write("Other Details : "+user["other"])
                    sub=st.form_submit_button("Return")
                    if(sub):
                        st.write("The Item belongs to "+user["username"]+" You can contact him\her at "+user["number"])
                        st.warning("The Contact will be shown only once for security reasons , kindly note the contact details")
                        return db.l_change_status(user["key"],st.session_state["curlogin"])


if "key" not in st.session_state:
    st.session_state["key"] = "log_sign"

if st.session_state["key"] == "log_sign":
    log_sign()
elif st.session_state["key"] == "main":
    main()

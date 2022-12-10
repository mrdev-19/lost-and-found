import os
from deta import Deta
from dotenv import load_dotenv

#load env var

load_dotenv(".env")

DETA_KEY=os.getenv("DETA_KEY")
deta=Deta(DETA_KEY)

ldb=deta.Base("Lost")
rdb=deta.Base("Found")
cred=deta.Base("Creds")

def insert_user(username,password,email):
    username=username.strip()
    dev=fetch_all_users()
    usernames=[]
    emails=[]
    for user in dev:
        usernames.append(user["key"])
        emails.append(user["email"])
    if(username in usernames):
        return "Username already exists!\nTry another username !"
    elif(email in emails):
        return "email already exists!\nTry with another email !"
    else:
        cred.put({"key":username,"password":password,"email":email})

def authenticate(username,password):
    username=username.strip()
    var=1
    dev=fetch_all_users()
    usernames=[user["key"] for user in dev]
    emails=[user["email"] for user in dev]
    for user in dev:
        if(username==user["key"] and user["password"]==password):
            return True
            var=0
    if(var):
        return False

def fetch_all_instances():
    dev=entries.fetch()
    res=dev.items
    return res

def fetch_all_users():
    res=cred.fetch()
    return res.items

def fetch_all_entries(username):
    data=[]
    dev=entries.fetch()
    res=dev.items
    for user in res:
        if user["username"]==username:
            data.append({"Entry":user["data"],"Date":user["date"]})
    return data

def insert_entry(username,date,name,place,number,other,lof):
    if(lof=="lost"):
        return ldb.put({"date": date,"name": name,"place": place,"number":number,"username":username,"other": other,"status":""})
    else:
        return rdb.put({"date": date,"name": name,"place": place,"number":number,"username":username,"other": other,"status":""})

def all_lost():
    dev=ldb.fetch()
    dev=dev.items
    return dev

def all_found():
    dev=rdb.fetch()
    dev=dev.items
    return dev

def f_change_status(data,key):
    found=all_lost()
    for user in found:
        print(user)
        if(user["name"]==key):
            print("data found dude")
            user["status"]=data

def l_change_status(username,upd):
    updates={"status":upd}
    ldb.update(updates,username)

def f_change_status(username,upd):
    updates={"status":upd}
    rdb.update(updates,username)

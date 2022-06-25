# EZ-Labs-REST-API

This project is demonstrate a REST API implementation for EZ Labs user management with following features

## Operation/Admin User

Actions available to user (Already created in the system)
1. Login
2. Disable or Enable a client from accessing his/her account

## Client User

Actions available to user -
1. Sign Up 
2. Email Verify ( A unique verification link, no mail service due to latest google policy for less secured apps, using link client can verify themselves.)
3. Login
4. Logout

# Installation:

+ Create a new directory for project and clone this repo
```
git clone https://github.com/newrouge/newrouge-EZ-Labs-REST-API.git
cd newrouge-EZ-Labs-REST-API
```

+ Create a virtual environment for project named `flask` and install all dependencies

```
python3 -m venv flask

source flask/bin/activate

pip install -r requirements.txt
```





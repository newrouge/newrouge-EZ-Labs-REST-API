# EZ-Labs-REST-API

This project is to demonstrate a REST API implementation for EZ Labs user management with following features

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

  ![Screenshot from 2022-06-25 14-41-25](https://user-images.githubusercontent.com/79413473/175766697-11bb5c56-5b5b-4b5d-a277-84331d5f686b.png)
  
  ![Screenshot from 2022-06-25 14-41-51](https://user-images.githubusercontent.com/79413473/175766702-d90d1a62-92a1-43db-804e-9ebc416cf003.png)


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
# Starting the app

+ export `FLASK_APP` environment variable to tell the flask where is actual app

```
export FLASK_APP=api/
```
+ Depending on your need if you want to run application in `DEBUG` mode, otherwise flask run in production mode by default

```
export FLASK_ENV=development
```
```
flask run
```

![Screenshot from 2022-06-25 14-41-06](https://user-images.githubusercontent.com/79413473/175767027-bc9487ea-25f8-4211-9ea3-9f4470d2e4ee.png)

You can access your application at `localhost:5000`


# Test credentials

```
Username: admin
Email: admin@ez.com
Password: admin
Role: Admin
```
```
Username: string
Email: string@gmail.com
Password: string
Role: Client
```

# API Endpoints 

API has following endpoints

## User Registration: 
```
POST /auth/signup
```

## User Login
```
POST /auth/login
```

## 🔓 User fetches own profile
```
GET /clients/profile
```

## 🔓 Generate Email verification link
```
GET /clients/verify/{client_username}
```

## 🔓 Confirm Email with link
```
GET /clients/confirm_email/{unique_token}
```

## 🔐 Admin user list all users
```
GET /admin/listusers
```

## 🔐 Admin fetch one single user's details
```
GET /admin/profile/{username}
```

## 🔐 Admin Changing user's profile access (Enable/Disable)
```
POST /admin/profile/access
```





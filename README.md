# Library Management
This is a Library Management Web App. This app will help admin perform tasks smoothly.


### Admin can perform following tasks
- Create Admin account and Login.
- Can Issue Book (added by Admin) to registered student.
- Can Add, View, Delete and Update Books present in the system.
- Can view Issued book with issued date and expiry date.
- Can view Fine (15 rupees for each day after expiry date).
- Can View Students that are registered into system.
- Can Add, Delete and Update Students.
- Can Import and add new Books.

## HOW TO RUN THIS PROJECT
- Install Python(3.12) (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :
```
python -m pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```

For creating admin User to Login please use below command
```
python manage.py createsuperuser
```

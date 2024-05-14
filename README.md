# Library Management
Welcome to our Library Management App! This App is designed to streamline and enhance the administrative tasks of running a library. From organizing books to managing students and tracking book issues, our app helps library administrators to efficiently handle all aspects of library operations.

### Admin can perform following tasks using this Web App
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

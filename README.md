## To set up the project follow the following steps:

1. Clone the repository by running the following command
   `git clone https://github.com/m4ace1/django-class`
2. Opn the project with any IDE of your choice
3. Create a virtual environment by running: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate` for Mac and
   linux users `\venv\Scripts\activate` for Windows users
5. Install the dependencies by running the following command
   `pip install -r requirements.txt`
6. change your directory to backend directory using `cd backend`
7. start the server by running: `python manage.py runserver 8000` this will run
   the server on port 8000 you can then proceed to test the endpoint on your
   postman using http://localhost:8000/api/blogs/

> NOTE: This app uses postgresql database so you will need to configure the
> database in [settings.py](/backend/blog/settings.py) by udating the username
> and password.

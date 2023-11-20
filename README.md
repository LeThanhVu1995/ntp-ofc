#### Backend

Before you install the python dependencies you need to install the virtualenv and activate it, in order
to do it please execute these commands one by one in a new command prompt window (cmd).

```
cd python-vue-spa-boilerplate\backend
pip install virtualenv
virtualenv venv
cd venv\Scripts\
activate
cd ..
cd ..
```

Using the same command prompt, go to the backend folder (if you are not in there yet) and run the pip install requirements.txt command

```
pip install -r ./requirements.txt
```

Once the pip have installed all the dependencies you need to create the database structure, to do it there is
python script that does it for you, just execute this command:

```
python databaseCreation.py
```

If you didn't get any error, you can run the backend API using this command below:

```
python app.py
```

You can check if the API is running accessign the address http://localhost:5000/home you should receive Unauthorized message, if you got it the API is runing.

Now let us start the Frontend

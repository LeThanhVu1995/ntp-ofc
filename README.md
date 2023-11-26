#### Backend

```
cd ntp_ofc_api
pip install virtualenv
virtualenv venv
cd venv\bin\
activate
cd ..
cd ..
```

Using the same command prompt, go to the backend folder (if you are not in there yet) and run the pip install requirements.txt command

```
pip install -r ./requirements.txt
```

If you didn't get any error, you can run the backend API using this command below:

```
python app.py
```

You can check if the API is running accessign the address http://localhost:5000/home you should receive Unauthorized message, if you got it the API is runing.

Now let us start the Frontend

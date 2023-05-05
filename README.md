# 420-project

## URL: 10.172.10.235:8000/

## List of Group Members:
    1. Shu Ya Liu ()
    2. Vincent Keedwell (2137034)
    3. Adriano D'Alonzo (2035770)

## Development Setup Steps:
    a) Install Python 3.7 or greater
    b) Create a virtual environment [ Windows: `py -m venv .venv` ] [ Linux/Mac: `python3 -m venv .venv` ]
    c) Activate virtual environment [ Windows: `.venv\Scripts\activate` ] [ Linux/Mac: `. .venv/bin/activate` ]
    d) Install requirements [ `pip install -r requirements.txt` ]
    e) Setup Database credentials by setting DBUSER and DBPWD environment variables [ Windows: `set` ] [ Linux/Mac: `export` ]
    f) Be sure you're connected to the Dawson network (VPN or local connection) in order to connect to the Database
    g) Setup the Database by running `schema.sql` located in the `sql` directory to initialize the Database.
    h) Run the application [ flask --app Application --debug run ] 

## Deployment Setup Steps:
    a) Install Python 3.7 or greater
    b) Create a virtual environment [ Windows: `py -m venv .venv` ] [ Linux/Mac: `python3 -m venv .venv` ]
    c) Activate virtual environment [ Windows: `.venv\Scripts\activate` ] [ Linux/Mac: `. .venv/bin/activate` ]
    d) Install requirements [ `pip install -r requirements.txt` ]
    e) Setup Database credentials by setting DBUSER and DBPWD environment variables [ Windows: `set` ] [ Linux/Mac: `export` ]
    f) Be sure you're connected to the Dawson network (VPN or local connection) in order to connect to the Database
    g) Setup the Database by running `schema.sql` located in the `sql` directory to initialize the Database.
    h) Run the application [ gunicorn -b 0.0.0.0:8000 'Application:create_app()' ] 

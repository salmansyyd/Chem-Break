# ChemBreak Breakage App

A web application built using Flask, MySQL, and other Python Flask extensions that allow Degree College Teachers to manage breakage records in their laboratory.

## Features

Secure login for teachers
Add, view, and manage breakage records
Add, edit, and delete apparatus data
Print breakage records in XLS format
Easy to use interface

## Requirements

Python 3.x
Flask
Flask-WTF
Flask-MySQLdb
openpyxl

## Installation

Clone the repository and navigate to the project folder.

```
git clone https://github.com/<your-username>/flask-breakage-app.git
cd flask-breakage-app
Create a virtual environment.
```

```
python3 -m venv env
Activate the virtual environment.
```

```
source env/bin/activate
Install the required packages.
```

```
pip install -r requirements.txt
Create a MySQL database.
```

```
CREATE DATABASE flask_breakage_app;
Create the required tables in the database.
```

```
python create_tables.py
Set the FLASK_APP environment variable.
```

```
export FLASK_APP=app
Run the application.
```

```
flask run
The application should now be running on http://localhost:5000.
```

## Usage

Navigate to http://localhost:5000 in your browser.

Login with your credentials.

Use the navigation bar to add, view, or manage breakage records.

Use the print report feature to export breakage records in XLS format.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

MIT

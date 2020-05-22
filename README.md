### Instructions

To run the application, follow the steps

---

1. **Install Python and create a virtualenv with Python 3.6+. There's many ways. See the example**:

      Example: `python -m venv env`

---

2. **Active your virtualenv. To do this, see below**:

    If you use Windows type this command at the prompt: `\path\to\env\Scripts\activate`
    
    *`\path\to\env` is your virtualenv's path*

    
    If you use Mac or Linux type the command at the terminal: `source env/bin/activate`

    *You should be inside the path at your was created the virtualenv*

---

3. **Install all the requirements. Open your terminal at the root path application and type the command**:
    
    `pip install -r requirements.txt`

---

4. **Export FLASK_APP and FLASK_ENV variables to run the application**

    If you use Windows, type: `set FLASK_APP=manage.py` and then `set FLASK_ENV=development` to run the application on debug mode

    
    If you use Mac or Linux, type this commands: `export FLASK_APP=manage.py` and `export FLASK_ENV=development`

---

5. **Open your favorite web browser an use it. The default port is 5000 then go to the address**
    
    http://localhost:5000

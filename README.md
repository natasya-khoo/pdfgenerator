# Notebook Issue Form and Navigation Project

## Overview

This project main purpose is to be imported from CSPTS so that user can 

## Project Structure

** sidenav.py **
- Contains the sidebar navigation structure and the main window.
- Root or main window to guide to different forms

** forms **

- **notebookissueform.py**
    - 

- **base_form.py / button_functions.py**  
  - `base_form.py` provides a base class with common functionalities (e.g., creating a database connection, submitting data, navigating back).  
  - Alternatively, `button_functions.py` can be used to store independent helper functions for button actions, which are then imported into every form python files.

- **navigate.py**  
  To navigate to different forms or to choose the form to start with.

- **config.py**  
  Stores PostgreSQL database configuration in a dictionary named `DB_CONFIG`.
  Change this config files as the change of DB.

- **README.md**  
  This documentation file. 

## Table created for the project
- soitua (User access system Form)
- soitsr (Service Request Form)
- soitni (Notebook Issue Form)

## Guides to write new form usage 
1. Turning it from a standalone application into a frame-based one.
2. Remove the main() function and instead create a class that inherits from tk.Frame. The __init__ method will take parent and controller as arguments. Change global variables into instance variables, using self.com_entry and so on.

## Dependencies

- **Python 3.13**
- **Tkinter** 
- **psycopg2** or **psycopg2-binary** (for PostgreSQL connectivity)

You can install the required dependencies via pip:

```bash
pip install -r requirements.txt
pip install psycopg2-binary customtkinter


#   p d f g e n e r a t o r  
 
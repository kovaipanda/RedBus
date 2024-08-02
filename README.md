# RedBus
Bus Routes Data Scraping and Analysis Project
Table of Contents
1 Introduction
2 Project Structure
3 Prerequisites
4 Setup
    Database Setup
    Python Environment Setup
5 Running the Scraping Script
6 Running the Streamlit Application
7 Deliverables
8 Streamlit application showing data filtering/ analysis

Introduction

This project involves scraping bus route data from a webpage, storing it in a MySQL database, and creating a Streamlit application to visualize and analyze the data.


Project Structure

Bus_Routes_Project/
│
├── scripts/
│   ├── scraper.py
│   └── streamlit_app.py
│
├── sql/
│   └── setup_database.sql
│
├── requirements.txt
│
└── README.md

scripts/: Contains the Python scripts for data scraping and the Streamlit application.
scraper.py: Script to scrape bus route data and store it in a MySQL database.
streamlit_app.py: Script to run the Streamlit application for data visualization.
sql/: Contains SQL scripts for setting up the MySQL database.
setup_database.sql: SQL script to create the database and tables.
requirements.txt: List of Python dependencies required for the project.
README.md: Project documentation.


Prerequisites

Python 3.7+
MySQL server
Chrome WebDriver for Selenium
Streamlit


Setup
Database Setup
Install MySQL
Run SQL Script

Python Environment Setup
Create a virtual environment
Install dependencies
Set up Chrome WebDriver

Running the Scraping Script
Configure MySQL Connection: Update the MySQL connection details in scraper.py

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="redbus_1"
)

Run the scraper:
python scripts/scraper.py

This will scrape the bus route data and store it in the bus_routes table in the redbus_1 database.

Running the Streamlit Application
Run the Streamlit app:
streamlit run scripts/streamlit_app.py
This will start the Streamlit server and open the application in your web browser.

Deliverables
Source Code: The complete source code for the data scraping script and the Streamlit application.
SQL Scripts: SQL scripts for creating and populating the database.
Documentation: This README file with detailed instructions.
Streamlit Application: A web application to visualize and analyze the scraped bus route data.


Streamlit application showing data filtering/ analysis

![C](https://github.com/user-attachments/assets/b8488712-e6dd-4355-8bfb-fe5f1bde480a)
![C5](https://github.com/user-attachments/assets/2ba53f69-ee73-4601-94d5-c5523e08453f)
![C4](https://github.com/user-attachments/assets/211040c4-5cf3-4001-ad10-c1a00597bbf4)
![C3](https://github.com/user-attachments/assets/55c276f2-7c71-402d-a9ba-c93c3deb5cc3)
![C2](https://github.com/user-attachments/assets/aa515db8-96e1-4185-841b-e09eb47ed45d)


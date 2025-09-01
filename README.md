# Investor-s-Assistant-App
This project is a virtual assistant that monitors stock prices, visualizes historical data, and sends email notifications when specific price thresholds are reached. The application was built in Python using the Flask framework, which allows it to run as a simple website.

Features
Stock data retrieval: The application uses the free Yahoo Finance API (yfinance) to retrieve current and historical stock prices.
Chart visualization: It uses the Matplotlib library to generate historical price charts.
Configuration: The list of monitored symbols is stored in the config.json file, making it easy to manage them without editing the code.
Web application: The whole thing works as a simple web application built on the Flask framework.

Requirements
Before running the application, make sure you have Python version 3.6 or newer installed.
Installation
Clone the repository (if you use Git) or download the project files.

Run the application for the first time. A config.json file with default symbols will be created automatically.
You can manually edit this file to add or remove action symbols that you want to monitor.
Running the application:

Bash
python app.py
Open your browser and go to the address provided in the console (usually http://127.0.0.1:5000).

File structure.
├── app.py                  # Main Flask application file
├── config.json             # File with a list of monitored symbols
├── templates/
│   └── index.html          # Home page template
└── static/                 # Folder for static files (charts)

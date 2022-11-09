from flask import Flask
import requests
import json

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')
@app.route('/hello')

def hello():
    # Declare how many results are wanted
    drawings = 10
    topNumbers = 10

    # Pull numbers from API, calculate stats
    pNumbers = PBNumbers(drawings)
    pRecurring = HighestRecurring(pNumbers.results(), topNumbers)


    # Render the page
    # return pNumbers.results()
    return str(pRecurring.results())

class PBNumbers:
    # Pull the defined number of winning number drawings
    def __init__(self, drawings):
        self.drawings = drawings
        
    def results(self):
        api_url = "https://data.ny.gov/resource/d6yy-54nr.json?$select=winning_numbers&$limit={}".format(self.drawings)
        response = requests.get(api_url)
        return response.json()

class HighestRecurring:
    # Calculate the stats for the winning numbers retrieved
    def __init__(self, response, topNumbers):
        self.response = response
        self.topNumbers = topNumbers

    def results(self):
        highestRecurring = self.response.count(10)
        return highestRecurring

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)



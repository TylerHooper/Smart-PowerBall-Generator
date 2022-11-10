from flask import Flask
from IPython.display import display
import requests as rq
import pandas as pd

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')
@app.route('/spbgen')

def spbgen():
    # Declare how many results are wanted
    drawings = 200
    topNumbers = 20

    # Pull numbers from API, calculate stats
    pNumbers = PBNumbers(drawings)
    pTopNum = HighestRecurring(pNumbers.results(), topNumbers)
    display(pTopNum.whiteNumbers())
    display(pTopNum.redNumbers())

    # Render the page
    return "success"

class PBNumbers:
    # Pull the defined number of winning number drawings
    def __init__(self, drawings):
        self.drawings = drawings
        
    def results(self):
        api_url = "https://data.ny.gov/resource/d6yy-54nr.json?$select=winning_numbers&$limit={}".format(self.drawings)

        # Get winning_numbers data, convert to DataFrame, split numbers into columns
        response = pd.concat([pd.DataFrame(rq.get(api_url).json())['winning_numbers'].str.split(' ', expand=True)], axis=1)
        return response

class HighestRecurring:
    # Calculate the stats for the winning numbers retrieved
    def __init__(self, response, topNumbers):
        self.response = response
        self.topNumbers = topNumbers

    def whiteNumbers(self):
        # Pull white number columns, stack numbers into series, count values and assign column names
        topWhiteNumbers = self.response[[0, 1, 2, 3, 4]].stack().value_counts(sort=True).reset_index()
        topWhiteNumbers.columns = ['number', 'count']

        # Return the desired quantity of top white numbers
        return topWhiteNumbers.iloc[0:self.topNumbers]
    
    def redNumbers(self):
        # Pull red number column as series, count values and assign column names
        topRedNumbers = self.response[5].value_counts(sort=True).reset_index()
        topRedNumbers.columns = ['number', 'count']

        # Return the desired quantity of top red numbers
        return topRedNumbers.iloc[0:self.topNumbers]


if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)



# Data visualization from Chess.com

## Summary
Fetch data from Chess.com API and visualize them in a Dash application.

## Running the application

Run the following command and open the local host web address chosen by Dash.

``python3 ./index.py``

## Fetching data from Chess.com API

Run the following command to get information about how to fetch data.

``python3 ./fetch_data.py -h``

## Running tests

Run the following command to run tests

``python3 -m pytest``

or push to semestral or semestral-tests branch to run the tests on Gitlab CI.

## Analyse code

Run the following command to analyse code.

``python3 -m pylint app --disable=C0301,C0103``
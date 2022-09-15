#import Data Analysis packages
import numpy as np
import pandas as pd

# Import API packages
from fastapi import FastAPI

app = FastAPI()

@app.get('/constructors')
def constructors():
    file = pd.read_json("Datasets\constructors.json", lines=True) 
    return file.to_dict()

@app.get('/circuits')
def circuits():
    file = pd.read_json("Datasets\circuits.json")
    return file.to_dict()

@app.get('/drivers')
def drivers():
    file = pd.read_json("Datasets\drivers.json", lines=True)
    return file.to_dict()

@app.get('/pit_stops')
def pits():
    file = pd.read_json('Datasets\pit_stops.json')
    return file.to_dict()

@app.get('/races')
def name():
    file = pd.read_csv('Datasets\\races.csv')
    return file.to_dict()

@app.get('/results')
def name():
    file = pd.read_json('Datasets\\results.json', lines=True)
    return file.to_dict()


#get queries
@app.get('/year-with-most-races')
def race_year():
    df = pd.read_csv("Datasets\\races.csv")
    most_races = df.groupby('year').year.count()
    most_races = int(most_races.idxmax())
    return {'Year': most_races}

@app.get('/greatest-driver')
def find_driver():
    results_df = pd.read_json('Datasets\\results.json', lines=True)
    drivers_df = pd.read_json('Datasets\drivers.json', lines=True)
    
    results_driver_position = results_df[['raceId', 'driverId', 'position']] 
    results_driver_position = results_driver_position.merge(drivers_df, on='driverId')

    results_driver_position = results_driver_position[results_driver_position['position'] == 1]
    driver_name = results_driver_position.name.value_counts().idxmax()
    driver_name = f"{driver_name['forename']} {driver_name['surname']}"
    return {'driver': driver_name}

@app.get('/most-runned-circuit')
def find_circuit():
    races_df = pd.read_csv('Datasets\\races.csv')
    circuits_df = pd.read_json('Datasets\circuits.json')

    id = races_df.circuitId.value_counts().idxmax()
    circuit_name = circuits_df[circuits_df.circuitId == id]['name'].iloc[0]
    
    return {"circuit":circuit_name}

@app.get('/driver-with-most-points')
def points():
    results_df = pd.read_json('Datasets\\results.json', lines=True)
    drivers_df = pd.read_json('Datasets\drivers.json', lines=True)

    big_results_df = results_df.merge(drivers_df, on='driverId')[['driverId', 'points', 'name', 'nationality']]
    big_results_df = big_results_df[(big_results_df.nationality == 'British') | (big_results_df.nationality == 'American')]

    driver_with_most_points = big_results_df.groupby('driverId').points.count().sort_values(ascending=False).idxmax()
    driver_name = big_results_df[big_results_df['driverId'] == driver_with_most_points]['name'].iloc[0]
    driver_name = {'driver': f"{driver_name['forename']} {driver_name['surname']}"}
    return driver_name
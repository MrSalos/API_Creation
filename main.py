#import packages
import numpy as np
import pandas as pd
from fastapi import FastAPI

#Create a FastAPI instance. In this cases is called app
app = FastAPI()

# Using decorators and the .get method we will feed our API with different datasets
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


#Here we are going start querying our datasets and upload those queries into our API

# First query: Year with most races
@app.get('/year-with-most-races')
def race_year():
    # Create dataframe
    df = pd.read_csv("Datasets\\races.csv")
    
    most_races = df.groupby('year').year.count()
    most_races = int(most_races.idxmax())
    
    return {'Year': most_races}

# Second query: Driver with most first places
@app.get('/greatest-driver')
def find_driver():
    #create dataframes
    results_df = pd.read_json('Datasets\\results.json', lines=True)
    drivers_df = pd.read_json('Datasets\drivers.json', lines=True)
    
    results_driver_position = results_df[['raceId', 'driverId', 'position']]
    results_driver_position = results_driver_position.merge(drivers_df, on='driverId')
    results_driver_position = results_driver_position[results_driver_position['position'] == 1]
    
    driver_name = results_driver_position.name.value_counts().idxmax()
    driver_name = f"{driver_name['forename']} {driver_name['surname']}"
    
    return {'driver': driver_name}

# Third query: Most runned circuit
@app.get('/most-runned-circuit')
def find_circuit():
    races_df = pd.read_csv('Datasets\\races.csv')
    circuits_df = pd.read_json('Datasets\circuits.json')

    id = races_df.circuitId.value_counts().idxmax()
    circuit_name = circuits_df[circuits_df.circuitId == id]['name'].iloc[0]
    
    return {"circuit":circuit_name}

#fourth query: Driver with most points whose American or British
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
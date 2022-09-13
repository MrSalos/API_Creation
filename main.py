#import Data Analysis packages
import numpy as np
import pandas as pd

# Import API packages
from fastapi import FastAPI

app = FastAPI()

@app.get('/constructors')
def hello():
    file = pd.read_json("Datasets/constructors.json", lines=True) 
    return file
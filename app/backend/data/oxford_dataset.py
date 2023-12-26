import pandas as pd
import os
from animal_detection.app.backend.breed_detection.settings import DATA_DIR_PATH

breeds_df = pd.DataFrame()

def load_breeds():
    global breeds_df
    breeds_df = pd.read_csv(os.path.join(DATA_DIR_PATH, 'oxford_dataset.csv'))
    
    
def get_breeds_data():
    global breeds_df
    if (breeds_df.empty):
        load_breeds()
    return breeds_df
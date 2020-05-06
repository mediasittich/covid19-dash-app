import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats.mstats import gmean

# ========================================
#              LOAD DATA
# ========================================
PROJECT_PATH = ''
project_path = Path(__file__).parent.parent.absolute()
DATA_PATH = ''
data_path = os.path.join(project_path, 'data')
external_data_path = os.path.join(data_path, 'external', '')
processed_data_path = os.path.join(data_path, 'processed', '')

# COVID-19 Dataset (Source: RamiKrispin GitHub)
corona_data_url = 'https://raw.githubusercontent.com/RamiKrispin/coronavirus-csv/master/coronavirus_dataset.csv'
# Population Data
population_data_filename = ''
# Government Response Data
government_response_data_url = ''

df = pd.read_csv(corona_data_url)

df = df[(df['Country.Region'] == 'Germany') & (
    df['type'] == 'confirmed')]  # [['Country.Region', 'date', 'cases']]


# ========================================
#              PRE-PROCESSING
# ========================================

# ------------ Remove Cruise ships from Dataset ------------


# ------------ Clean up Province.State ------------


#  ------------ Update Country Names to Official Names ------------


#  ------------ Add Column 'DisplayName' for Shorter Names in Figures ------------


#  ------------ Add ISO Codes to Countries ------------


#  ------------ Update Country Names to Official Names ------------

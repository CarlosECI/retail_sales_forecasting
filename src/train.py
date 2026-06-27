import os
import joblib
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(BASE_DIR, 'models')
DATA_RAW = os.path.join(BASE_DIR, 'data', 'raw', 'icm_general.csv')

def train_sarima():
    df = pd.read_csv(DATA_RAW)
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # interpolación sobre outlier del covid
    mask_covid = (df['fecha'] >= '2020-03-01') & (df['fecha'] <= '2020-04-01')
    
    df['valor_icm_clean'] = df['valor'].copy()
    df.loc[mask_covid, 'valor_icm_clean'] = np.nan
    df['valor_icm_clean'] = df['valor_icm_clean'].interpolate(method='linear')
    
    serie = df.set_index('fecha')['valor_icm_clean']
    serie.index.freq = serie.index.inferred_freq
    
    model = SARIMAX(
        serie,
        order=(2, 1, 1),
        seasonal_order=(0, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    
    model = model.fit(disp=False)
    
    return model

if __name__ == '__main__':
    model_sarima = train_sarima()
    joblib.dump(model_sarima, os.path.join(MODELS, 'model_sarima.pkl'))
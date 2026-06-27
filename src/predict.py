import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(BASE_DIR, 'models', 'model_sarima.pkl')
REPORTS = os.path.join(BASE_DIR, 'reports')

def predictions():
    model = joblib.load(MODELS)

    predictions_final = model.forecast(steps=3)
    intervalos = model.get_forecast(steps=3).conf_int()

    df = pd.DataFrame({
        'fecha': predictions_final.index,
        'predicciones': predictions_final.values,
        'int_conf_bajo': intervalos.iloc[:, 0],
        'int_conf_alto': intervalos.iloc[:, 1],
    }).reset_index(drop=True)

    return df

if __name__ == '__main__':
    prediccion_sarima = predictions()
    prediccion_sarima.to_csv(os.path.join(REPORTS, 'predictions.csv'), index=False)
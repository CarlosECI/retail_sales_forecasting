import requests
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, 'data', 'raw')


def extraer_serie_ine(codigo_serie, nult=300):
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{codigo_serie}?nult={nult}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print(f'Timeout al consultar la serie {codigo_serie}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'Error al consultar la serie {e}')
        return None
    
    if 'Data' not in data:
        print(f'La respuesta no contiene datos para {codigo_serie}')
        return None
        
    registros = [
        {
            'fecha': entry['Fecha'],
            'valor': entry['Valor'],
        }
        for entry in data['Data']
    ]

    df = pd.DataFrame(registros)
    df['fecha'] = pd.to_datetime(df['fecha'], unit='ms')
    df = df.sort_values('fecha').reset_index(drop=True)
    
    return df

if __name__ == '__main__':
    df_icm = extraer_serie_ine('ICM3821')
    df_ipc = extraer_serie_ine('IPC251852')

    df_icm['fecha'] = df_icm['fecha'].dt.to_period('M').dt.to_timestamp()
    df_ipc['fecha'] = df_ipc['fecha'].dt.to_period('M').dt.to_timestamp()

    df_icm.to_csv(os.path.join(DATA_RAW, 'icm_general.csv'), index=False)
    df_ipc.to_csv(os.path.join(DATA_RAW, 'ipc_general.csv'), index=False)
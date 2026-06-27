import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT = os.path.join(BASE_DIR, 'src', 'extract.py')
TRAIN = os.path.join(BASE_DIR, 'src', 'train.py')
PREDICT = os.path.join(BASE_DIR, 'src', 'predict.py')

def pipeline():
    archivos = [
        EXTRACT,
        TRAIN,
        PREDICT
    ]
    
    for archivo in archivos:
        print(f'Ejecutando {archivo}...')
        try:
            resultado = subprocess.run(['python', archivo], check=True, capture_output=True, text=True)
            print(f'Salida de {archivo}:\n{resultado.stdout}')
        except subprocess.CalledProcessError as e:
            print(f'Error al ejecutar {archivo}. Detalles:\n{e.stderr}')
            sys.exit(1)

if __name__ == '__main__':
    pipeline()
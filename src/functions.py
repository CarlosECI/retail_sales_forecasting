from sklearn.metrics import mean_absolute_percentage_error
import numpy as np

def walk_forward_validation(serie, modelo_func, min_train=96, horizonte=3):
    errores = []
    n = len(serie)
    
    for i in range(min_train, n - horizonte + 1, horizonte):
        train = serie.iloc[:i]
        test = serie.iloc[i: i + horizonte]
        
        try:
            predicciones = modelo_func(train, horizonte)
            mape = mean_absolute_percentage_error(test, predicciones)
            errores.append(mape)
        except Exception as e:
            print(f'Error en ventana {i}: {e}')
            continue
        
    return {
        'mape_medio': np.mean(errores),
        'mape_std': np.std(errores),
        'n_ventanas': len(errores)
    }
    
def naive_seasonal(train, horizonte, periodo=12):
    ultimos_valores = train.iloc[-periodo:].values
    predicciones = []
    
    for i in range(horizonte):
        predicciones.append(ultimos_valores[i % periodo])
        
    return np.array(predicciones)
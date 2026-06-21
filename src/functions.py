from sklearn.metrics import mean_absolute_percentage_error
import numpy as np
import pandas as pd

def walk_forward_validation(data, modelo_func, min_train=96, horizonte=3, features=None, target=None):
    errores = []
    n = len(data)
    
    if features is not None and target is not None:
        for i in range(min_train, n - horizonte + 1, horizonte):
            X = data[features].iloc[:i,:]
            y = data[target].iloc[:i]
            y_test = data[target].iloc[i:i + horizonte]
            
            X_test = data[features].iloc[i: i + horizonte]
            
            try:
                predicciones = modelo_func(X, y, X_test)
                mape = mean_absolute_percentage_error(y_test, predicciones)
                errores.append(mape)
            except Exception as e:
                print(f'Error en ventana {i}: {e}')
                continue
    else:
        for i in range(min_train, n - horizonte + 1, horizonte):
            train = data.iloc[:i]
            test = data.iloc[i: i + horizonte]
            
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
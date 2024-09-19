import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_prepare_data(file_path):
    # Cargar el dataset
    data = pd.read_csv(file_path)
    
    # Eliminar filas con valores faltantes
    data = data.dropna()

    # Extraer las características y la variable objetivo
    features = data.iloc[:, 6:]  # Desde la columna 6 en adelante están los cursos
    target = data['Hogwarts House']
    
    # Convertir la variable objetivo a números
    target = pd.factorize(target)[0]
    
    # Normalizar las características
    scaler = StandardScaler()
    features = scaler.fit_transform(features)
    
    return features, target

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def compute_cost(X, y, theta):
    m = len(y)
    h = sigmoid(X @ theta)
    cost = (-1/m) * (y.T @ np.log(h) + (1 - y).T @ np.log(1 - h))
    return cost

def gradient_descent(X, y, theta, alpha, num_iters):
    m = len(y)
    cost_history = []
    
    for _ in range(num_iters):
        gradient = (1/m) * X.T @ (sigmoid(X @ theta) - y)
        theta -= alpha * gradient
        cost = compute_cost(X, y, theta)
        cost_history.append(cost)
    
    return theta, cost_history

def one_vs_all(X, y, num_classes, alpha, num_iters):
    m, n = X.shape
    all_theta = np.zeros((num_classes, n + 1))
    X = np.insert(X, 0, 1, axis=1)  # Añadir columna de 1s para el término de bias
    
    for i in range(num_classes):
        binary_y = np.where(y == i, 1, 0)
        theta = np.zeros(X.shape[1])
        theta, _ = gradient_descent(X, binary_y, theta, alpha, num_iters)
        all_theta[i, :] = theta
    
    return all_theta

def save_model(all_theta, filename='trained_weights.csv'):
    np.savetxt(filename, all_theta, delimiter=",")

def main(file_path):
    features, target = load_and_prepare_data(file_path)
    
    num_classes = len(np.unique(target))
    alpha = 0.1  # Tasa de aprendizaje
    num_iters = 1000  # Número de iteraciones
    
    all_theta = one_vs_all(features, target, num_classes, alpha, num_iters)
    
    save_model(all_theta)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])

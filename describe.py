import pandas as pd
import sys

def count_values(column_data):
    count = 0
    for i in column_data:
        count += 1
    return count
def calculate_mean(column_data):
    total = 0
    count = 0
    for value in column_data:
        count += 1
        total += value
    return total / count if count != 0 else 0

def calculate_std(column_data, mean):
    sum_squared_diff = 0
    count = 0
    for value in column_data:
        sum_squared_diff += (value - mean) ** 2
        count += 1
    variance = sum_squared_diff / (count - 1) if count > 1 else 0
    return variance ** 0.5

def calculate_min(column_data):
    try:
        min = column_data[0]
    except IndexError:
        return None
    for value in column_data:
        if value < min:
            min = value
    return min

def calculate_max(column_data):
    try:
        max = column_data[0]
    except IndexError:
        return None
    for value in column_data:
        if value > max:
            max = value
    return max

def calculate_percentile(column_data, percentile):
    sorted_data = sorted(column_data)
    k = (len(sorted_data) - 1) * percentile #posicion que ocupa ese porcentaje de percentil
    f = int(k) #parte entera
    c = k - f #parte decimal
    if f + 1 < len(sorted_data):
        return sorted_data[f] + (sorted_data[f + 1] - sorted_data[f]) * c
    else:
        return sorted_data[f]

def describe_dataset(file_path):
    # Intentar leer el archivo CSV con utf-8
    try:
        data = pd.read_csv(file_path)
    except UnicodeDecodeError:
        # Si falla, intentar con ISO-8859-1
        try:
            data = pd.read_csv(file_path, encoding='ISO-8859-1')
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return
        except pd.errors.EmptyDataError:
            print(f"Error: The file {file_path} is empty.")
            return
        except pd.errors.ParserError:
            print(f"Error: The file {file_path} could not be parsed.")
            return
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return
    except pd.errors.ParserError:
        print(f"Error: The file {file_path} could not be parsed.")
        return


    # Filtrar solo las columnas numéricas
    numeric_data = data.select_dtypes(include=[float, int])

    # Preparar una tabla para almacenar las estadísticas
    columns = numeric_data.columns
    stats = {
        'count': [],
        'mean': [],
        'std': [],
        'min': [],
        '25%': [],
        '50%': [],
        '75%': [],
        'max': []
    }

    
    # Calcular manualmente las estadísticas para cada columna
    for column in columns:
        col_data = numeric_data[column].dropna().tolist()  # Eliminar valores nulos y convertir a lista
        
        if not col_data:  # Si la columna está vacía después de eliminar nulos, omitir
            for stat in stats:
                stats[stat].append(None)
            continue

        # Conteo
        count = count_values(col_data)
        stats['count'].append(count)

        # Media
        mean = calculate_mean(col_data)
        stats['mean'].append(mean)

        # Desviación Estándar
        std = calculate_std(col_data, mean)
        stats['std'].append(std)

        # Mínimo
        min_val = calculate_min(col_data)
        stats['min'].append(min_val)

        # Percentiles
        q25 = calculate_percentile(col_data, 0.25)
        stats['25%'].append(q25)

        q50 = calculate_percentile(col_data, 0.50)  # La mediana
        stats['50%'].append(q50)

        q75 = calculate_percentile(col_data, 0.75)
        stats['75%'].append(q75)

        # Máximo
        max_val = calculate_max(col_data)
        stats['max'].append(max_val)

    # Imprimir la descripción en el formato solicitado
    print(f"{'':<10}{' '.join([f'{col:<15}' for col in columns])}")
    for stat, values in stats.items():
        print(f"{stat:<10}{' '.join([f'{(v if v is not None else 'N/A'):<15}' for v in values])}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: describe.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        describe_dataset(file_path)
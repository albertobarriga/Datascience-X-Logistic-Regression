import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def find_most_similar_courses(data):
    # Filtrar solo las columnas correspondientes a los cursos
    course_columns = [
        "Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
        "Divination", "Muggle Studies", "Ancient Runes", "History of Magic",
        "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"
    ]
    
    courses_data = data[course_columns]
    
    # Manejar datos faltantes: eliminar filas con NaN
    courses_data = courses_data.dropna()
    
    # Calcular la matriz de correlación entre los cursos
    correlation_matrix = courses_data.corr().abs()
    
    # Eliminar la diagonal para evitar seleccionar la misma columna dos veces
    for i in range(len(correlation_matrix)):
        correlation_matrix.iloc[i, i] = 0
    
    # Encontrar el par de cursos con la correlación más alta
    most_similar = correlation_matrix.unstack().idxmax()
    
    return most_similar

def plot_scatter(data, course1, course2):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=data[course1], y=data[course2])
    
    plt.title(f"Scatter Plot of {course1} vs {course2}")
    plt.xlabel(course1)
    plt.ylabel(course2)
    
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scatter_plot.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        try:
            data = pd.read_csv(file_path)

            # Encontrar los dos cursos más similares
            course1, course2 = find_most_similar_courses(data)
            print(f"The two most similar courses are: {course1} and {course2}")

            # Generar el scatter plot
            plot_scatter(data, course1, course2)
            
        except pd.errors.EmptyDataError:
            print("The provided CSV file is empty.")
        except pd.errors.ParserError:
            print("There was an error parsing the CSV file.")
        except Exception as e:
            print(f"An error occurred: {e}")

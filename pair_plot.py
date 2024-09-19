import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def create_pair_plot(data):
    # Filtrar solo las columnas correspondientes a los cursos
    course_columns = [
        "Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
        "Divination", "Muggle Studies", "Ancient Runes", "History of Magic",
        "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"
    ]
    
    # Seleccionar también la columna de 'Hogwarts House' para colorear según la casa
    data = data.dropna(subset=course_columns + ['Hogwarts House'])
    
    # Crear el pair plot
    sns.pairplot(data, vars=course_columns, hue="Hogwarts House", diag_kind="kde", palette="husl")
    
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pair_plot.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        try:
            data = pd.read_csv(file_path)

            # Generar el pair plot
            create_pair_plot(data)
            
        except pd.errors.EmptyDataError:
            print("The provided CSV file is empty.")
        except pd.errors.ParserError:
            print("There was an error parsing the CSV file.")
        except Exception as e:
            print(f"An error occurred: {e}")

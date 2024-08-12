import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def find_most_homogeneous_course(data):
    house_colors = {
        "Gryffindor": "red",
        "Hufflepuff": "yellow",
        "Ravenclaw": "blue",
        "Slytherin": "green"
    }
    
    courses = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col]) and col != "Index"]
    
    min_std_diff = float('inf')
    best_course = None
    
    for course in courses:
        course_data = data[[course, "Hogwarts House"]].dropna()
        
        if not course_data.empty:  # Check if there are rows left after dropping NaN
            std_devs = course_data.groupby("Hogwarts House")[course].std()
            
            if len(std_devs) == 4:  # Ensure all houses are present
                std_diff = std_devs.max() - std_devs.min()
                if std_diff < min_std_diff:
                    min_std_diff = std_diff
                    best_course = course
    
    return best_course

def plot_histogram(data, course):
    house_colors = {
        "Gryffindor": "red",
        "Hufflepuff": "yellow",
        "Ravenclaw": "blue",
        "Slytherin": "green"
    }

    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x=course, hue="Hogwarts House", multiple="stack", kde=False, palette=house_colors)
    
    plt.title(f"Distribution of {course} Scores by House")
    plt.xlabel(f"{course} Scores")
    plt.ylabel("Count")

    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in house_colors.values()]
    labels = list(house_colors.keys())
    plt.legend(handles=handles, labels=labels, title="Hogwarts House", loc='upper right')
    
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 histogram.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        try:
            data = pd.read_csv(file_path)

            best_course = find_most_homogeneous_course(data)
            
            if best_course:
                print(f"The most homogeneous course is: {best_course}")
                plot_histogram(data, best_course)
            else:
                print("No suitable course found.")
        except pd.errors.EmptyDataError:
            print("The provided CSV file is empty.")
        except pd.errors.ParserError:
            print("There was an error parsing the CSV file.")
        except Exception as e:
            print(f"An error occurred: {e}")

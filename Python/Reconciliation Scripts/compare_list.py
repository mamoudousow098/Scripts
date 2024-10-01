import csv
import sys
import os


def compare_tuples(list1, list2):
    # Trouver les éléments présents dans list1 mais pas dans list2
    diff1 = tuple ( [item for item in list1 if item not in list2] )
    
    # Trouver les éléments présents dans list2 mais pas dans list1
    diff2 = tuple( [item for item in list2 if item not in list1])
    
    # Retourner les différences
    return diff1, diff2


def write_differences_to_file(output_path, diff1, diff2):
    with open(output_path, 'w') as file:
        file.write("Différences dans le premier fichier (absent du second fichier):\n")
        file.write(str(diff1) + "\n\n")
        file.write("Différences dans le second fichier (absent du premier fichier):\n")
        file.write(str(diff2) + "\n")


def read_tuples_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        tuples_list = eval(content)  # Utiliser eval pour convertir la chaîne en liste de tuples
    return tuples_list

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <chemin_fichier_input1.csv> <chemin_fichier_input2.csv> <chemin_fichier_output1.txt> <chemin_fichier_output2.txt>")
        sys.exit(1)

    input1_path = sys.argv[1]
    input2_path = sys.argv[2]
    output1_path = sys.argv[3]
    


    # Lire les tuples à partir des fichiers texte
    list1 = read_tuples_from_file(input1_path)
    list2 = read_tuples_from_file(input2_path)

    # Comparer les listes de tuples
    diff1, diff2 = compare_tuples(list1, list2)

   
    write_differences_to_file(output1_path, diff1, diff2)

    print(f"Les différences ont été enregistrées dans {output1_path}.")

if __name__ == "__main__":
    main()
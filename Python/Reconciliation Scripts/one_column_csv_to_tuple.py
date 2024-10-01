import csv
import sys
import os

def csv_to_tuple(input_path, output_path):
    # Vérifier si le fichier d'entrée existe
    if not os.path.isfile(input_path):
        print(f"Le fichier d'entrée {input_path} n'existe pas.")
        sys.exit(1)

    # Lire le fichier CSV et extraire la colonne
    with open(input_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Ignorer l'en-tête
        values = [row[0] for row in csv_reader]

    # Convertir la liste en tuple
    result_tuple = tuple(values)

    # Enregistrer le tuple dans un fichier texte
    with open(output_path, 'w') as txt_file:
        txt_file.write(str(result_tuple))

    print(f"Le tuple a été enregistré dans {output_path}.")

if __name__ == "__main__":
    # Vérifier que les arguments sont passés
    if len(sys.argv) != 3:
        print("Usage: python script.py <chemin_fichier_input.csv> <chemin_fichier_output.txt>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    csv_to_tuple(input_path, output_path)

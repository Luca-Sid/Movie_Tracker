import csv, os.path
def add_row(filename, dati):
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(dati)

def read_csv(filename):
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        reader.__next__()
        out = []
        for record in reader:
            out.append(record)
        return out



# usa absolute path (necessario per funzionare con apache che esegue lo script in altra directory)
base_dir = os.path.dirname(os.path.abspath(__file__))

"""Se define la función para contar nucleóticos """
import re

"""Definimos la función que divide una secuencia larga en varias líneas más cortas.
   Cada línea tendrá un máximo de 60 caracteres """


def formato(sequence, line_length=60):           # esto lo hago para organizar y visualizar mejor la secuancia, el que use el código puede cambiar a su gusto la longitud de cada linea, cambiando el número en line_length
    lineas = []
    for i in range(0, len(sequence), line_length):  
        lineas.append(sequence[i:i + line_length])  

    return "\n".join(lineas)    # Unimos todas las líneas en una sola cadena separadas por saltos de línea.


"""La siguente función se define  para contar nucleóticos y GC"""


def contenido(sequence):
    sequence = sequence.rstrip("\n")
    sequence = sequence.upper()  # convertir todos los caracteres de una cadena a mayúsculas.
    A_count = sequence.count("A")
    T_count = sequence.count("T")
    G_count = sequence.count("G")  # contar la cantidad de G
    C_count = sequence.count("C")
    total = len(sequence)
    GC_content = G_count + C_count
    GC_content = GC_content / len(sequence)
    GC_content = round(100 * GC_content, 2)
    return total, GC_content


"""La siguiente función traduce el DNA a RNA """


def RNA(sequence):
    rna_seq = sequence.replace("T", "U")
    return f"Secuencia de RNA: \n {formato(rna_seq)}"


pass

""" La siguiente función extrae el nombre de la proteína de una línea ya que busca el texto entre '[protein=' y ']'."""


def protein_name(line):
    match = re.search("\[protein=(.+?)\]", line)  #.+? asegura que se capture solo el nombre de la primera proteína dentro del patrón [protein=...]
    return f"Proteína:  {match.group(1)}"


"""La sigueinte función abre un archivo, lo procesa aplicando las funciones anteriormente determinadas y
 lo que genera lo guarda en un archivo de texto"""


def procesar(sequence):
    with open(sequence) as file:
        almacenar = {}
        n_proteina = ""
        sequencia = ""

        for line in file:
            if line.startswith(">"):
                if n_proteina:
                    almacenar[n_proteina] = sequencia
                n_proteina = protein_name(line)
                sequencia = ""
            else:
                sequencia += line.strip()

        if n_proteina:
            almacenar[n_proteina] = sequencia

    for proteina, sequence in almacenar.items():
        total, GC_content = contenido(sequence)
        print(proteina)
        print(f"Número de nucleotidos {total}")
        print(f"Contenido GC:{GC_content}")
        print(RNA(sequence))
        print("--" * 60)  # lo pongo con el objetivo de separar visualmente el resultado para cada secuencia

    with open("Resultados.txt", "w") as out_file:      # me abre un archivo externo con el nombre de Resultados.txt, para guardar los resultados 
        for proteina, sequence in almacenar.items():
            total, GC_content = contenido(sequence)
            rna = RNA(sequence)

            out_file.write(f"{proteina}\n")
            out_file.write(f"Número de nucleótidos: {total}\n")
            out_file.write(f"Contenido GC: {GC_content}\n")
            out_file.write(rna)
            out_file.write("--" * 60 + "\n""\nnn")
    print("Resultados guardados en 'Resultados.txt'")


print(procesar("sequence (Staphylococcus aureus subsp. aureus).txt"))  # ingreso el archivo que quiero que procese.
# puedes hacerlo con el mismo archivo o dercargar otro con las especificaciones dadas en el apartado para el archivo en README.

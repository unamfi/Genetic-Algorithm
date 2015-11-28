# Hernández Alarcón Jesús Alfredo
# Vargas Mariñelarena José Brandon

import random
import string

inp = input("Escribe una palabra :> ")  # Objetivo a alcanzar
inp = inp.lower()
modelo = []
evolution = 100
file_population = open("population.txt",'w') 
file_fitness = open("fitness.txt",'w')

for e in inp:
    modelo.append(e)

largo = len(modelo)  # La longitud del material genetico de cada individuo
num = 100  # La cantidad de individuos que habra en la poblacion
pressure = 3  # Cuantos individuos se seleccionan para reproduccion.
mutation_chance = 0.2  # La probabilidad de que un individuo mute

print("\n\nModelo: %s\n" % (modelo))  # Mostrar el modelo, con un poco de espaciado


def individual():
    """
        Crea un individual
    """
    return [random.choice(string.ascii_lowercase) for i in range(largo)]


def crear_poblacion():
    """
        Crea una poblacion nueva de individuos
    """
    return [individual() for i in range(num)]


def calcular_fitness(individual):
    """
        Calcula el fitness de un individuo concreto.
    """
    fitness = 0
    for i in range(len(individual)):
        if individual[i] == modelo[i]:
            fitness += 1

    return fitness


def write_fitness(lista):
    for element in lista:
        file_fitness.write(str(element[0]))
        file_fitness.write(" - ")
        file_fitness.write(str(element[1]))
        file_fitness.write("\n")

def selection_and_reproduction(population):
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).

        Por ultimo muta a los individuos.

    """
    puntuados = [(calcular_fitness(i), i) for i in
                 population]  # Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , ['a','b','c','d',...])

    # print("Puntuados",puntuados)
    write_fitness(puntuados)

    puntuados = [i[1] for i in sorted(puntuados, key=lambda tup: tup[0])]  # Ordena los pares ordenados y se queda solo con el array de valores
    population = puntuados

    selected = puntuados[(len(
        puntuados) - pressure):]  # Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
    # Se mezcla el material genetico para crear nuevos individuos
    for i in range(len(population) - pressure):
        punto = random.randint(1, largo - 1)  # Se elige un punto para hacer el intercambio
        padre = random.sample(selected, 2)  # Se eligen dos padres

        population[i][:punto] = padre[0][:punto]  # Se mezcla el material genetico de los padres en cada nuevo individuo
        population[i][punto:] = padre[1][punto:]

    return population  # El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven


def mutation(population):
    """
        Se mutan los individuos al azar. Sin la mutacion de nuevos genes nunca podria
        alcanzarse la solucion.
    """
    for i in range(len(population) - pressure):
        if random.random() <= mutation_chance:  # Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar
            punto = random.randint(1, largo - 1)  # Se elgie un punto al azar
            nuevo_valor = random.choice(string.ascii_lowercase)  # y un nuevo valor para este punto

            # Es importante mirar que el nuevo valor no sea igual al viejo
            while nuevo_valor == population[i][punto]:
                nuevo_valor = random.choice(string.ascii_lowercase)

            # Se aplica la mutacion
            population[i][punto] = nuevo_valor

    return population

def show_population(p):
    for element in p:
        print(element)

def write_population(p):
    for element in p:
        file_population.write(str(element)+"\n")

population = crear_poblacion()  # Inicializar una poblacion
#print("Poblacion Inicial:\n%s" % (population))  # Se muestra la poblacion inicial
print("Población Inicial:")
show_population(population)

# Se evoluciona la poblacion
for i in range(evolution):
    if(i==0) or (i==1) or (i==evolution-2) or (i==evolution-1):
        #print("Generacion ",i)
        file_population.write("Generacion "+str(i)+"\n")
        #show_population(population)
        write_population(population)
        #print("--------------------------------\n")
        file_population.write("--------------------------------\n")
    population = selection_and_reproduction(population)
    population = mutation(population)

#print("\nPoblacion Final:\n%s" % (population))  # Se muestra la poblacion evolucionada
print("Población Final: ")
show_population(population)

file_population.close()
print("\n\n")

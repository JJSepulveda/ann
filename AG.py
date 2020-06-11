####################################
## Algoritmo genetico
####################################
import numpy as np


class AG(object):
	def __init__(self,population):
		#el numer ode poblacion tiene que ser par
		self.population = np.uint32(population)
		#self.participants = np.uint32(self.population * 0.05)
		self.participants = 5
		self.winners = []
		self.actual_generation = 0
	def crossover(self, dad, mother):
		variable_type = 64 #float 64
		parent1 = dad.reshape(-1)
		parent2 = mother.reshape(-1)

		#lo multiplicamos por el tipo de variable ya que la cruza se 
		#hara a nivel de bits.
		leng = (len(parent1) * variable_type) - 1
		screw_point = np.random.randint(leng)
		#lo dividimos entre el numer ode bits del tipo de variable
		#y nos da la posición en el arreglo
		index_of_screw = screw_point/variable_type
		#no se me ocurrio otra cosas mas queagregar este if para 
		#que cuando la division diera 0 no se use el operador modulo
		#porque no funciona porque es una division entre 0
		if(index_of_screw<1):
			bit_index = index_of_screw * variable_type
			pass
		else:
			bit_index = (index_of_screw % np.floor(index_of_screw)) * variable_type
		#Convertimos la variable bit_index ahora porque en unas cuantas lineas mas se usara
		#este indice como corrimiento para una mascara y el operador de corrimiento
		#no acepta variables del tipo float para realziar su funcion.
		bit_index = np.uint8(bit_index)
		index_of_screw = np.floor(index_of_screw)
		index_of_screw = np.uint64(index_of_screw)

		#partimos el elemento
		mask = np.uint64(0)
		mask = ~mask << bit_index
		#lo multiplicamos por mil debido a que lo estamos transformando
		#a un tipo de datos que no maneja decimales y si no se multiplica
		#se pierden los decimals. Posteriormente lo reconvertimos y se divide
		#entre 1000.
		sign_parent1 = False
		if(parent1[index_of_screw] < 0):
			parent1[index_of_screw] *= -1
			sign_parent1 = True
		target_value = np.uint64(parent1[index_of_screw] * 1000)
		first_cut_parent1 = (target_value & mask) 
		second_cut_parent1 = (target_value & ~mask)

		#guardamos el signo porque las operaciones bitwise solo son compatibles
		#con variables sin signo.
		sign_parent2 = False
		if(parent2[index_of_screw] < 0):
			parent2[index_of_screw] *= -1
			sign_parent2 = True
		target_value = np.uint64(parent2[index_of_screw] * 1000)
		first_cut_parent2 = (target_value & mask)
		second_cut_parent2 = (target_value & ~mask)

		child_single_value1 = np.float64( (second_cut_parent1 | first_cut_parent2) /1000)
		child_single_value2 = np.float64( (first_cut_parent1 | second_cut_parent2) /1000)

		#recuperamos el signo.
		#estoy pensando en poner que el signo se recupera aleatoriamente.
		if(sign_parent1):
			child_single_value1 *= -1

		if(sign_parent2):
			child_single_value2 *= -1

		parent2[index_of_screw] = child_single_value1
		child1 = parent1[0:index_of_screw]
		child1 = np.append(child1, parent2[index_of_screw:])

		parent1[index_of_screw] = child_single_value2
		child2 = parent2[0:index_of_screw]
		child2 = np.append(child2, parent1[index_of_screw:])

		return np.array([child1.reshape(dad.shape), child2.reshape(dad.shape)])
	def tournament (self):
		#arreglo de un numero entero entre 0 y el tamaño total de los participantes,
		#del tamaño de la cantidad de participantes.

		winners = []

		#para que este algoritmo funciones se el buffer tiene que estar ordenado de mayor a menor
		#con respecto al fitness
		for _ in range(self.population):
			participants_id = np.random.randint(0, self.population - 1, (self.participants))
			winners.append(np.min(participants_id))

		winners = winners
		self.winners = winners
	def first_generation(self):
		return np.random.randn(self.population,4,2)
	def new_generation(self,buff):

		self.tournament()
		childs = []
		#para que range funciones tiene que ser un entero
		amount = self.population//2

		for _ in range(amount):
			dad = buff[self.winners[0]]
			mother = buff[self.winners[1]]
			c1, c2 = self.crossover(dad,mother)
			childs.append(c1)
			childs.append(c2)
			self.winners.pop(0)
			self.winners.pop(0)

		self.actual_generation += 1
		print("childs shape: {}".format((np.asarray(childs)).shape))
		print("Generación acual: {}".format(self.actual_generation))

		return childs

if(__name__ == '__main__'):
	ag = AG(50)
	#dad = np.array([[-1.0,1.0,1.0,1.0],[-2.0,2.0,2.0,2.0]])
	#mot = np.array([[-3.0,3.0,3.0,3.0],[-4.0,4.0,4.0,4.0]])
	#dad, mot = ag.crossover(dad,mot)
	#print(dad)
	#print(mot)
	fg = ag.first_generation()
	ag.new_generation(fg)
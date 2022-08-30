import board
import random


def distance_between(startpoint, endpoint):
	sx = startpoint % board.BOARDCOLS
	sy = startpoint // board.BOARDCOLS
	ex = endpoint % board.BOARDCOLS
	ey = endpoint // board.BOARDCOLS
	return (abs((ex - sx)) + abs((ey - sy)))


def find_bomb(fields, start_position):
	bombfield = -1
	mindist = board.BOARDCOLS ** 2
	for i in range(len(fields)):
		if fields[i].type == 'B':
			if fields[i].object.defused == False:
				dist = distance_between(start_position, i)
				if dist < mindist:
					bombfield = i
					mindist = dist

	return bombfield

class Chromosome:
	def __init__(self, fo, wl):
		self.fields_order = fo
		self.way_lenght = wl

class Genetic:
	def __init__(self, fields, ap):
		self.bombfields = self.get_bombs(fields)
		self.agent_position = ap
		self.local_minimum_path = self.find_local_minimum_path()
		self.make_parents()
		self.parents = self.make_parents()
		self.children = self.make_children(self.parents)
		self.genetic_path = self.parents[0]
		for i in range(10000):
			self.genetic_path = self.find_genetic_path()
		print("Genetic path way:  ", self.genetic_path.fields_order)
		print("Genetic path way lenght:  ", self.genetic_path.way_lenght)
		print("Local minimum path:  ", self.local_minimum_path.fields_order)
		print("Local minimum path way lenght:  ", self.local_minimum_path.way_lenght)
		if self.local_minimum_path.way_lenght >= self.genetic_path.way_lenght:
			print("Wygrywa genetic path !!!")
		else:
			print("Local minimum path teoretycznie byłby lepszy :/")

	def get_bombs(self,fields):
		bombfields = []
		for i in range(len(fields)):
			if fields[i].type == 'B':
				bombfields.append(i)
		#print(bombfields)
		return bombfields


	def make_parents(self):
		parent_chromosomes = []
		for i in range(len(self.bombfields)*10):
			bombfieldscopy = self.bombfields.copy()
			single_chromosome = []
			weight_of_chromosome = 0
			for j in range(len(self.bombfields)):
				random_choice = random.randint(0,(len(bombfieldscopy)-1))
				single_chromosome.append(bombfieldscopy[random_choice])
				bombfieldscopy.remove(bombfieldscopy[random_choice])
				if j == 0:
					weight_of_chromosome = weight_of_chromosome + distance_between(self.agent_position,single_chromosome[j])
				else:
					weight_of_chromosome = weight_of_chromosome + distance_between(single_chromosome[j-1],single_chromosome[j])
			parent_chromosomes.append(Chromosome(single_chromosome,weight_of_chromosome))
			#print("parent chromosome ", i, ":")
			#print(parent_chromosomes[i].fields_order)
			#print(parent_chromosomes[i].way_lenght)
		return parent_chromosomes

	def make_children(self,parents):
		children_chromosomes = []
		parentscopy = parents.copy()
		for i in range(len(self.bombfields)*10):
			parentscopy = parents.copy()
			rch = random.randint(0,(len(self.bombfields)*10)-1)
			parent1 = parentscopy[rch].fields_order.copy()
			#print("parent 1 order: ", parent1)
			parentscopy.remove(parentscopy[rch])
			rch2 = random.randint(0,(len(self.bombfields)*10)-2)
			parent2 = parentscopy[rch2].fields_order.copy()
			#print("parent 2 order: ",parent2)
			parentscopy.remove(parentscopy[rch2])
			how_many_elements = random.randint(1,len(self.bombfields)-1)
			elements_to_switch = []
			single_chromosome = []
			weight_of_chromosome = 0
			for j in range(how_many_elements):
				random_choice = random.randint(0,(len(parent1)-1))
				elements_to_switch.append(parent1[random_choice])
				#print("element to switch: ", elements_to_switch[j])
				parent1.remove(elements_to_switch[j])
				#print("parent 2 order: ", parent2.fields_order)
				parent2.remove(elements_to_switch[j])
				parent2.append(elements_to_switch[j])
			single_chromosome = parent2.copy()
			for j in range(len(single_chromosome)):
				if j == 0:
					weight_of_chromosome = weight_of_chromosome + distance_between(self.agent_position,single_chromosome[j])
				else:
					weight_of_chromosome = weight_of_chromosome + distance_between(single_chromosome[j - 1],single_chromosome[j])
			children_chromosomes.append(Chromosome(single_chromosome,weight_of_chromosome))
			#print("children chromosome ", i, ":")
			#print(children_chromosomes[i].fields_order)
			#print(children_chromosomes[i].way_lenght)
		return children_chromosomes


	def find_genetic_path(self):
		chromosomes = []
		new_parents = []
		for i in range(len(self.parents)):
			chromosomes.append(self.parents[i])
		for i in range(len(self.children)):
			chromosomes.append(self.children[i])
		chromosomes.sort(key=lambda x: x.way_lenght)
		for j in range(len(self.bombfields)**2):
			new_parents.append(chromosomes[j])
		self.parents = new_parents
		self.children = self.make_children(self.parents)
		return chromosomes[0]

	def find_local_minimum_path(self):
		path = []
		bombfiledscopy = self.bombfields.copy()
		path_lenght = 0
		bombfield = -1
		mindist = board.BOARDCOLS ** 2
		for field in bombfiledscopy:
			dist = distance_between(self.agent_position,field)
			if dist < mindist:
				bombfield = field
				mindist = dist
		path_lenght = path_lenght + mindist
		path.append(bombfield)
		bombfiledscopy.remove(bombfield)

		while len(bombfiledscopy) > 0:
			mindist = board.BOARDCOLS ** 2
			for field in bombfiledscopy:
				dist = distance_between(bombfield, field)
				if dist < mindist:
					bombfield = field
					mindist = dist
			path_lenght = path_lenght + mindist
			path.append(bombfield)
			bombfiledscopy.remove(bombfield)

		return Chromosome(path,path_lenght)











class Node:
	def __init__(self,fieldN,parent,destination,obstacle_deley_value):
		self.field_number = fieldN
		self.parent_field = parent
		self.distance_to_destination = distance_between(fieldN,destination)
		if parent is None:
			self.distance_to_agent = 0
			self.obstacle_deley = obstacle_deley_value
		else:
			self.distance_to_agent = parent.distance_to_agent + 1
			self.obstacle_deley = obstacle_deley_value + parent.obstacle_deley
		self.path_cost = self.distance_to_destination + self.distance_to_agent + self.obstacle_deley

class Pathfind:
	def __init__(self, fields, bombfield, agent_position):
		self.open_nodes = []
		self.closed_nodes = []

		self.fields = fields
		self.bombfield = bombfield
		self.agent_position = agent_position
		self.way = self.pathway()

	def lowest_cost_node(self):
		lowestcost = self.open_nodes[0].path_cost
		bestnode = self.open_nodes[0]
		#print("szukam lowest cost!")
		#print("lowest cost: ", lowestcost)
		#print("przeszukuje nodes")
		for node in self.open_nodes:
			#print(node.path_cost)
			if (node.path_cost < lowestcost) or (node.path_cost == lowestcost and node.distance_to_destination < bestnode.distance_to_destination):
				lowestcost = node.path_cost
				bestnode = node
				#print("zmienilem node")

		#print("skonczylem wyszukiwac, lowest cost = ", bestnode.path_cost)
		return bestnode

	def neighbours(self, node):
		actuallpos = node.field_number
		neighboursTab = []

		if not actuallpos - board.BOARDCOLS < 0:
			neighboursTab.append(actuallpos - board.BOARDCOLS)

		if not actuallpos + board.BOARDCOLS >= (board.BOARDCOLS ** 2):
			neighboursTab.append(actuallpos + board.BOARDCOLS)

		if not (actuallpos - 1 < 0 or actuallpos%board.BOARDCOLS == 0 ):
			neighboursTab.append(actuallpos - 1)

		if not (actuallpos + 1 >= (board.BOARDCOLS ** 2) or actuallpos%board.BOARDCOLS == (board.BOARDCOLS-1) ):
			neighboursTab.append(actuallpos + 1)

		return neighboursTab


	def node_in_closed(self, fn):
		for node in self.closed_nodes:
			if node.field_number == fn:
				return True
		return False

	def node_in_open(self,fn):
		for node in self.open_nodes:
			if node.field_number == fn:
				return node
		return None



	def findway(self):
		startnode = Node(self.agent_position, None, self.bombfield, 0)
		self.open_nodes.append(startnode)

		while True:
			current = self.lowest_cost_node()
			#print("szukam drogi  , current field:", current.field_number)
			self.open_nodes.remove(current)
			self.closed_nodes.append(current)

			if current.field_number == self.bombfield:
				#print("znalazlem droge !!!!!!!!!!!!")
				return current

			neighbours = self.neighbours(current)
			#print("neighbours: ", end=" ")
			#for x in neighbours:
				#print(x, end=" ")
			#print("")
			for neighbour in neighbours:
				if self.node_in_closed(neighbour) == False:

					if self.node_in_open(neighbour) is None:
						node = Node(neighbour, current, self.bombfield, self.fields[neighbour].deley_value)
						self.open_nodes.append(node)
						#print(neighbour, ": ", node.path_cost)
					else:
						newcost = distance_between(neighbour, self.bombfield) + current.obstacle_deley + self.fields[neighbour].deley_value + current.distance_to_agent + 1
						if newcost < self.node_in_open(neighbour).path_cost:
							self.node_in_open(neighbour).pathcost = newcost
							self.node_in_open(neighbour).parent_field = current
							#print(neighbour, ": ", node.path_cost)







	def pathway(self):
		way = []
		current = self.findway()
		while current.field_number != self.agent_position:
			way.append(current.field_number)
			current = current.parent_field

		way.reverse()
		#print("path is: ", end =" ")
		#for x in way:
			#print(x, end = " ")
		#print("")

		return way





















#Name: Juan Diego Gonzalez German
#ID: 1001401837
#Date: 02/04/2019

import sys

#if the user does not provide enough parameters, print error message and terminate
if (len(sys.argv) < 4):
	print("Please run script as \n  python find_route.py input_filename origin_city destination_city\n  OR")
	print("  python find_route.py input_filename origin_city destination_city heuristic_filename")
	sys.exit(1)

#move the parameters to appropiate variables
mapfile = sys.argv[1]
origin = sys.argv[2]
goal = sys.argv[3]
hfile = ""
informed = False

#get the heuristics file, if there is one
if(len(sys.argv) == 5):
	hfile = sys.argv[4]

#initialize an empty dictionary for routes, and open the routes file
map = {}
explored = {}
file = open(mapfile, "r")

#parse the routes into a dictionary
for line in file:
	if (line == "END OF INPUT\n" or line == "END OF INPUT"):
		break
	route = line.split(" ")

	for i in range(2):

		if i == 0:
			j = 1
		else:
			j = 0

		if route[i] not in map:
			map[route[i]] = []
			explored[route[i]] = False

		paths = map[route[i]]
		paths.append(tuple((route[j], int(route[2]))))

file.close()

#initialize an empty dictionary for the heuristics, and fill it if there is a heuristic file to parse
heuristic = {}
if(hfile != ""):
	informed = True
	file = open(hfile, "r")

	for line in file:

		if (line == "END OF INPUT\n" or line == "END OF INPUT"):
			break

		approx = line.split(" ")
		heuristic[approx[0]] = int(approx[1])

	file.close()

#define class for path nodes
#current city, previous node, last cost, and total running cost are object properties
class City:
	def __init__ (self, name, previous, cost, total):
		self.name = name
		self.previous = previous
		self.cost = cost
		self.total = total

#function to find cost of expansion
#informed search takes heuristic into account		
def get_total(city):
	if not informed:
		return city.total
	else:
		return city.total + heuristic[city.name]
	
#check that origin and destination are in provided map
if (origin not in map or goal not in map):
	print("Cities not found on file, aborting...")
	sys.exit(1)

#create start node and added to frontier (fringe)
node = City(origin, None, 0, 0)
frontier = [node]
count = 0

while(True):
	#if we cannot expand more, we return a failure
	if not frontier :
		print("nodes expanded = %d" % count)
		print("distance = infinity")
		print("route:\nnone")
		sys.exit(1)

	#upon expanding a node, we increment counter and make its explored value True
	#if it has already been explored, we just ignore it
	city = frontier.pop()
	count += 1
	if(explored[city.name]):
		continue
	explored[city.name] = True

	#if we have reached destination, we print information and exit
	if(city.name == goal):
		print("nodes expanded = %d" % count)
		print("distance = %d" % city.total)
		print("route:")
		
		history = []
		
		#backtrack to get all the path information
		while(city.previous is not None):
			history.insert(0, "%s to %s, %d km" % (city.previous.name, city.name, city.cost))
			city = city.previous
			
		print('\n'.join(history))
			
		sys.exit(0)
	
	for x in map[city.name]:
		#create new nodes to expand from current node's successors. Add to the fringe
		destination = City(x[0], city, x[1], x[1] + city.total)
		frontier.append(destination)

	#sort expansion queue wrt to cost, or cost + heuristic if informed					
	frontier.sort(reverse = True, key = get_total)	

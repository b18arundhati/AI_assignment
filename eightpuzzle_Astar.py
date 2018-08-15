#implementation of A* for eight puzzle game
#heuristics used:
#h1(n) = 0
#h2(n) = number of misplaced tiles 
#h3(n) = sum of manhattan distances of misplaced tiles from their goal position
#h4(n) = ???

from random import shuffle
import copy
import operator
import time
import math

goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']]

def play():
	startPuzzle = inputPuzzle()
	#startPuzzle = [[' ','2','3'], ['5','6','1'], ['7','4','8']]
	#startPuzzle = [[' ','5','3'], ['2','6','1'], ['8','7','4']]
	printPuzzle(startPuzzle)
	if not isSolvable(startPuzzle):
		print "Not solvable"
		return
	#startPuzzle = [['5',' ','8'],['4','2','1'],['7','3','6']]
	#startPuzzle = [[' ','1','3'], ['4','2','5'], ['7','8','6']]
	
	#heuristic = chooseHeuristic()
	solvePuzzle(startPuzzle)

def isSolvable(puzzle):
	inversion = 0
	l = []
	for row in puzzle:
		for cell in row:
			if cell != ' ':
				l.append(int(cell))

	for i in xrange(len(l)):
		count = l[i] - 1
		if count > 0:
			for j in xrange(i):
				if l[j] < l[i]:
					count -= 1
			inversion += count


	if inversion%2 == 0:
		return True
	else:
		return False


def printPuzzle(puzzle):
	print '\n'
	for i in puzzle:
		for j in i:
			if j == ' ':
				print 'X','\t',
			else:
				print j,'\t',
		print '\n'
	print '\n'

#take a random puzzle input
def inputPuzzle():
	l = ['1', '2', '3', '4', '5', '6', '7', '8', ' ']
	shuffle(l)
	puzzle = [[],[],[]]
	for i in enumerate(l):
		puzzle[i[0]/3].append(i[1])
	return puzzle

def misplacedTiles(puzzle):
	misplaced = 0
	#puzzle is a list of lists
	for i in range(len(puzzle)):
		for j in range(len(puzzle[i])):
			if puzzle[i][j] != ' ':
				if puzzle[i][j] != goal[i][j]:
					misplaced += 1

	return misplaced

def manhattan(puzzle):
	manhattan = 0
	#puzzle is a list of lists

	for i in range(len(puzzle)):
		for j in range(len(puzzle[i])):
			if puzzle[i][j] != ' ':
				if puzzle[i][j] != goal[i][j]:
					found = 0
					for m in range(len(goal)):
						for n in range(len(goal[m])):
							if puzzle[i][j] ==  goal[m][n]:
								manhattan += abs(m - i) + abs(n - j)
								found = 1
								break
						if found:
							break
	return manhattan

def euclidean(puzzle):
	dist = 0

	for i in range(len(puzzle)):
		for j in range(len(puzzle[i])):
			if puzzle[i][j] != ' ':
				if puzzle[i][j] != goal[i][j]:
					found = 0
					for m in range(len(goal)):
						for n in range(len(goal[m])):
							if puzzle[i][j] ==  goal[m][n]:
								dist += math.sqrt((m - i)**2 + (n - j)**2)
								found = 1
								break
						if found:
							break
	return dist


def expand(puzzle):#, heuristic, priorityQueue):
	#expand moving the empty tile to all possible positions
	#order of expansion to neighboring positions - Left, Top, Right, Bottom
	expanded = []

	leftShift = copy.deepcopy(puzzle)

	for x in leftShift:
		if x.count(' ') == 1:
			if x.index(' ') != 0:
				index = x.index(' ')
				x[index], x[index-1] = x[index-1], x[index]
				expanded.append(leftShift)
				break

	topShift = copy.deepcopy(puzzle)

	for x in topShift:
		if x.count(' ') == 1:
			if x != topShift[0]:
				index = x.index(' ')
				if x == topShift[1]:
					topShift[1][index], topShift[0][index] = topShift[0][index], topShift[1][index]
					expanded.append(topShift)
					break
				elif x == topShift[2]:
					topShift[1][index], topShift[2][index] = topShift[2][index], topShift[1][index]
					expanded.append(topShift)
					break
				

	rightShift = copy.deepcopy(puzzle)

	for x in rightShift:
		if x.count(' ') == 1:
			if x.index(' ') != 2:
				index = x.index(' ')
				x[index+1], x[index] = x[index], x[index+1]
				expanded.append(rightShift)
				break

	bottomShift = copy.deepcopy(puzzle)

	for x in bottomShift:
		if x.count(' ') == 1:
			if x != bottomShift[2]:
				index = x.index(' ')
				if x == bottomShift[0]:
					bottomShift[0][index], bottomShift[1][index] = bottomShift[1][index], bottomShift[0][index]
					expanded.append(bottomShift)
					break
				elif x == bottomShift[1]:
					bottomShift[1][index], bottomShift[2][index] = bottomShift[2][index], bottomShift[1][index]
					expanded.append(bottomShift)
					break

	return expanded

def solve_h1(puzzle):
	print "using heuristic h(n) = 0 with A* algorithm: "

	start_time = time.time()

	start = copy.deepcopy(puzzle)
	expandedQueue = []
	priorityQueue = []
	expandedCount = 0
	depth = 0

	while start != goal:

		expandedQueue.append(start)
		expandedCount += 1
		#print 'expanding ',
		#printPuzzle(start)
		if expandedCount > 362880:
			print 'failed'
			break
		expanded = expand(start)

		for i in expanded:
			if i in expandedQueue:
				continue
			#elif not isSolvable(i):
			#	continue
			else:
				priorityQueue.append((i,depth+1))
		
		depth += 1

		node = priorityQueue.pop(0)
		start = node[0]

	if start == goal:
		exec_time = time.time() - start_time
		print 'goal reached in time %s seconds'%exec_time,
		print expandedCount, ' nodes expanded'
		#printPuzzle(start)
		

	#print "Solved using h(n) = 0."
	#print "XXXX"

def solve_h2(puzzle):
	print "using heuristic h(n) = number of misplaced tiles in nth iteration "

	start_time = time.time()

	start = copy.deepcopy(puzzle)

	priorityQueue = [] #to be used during expansion
	depth = 0
	expandedQueue = []
	expandedCount = 0

	while start != goal:
		
		#print "expanding at depth ",depth,
		#printPuzzle(start)
		expandedQueue.append(start)
		expandedCount += 1

		if expandedCount > 362880:
			print 'failed'
			break

		expanded = expand(start)
		#print expandedCount, " nodes expanded"
		
		#print expanded

		#print 'input 1'
		# while input() != 1:
		# 	sleep(5)
		# temp = node()
		# temp.setPuzzle(start)
		# depth = temp.getDepth()
		for n in expanded:
			# node = node()
			# node.setPuzzle(n)
			# node.setDepth(depth+1)
			# node.setHeuristic(misplacedTiles(n))
			if n in expandedQueue:
				continue
			#elif not isSolvable(n):
			#	continue
			else:	
				priorityQueue.append((n,depth+1+misplacedTiles(n), depth+1))
				
		#sort the priority queue
		# for i in range(len(priorityQueue)-1, 0, -1):
		# 	for j in xrange(i):
		# 		if priorityQueue[j][1] + priorityQueue[j][2] > priorityQueue[j+1][1] + priorityQueue[j+1][2]:
		# 			priorityQueue[j], priorityQueue[j+1] = priorityQueue[j+1], priorityQueue[j]		
		priorityQueue.sort(key=operator.itemgetter(1))
		#print priorityQueue

		# while input() != 1:
		# 	sleep(5)

		node = priorityQueue.pop(0)
		start = node[0]
		depth = node[2]
		# if len(priorityQueue) == 0:
		# 	if start == goal:
		# 		print 'solved.'
		# 	else:
		# 		print "search exhausted. exiting..."
		# 	#sys.exit(0)

	if start == goal:
		exec_time = time.time() - start_time
		print 'popped goal state in %s seconds'%exec_time,
		print expandedCount,' nodes expanded'
		#printPuzzle(start)

	#print "solved using h(n) = number of misplaced tiles in nth iteration"


def solve_h3(puzzle):
	print "using heuristic h(n) = manhattan distance of tiles from their position in goal state "

	start_time = time.time()

	start = copy.deepcopy(puzzle)
	expandedQueue = []
	priorityQueue = []
	expandedCount = 0
	depth = 0

	while start != goal:

		expandedQueue.append(start)
		expandedCount += 1
		# print 'expanding ',
		# printPuzzle(start)
		if expandedCount > 362880:
			print 'failed'
			break
		expanded = expand(start)

		for n in expanded:
			if n in expandedQueue:
				continue
			#elif not isSolvable(n):
			#	continue
			else:
				priorityQueue.append((n,depth+1+manhattan(n), depth+1))

		# for i in range(len(priorityQueue)-1,0,-1):
		# 	for j in xrange(i):
		# 		if priorityQueue[j][1] + priorityQueue[j][2] > priorityQueue[j+1][1] + priorityQueue[j+1][2]:
		# 			priorityQueue[j], priorityQueue[j+1] = priorityQueue[j+1], priorityQueue[j]
		priorityQueue.sort(key=operator.itemgetter(1))
		node = priorityQueue.pop(0)
		start = node[0]
		depth = node[2]

	if start == goal:
		exec_time = time.time() - start_time
		print 'popped goal state in %s seconds'%exec_time,
		print expandedCount,' nodes expanded using heuristic manhattan distance'
		#printPuzzle(start)

	#print "computation over. goal reached"


def solve_h4(puzzle):
	print "using heuristic h(n) = euclidean distance of tiles from their position in goal state "

	start_time = time.time()

	start = copy.deepcopy(puzzle)
	expandedQueue = []
	priorityQueue = []
	expandedCount = 0
	depth = 0

	while start != goal:

		expandedQueue.append(start)
		expandedCount += 1
		# print 'expanding ',
		# printPuzzle(start)
		if expandedCount > 362880:
			print 'failed'
			break
		expanded = expand(start)

		for n in expanded:
			if n in expandedQueue:
				continue
			#elif not isSolvable(n):
			#	continue
			else:
				priorityQueue.append((n,depth+1+euclidean(n), depth+1))

		# for i in range(len(priorityQueue)-1,0,-1):
		# 	for j in xrange(i):
		# 		if priorityQueue[j][1] + priorityQueue[j][2] > priorityQueue[j+1][1] + priorityQueue[j+1][2]:
		# 			priorityQueue[j], priorityQueue[j+1] = priorityQueue[j+1], priorityQueue[j]
		priorityQueue.sort(key=operator.itemgetter(1))
		node = priorityQueue.pop(0)
		start = node[0]
		depth = node[2]

	if start == goal:
		exec_time = time.time() - start_time
		print 'popped goal state in %s seconds'%exec_time,
		print expandedCount,' nodes expanded using heuristic euclidean distance'
		#printPuzzle(start)

	#print "computation over. goal reached"


def solvePuzzle(puzzle):
	#use the 4 heuristics one by one and show result

	#1. using heuristic h1
	#solve_h1(puzzle)

	#2. using heuristic h2
	solve_h2(puzzle)

	#3. using heuristic h3
	solve_h3(puzzle)

	#4. using heuristic h4
	solve_h4(puzzle)


if __name__ == "__main__":
	# for i in range(1,5):
	# 	print 'Puzzle ',i
	play()

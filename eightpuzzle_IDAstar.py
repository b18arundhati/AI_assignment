#implementation of IDA* for eight puzzle game
#heuristics used:
#h1(n) = 0
#h2(n) = number of misplaced tiles 
#h3(n) = sum of manhattan distances of misplaced tiles from their goal position
#h4(n) = ???

from random import shuffle
import copy
import operator, math, time

goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']]

expandList = []
expandedCount = 0

def play():
	startPuzzle = inputPuzzle()
	#startPuzzle = [['5',' ','8'],['4','2','1'],['7','3','6']]
	#startPuzzle = [['7','6','2'], ['3','4','8'], ['1','5',' ']]
	printPuzzle(startPuzzle)
	if not isSolvable(startPuzzle):
		print "Not solvable"
		return
	#heuristic = chooseHeuristic()
	solvePuzzle(startPuzzle)

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


#take a random puzzle input
def inputPuzzle():
	l = ['1', '2', '3', '4', '5', '6', '7', '8', ' ']
	shuffle(l)
	puzzle = [[],[],[]]
	for i in enumerate(l):
		puzzle[i[0]/3].append(i[1])
	return puzzle

def h0(puzzle):
	return 0

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


class node:

	def __init__(self):
		self.depth = 0
		self.heuristic = 0

	def setPuzzle(self,puzzle):
		self.puzzle = puzzle

	def setDepth(self,depth):
		self.depth = depth

	def setHeuristic(self,value):
		self.heuristic = value

	def getFn(self):
		cost = self.depth + self.heuristic
		return cost

def expandIDAstar(mynode, f_limit, myheuristic):
	#order - left, top, right, bottom
	global expandList
	global expandedCount

	#expandList = []
	new_f = None

	if myheuristic == "zero":
		heuristic = h0
	elif myheuristic == "misplacedTiles":
		heuristic = misplacedTiles
	elif myheuristic == "manhattan":
		heuristic = manhattan
	elif myheuristic == "euclidean":
		heuristic = euclidean

	puzzle = mynode.puzzle

	leftShift = copy.deepcopy(puzzle)
	for x in leftShift:
		if x.count(' ') == 1:
			if x.index(' ') != 0:
				index = x.index(' ')
				x[index-1], x[index] = x[index], x[index-1]

				if leftShift in expandList:
					break

				#if not isSolvable(leftShift):
				#	break

				# print 'expanded ',
				# printPuzzle(leftShift)

				cost = mynode.depth + 1 + heuristic(leftShift)
				if cost <= f_limit:
					expandList.append(leftShift)
					expandedCount += 1

					if leftShift == goal:
						return leftShift, -1

					temp = node()
					temp.setPuzzle(leftShift)
					temp.setDepth(mynode.depth + 1)
					temp.setHeuristic(heuristic(leftShift))
					l, f = expandIDAstar(temp, f_limit, myheuristic)
					#expandList.extend(l)
					if l is None:
						if new_f is None:
							new_f = f
						else:
							new_f = min(new_f, f)
					else:
						return l,f
				else:
					if new_f is None:
						new_f = cost
					else:
						new_f = min(new_f, cost)
				break 

	topShift = copy.deepcopy(puzzle)
	for x in topShift:
		if x.count(' ') == 1:
			if x != puzzle[0]:
				index = x.count(' ')
				if x == topShift[1]:
					topShift[0][index], topShift[1][index] = topShift[1][index], topShift[0][index]

					if topShift in expandList:
						break
					#if not isSolvable(topShift):
					#	break
					# print 'expanded ',
					# printPuzzle(topShift)
					cost = mynode.depth + 1 + heuristic(topShift)
					if cost <= f_limit:
						expandList.append(topShift)
						expandedCount += 1

						if topShift == goal:
							return topShift, -1

						temp = node()
						temp.setPuzzle(topShift)
						temp.setDepth(mynode.depth + 1)
						temp.setHeuristic(heuristic(topShift))

						l, f = expandIDAstar(temp, f_limit, myheuristic)

						if l is None:
							if new_f is None:
								new_f = f
							else:
								new_f = min(new_f, f)
						else:
							return l, f
					else:
						if new_f is None:
							new_f = cost
						else:
							new_f = min(new_f, cost)

					break
				elif x == topShift[2]:
					topShift[1][index], topShift[2][index] = topShift[2][index], topShift[1][index]

					if topShift in expandList:
						break
					#if not isSolvable(topShift):
					#	break
					# print 'expanded ',
					# printPuzzle(topShift)
					cost = mynode.depth + 1 + heuristic(topShift)
					if cost <= f_limit:
						expandList.append(topShift)
						expandedCount += 1
						if topShift == goal:
							return topShift, -1

						temp = node()
						temp.setPuzzle(topShift)
						temp.setDepth(mynode.depth + 1)
						temp.setHeuristic(heuristic(topShift))
						l, f = expandIDAstar(temp, f_limit, myheuristic)
						if l is None:
							if new_f is None:
								new_f = f
							else:
								new_f = min(new_f, f)
						else:
							return l, f
					else:
						if new_f is None:
							new_f = cost
						else:
							new_f = min(new_f, cost)

					break

	rightShift = copy.deepcopy(puzzle)
	for x in rightShift:
		if x.count(' ') == 1:
			if x.index(' ') != 2:
				index = x.index(' ')
				x[index], x[index+1] = x[index+1], x[index]

				if rightShift in expandList:
					break
				#if not isSolvable(rightShift):
				#	break
				# print 'expanded ',
				# printPuzzle(rightShift)
				cost = mynode.depth + 1 + heuristic(rightShift)
				if cost <= f_limit:
					expandList.append(rightShift)
					expandedCount += 1

					if rightShift == goal:
						return rightShift, -1

					temp = node()
					temp.setPuzzle(rightShift)
					temp.setDepth(mynode.depth + 1)
					temp.setHeuristic(heuristic(rightShift))
					l, f = expandIDAstar(temp, f_limit, myheuristic)

					if l is None:
						if new_f is None:
							new_f = f
						else:
							new_f = min(new_f, f)
					else:
						return l, f
				else:
					if new_f is None:
						new_f = cost
					else:
						new_f = min(new_f, cost)
				break

	bottomShift = copy.deepcopy(puzzle)
	for x in bottomShift:
		if x.count(' ') == 1:
			if x != puzzle[2]:
				index = x.index(' ')
				if x == bottomShift[0]:
					bottomShift[0][index], bottomShift[1][index] = bottomShift[1][index], bottomShift[0][index]

					if bottomShift in expandList:
						break
					#if not isSolvable(bottomShift):
					#	break

					# print 'expanded',
					# printPuzzle(bottomShift)
					cost = mynode.depth + 1 + heuristic(bottomShift)
					if cost <= f_limit:
						expandList.append(bottomShift)
						expandedCount += 1

						if bottomShift == goal:
							return bottomShift, -1
						temp = node()
						temp.setPuzzle(bottomShift)
						temp.setDepth(mynode.depth + 1)
						temp.setHeuristic(heuristic(bottomShift))
						l, f = expandIDAstar(temp, f_limit, myheuristic)

						if l is None:
							if new_f is None:
								new_f = f
							else:
								new_f = min(new_f, f)
						else:
							return l, f
					else:
						if new_f is None:
							new_f = cost
						else:
							new_f = min(new_f, cost)
					break

				elif x == bottomShift[1]:
					bottomShift[1][index], bottomShift[2][index] = bottomShift[2][index], bottomShift[1][index]

					if bottomShift in expandList:
						break
					#if not isSolvable(bottomShift):
					#	break

					# print 'expanded',
					# printPuzzle(bottomShift)
					cost = mynode.depth + 1 + heuristic(bottomShift)
					if cost <= f_limit:
						expandList.append(bottomShift)
						expandedCount += 1

						if bottomShift == goal:
							return bottomShift, -1
						temp = node()
						temp.setPuzzle(bottomShift)
						temp.setDepth(mynode.depth + 1)
						temp.setHeuristic(heuristic(bottomShift))
						l, f = expandIDAstar(temp, f_limit, myheuristic)

						if l is None:
							if new_f is None:
								new_f = f
							else:
								new_f = min(new_f, f)
						else:
							return l, f
					else:
						if new_f is None:
							new_f = cost
						else:
							new_f = min(new_f, cost)
					break


	return None, new_f


def solve_h1(puzzle):
	#heuristic h(n) = 0
	print "heuristic zero"

	start_time = time.time()
	start = copy.deepcopy(puzzle)
	f_limit = 1

	tempStart = node()
	tempStart.setPuzzle(puzzle)
	tempStart.setDepth(0)
	tempStart.setHeuristic(h0(puzzle))
	global expandedCount
	global expandList
	expandedCount = 0
	while True:
		expandList = []
		l, f = expandIDAstar(tempStart, f_limit, "zero")
		if l is not None and f == -1:
			print 'goal reached'
			exec_time = time.time() - start_time
			print expandedCount,' nodes expanded'
			print 'execution time %s seconds'%exec_time
			break
		else:
			f_limit = f

def solve_h2(puzzle):
	#heuristic h(n) = number of tiles misplaced in puzzle state at iteration n
	#set a limit cost at each iteration and run dfs till that cost is exceeded
	start_time = time.time()
	start = copy.deepcopy(puzzle)
	f_limit = misplacedTiles(start)

	tempStart = node()
	tempStart.setPuzzle(puzzle)
	tempStart.setDepth(0)
	tempStart.setHeuristic(misplacedTiles(puzzle))
	global expandedCount
	global expandList
	expandedCount = 0
	while True:
		expandList = []
		l, f = expandIDAstar(tempStart, f_limit, "misplacedTiles")
		if l is not None and f == -1:
			print 'goal reached'
			exec_time = time.time() - start_time
			print expandedCount,' nodes expanded'
			print 'execution time %s seconds'%exec_time
			break
		else:
			f_limit = f


def solve_h3(puzzle):
	start_time = time.time()
	start = copy.deepcopy(puzzle)
	f_limit = manhattan(start)

	tempStart = node()
	tempStart.setPuzzle(puzzle)
	tempStart.setDepth(0)
	tempStart.setHeuristic(manhattan(puzzle))
	global expandedCount
	global expandList
	expandedCount = 0
	while True:
		expandList = []
		l, f = expandIDAstar(tempStart, f_limit, "manhattan")
		if l is not None and f == -1:
			print 'goal reached'
			exec_time = time.time() - start_time
			print expandedCount,' nodes expanded'
			print 'execution time %s seconds'%exec_time
			break
		else:
			f_limit = f

def solve_h4(puzzle):
	start_time = time.time()
	start = copy.deepcopy(puzzle)
	f_limit = euclidean(start)

	tempStart = node()
	tempStart.setPuzzle(puzzle)
	tempStart.setDepth(0)
	tempStart.setHeuristic(euclidean(puzzle))
	global expandedCount
	global expandList
	expandedCount = 0
	while True:
		expandList = []
		l, f = expandIDAstar(tempStart, f_limit, "euclidean")
		if l is not None and f == -1:
			print 'goal reached'
			exec_time = time.time() - start_time
			print expandedCount, ' nodes expanded'
			print 'execution time %s seconds'%exec_time
			break
		else:
			f_limit = f

def solvePuzzle(puzzle):
	#use the 4 heuristics one by one and show result

	#1. using heuristic h1
	print 'using heuristic h(n) = 0: '
	#solve_h1(puzzle)

	#2. using heuristic h2
	print 'using heuristic h(n) = number of misplaced tiles in current state: '
	solve_h2(puzzle)

	# #3. using heuristic h3
	print 'using heuristic h(n) = sum of manhattan distances of tiles between current state and goal state: '
	solve_h3(puzzle)

	# #4. using heuristic h4
	print 'using heuristic h(n) = sum of euclidean distances of tiles between current state and goal state: '
	solve_h4(puzzle)


if __name__ == "__main__":
	# for i in range(1,20):
	# 	print 'puzzle ',i
	# 	play()
	play()

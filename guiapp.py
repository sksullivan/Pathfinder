from Tkinter import *

class Grid():
	def __init__(self, gridX, gridY):
		self.positions = []

		self.directions = {"w" : 0, "e" : 1, "d" : 2, "c" : 3, "x" : 4, "z" : 5, "a" : 6, "q" : 7}

		self.gridY = gridY
		for i in range(gridY):
			self.positions.append([])
			for j in range(gridX):
				self.positions[i].append(0)
		self.positions[5][5] = 0
		print self.getFreeAdjacentPositions((5, 5))
		print(self)

	def __str__(self):
		ret = ""
		for i in range(self.gridY):
			ret += str(self.positions[i])+"\n"
		return ret

	def getStatus(self, pos):
		return self.positions[pos[0]][pos[1]]

	def getPositionInDirection(self, dir, pos):
		ret = None
		if (self.directions[dir] == 0):
			ret = (pos[0],pos[1]-1)
		elif (self.directions[dir] == 1):
			ret = (pos[0]+1,pos[1]-1)
		elif (self.directions[dir] == 2):
			ret = (pos[0],pos[1]+1)
		elif (self.directions[dir] == 3):
			ret = (pos[0]+1,pos[1]+1)
		elif (self.directions[dir] == 4):
			ret = (pos[0],pos[1]+1)
		elif (self.directions[dir] == 5):
			ret = (pos[0]-1,pos[1]+1)
		elif (self.directions[dir] == 6):
			ret = (pos[0]-1,pos[1])
		elif (self.directions[dir] == 7):
			ret = (pos[0]-1,pos[1]-1)
		else:
			print "POSITION DOES NOT EXIST :("

		if self.getStatus(ret) != 0:
			return None
		else:
			return ret

	def getFreeAdjacentPositions(self, pos):
		possiblePos = []
		for dir in self.directions:
			if self.getStatus(self.getPositionInDirection(dir, pos)) == 0:
				possiblePos.append(self.getPositionInDirection(dir, pos))
		print possiblePos

class Navigator():
	def __init__(self, grid, (x, y), (destX, destY)):
		self.grid = grid
		self.pos = (x,y)
		self.dest = (destX, destY)
		self.path = self.createPath((destX, destY), (x, y))

	def draw(self, canvas):
		offset = 50
		navSize = 50
		canvas.create_rectangle(self.pos[0]*offset-navSize/2, self.pos[1]*offset-navSize/2, self.pos[0]*offset+navSize/2, self.pos[1]*offset+navSize/2, outline="#000000")

	def createPath(self, dest, start):
		path = [dest]
		while path[len(path)-1] != start:
			temp = path[len(path)-1]
			if temp[1] > start[1] and temp[0] > start[0]:
				nextPos = self.grid.getPositionInDirection("q", path[len(path)-1])
			elif temp[1] < start[1] and temp[0] > start[0]:
				nextPos = self.grid.getPositionInDirection("z", path[len(path)-1])
			elif temp[1] > start[1] and temp[0] == start[0]:
				nextPos = self.grid.getPositionInDirection("w", path[len(path)-1])
			elif temp[1] < start[1] and temp[0] == start[0]:
				nextPos = self.grid.getPositionInDirection("x", path[len(path)-1])
			elif temp[1] > start[1] and temp[0] < start[0]:
				nextPos = self.grid.getPositionInDirection("e", path[len(path)-1])
			elif temp[1] < start[1] and temp[0] < start[0]:
				nextPos = self.grid.getPositionInDirection("c", path[len(path)-1])
			elif temp[0] > start[0] and temp[1] == start[1]:
				nextPos = self.grid.getPositionInDirection("a", path[len(path)-1])
			elif temp[0] < start[0] and temp[1] == start[1]:
				nextPos = self.grid.getPositionInDirection("d", path[len(path)-1])
			
			if nextPos == None:
				print "need a re route around"
				print path[len(path)-1]
				print self.grid.getFreeAdjacentPositions(path[len(path)-1])
			else:
				path.append(nextPos)

		print path
		return path

	def move(self):
		if len(self.path) > 0:
			self.pos = self.path.pop()


class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.grid = Grid(10, 10)
        self.canvas = Canvas(self)
        self.parent = parent
        self.nav = Navigator(self.grid, (0,0), (10,10))
        self.initUI()
    
    def initUI(self):
        self.parent.title("Pathfinder")

        self.nav.draw(self.canvas)
        self.canvas.pack(fill=BOTH, expand=1)

        self.pack(fill=BOTH, expand=1)

    def draw(self):
     	self.canvas.delete(ALL)
     	for i in range(len(self.grid.positions)-1):
     		self.canvas.create_line(50+50*i,0,50+50*i,500)
     		self.canvas.create_line(0,50+50*i,500,50+50*i)
     	self.nav.draw(self.canvas)

    def update(self):
    	self.nav.move()
     	self.draw()
     	self.after(1000/10, self.update)


def main():
    root = Tk()
    root.geometry("500x500+0+0")
    app = App(root)
    sx = 0
    sy = 0
    ex = 0
    ey = 0

    def setEnd(event):
    	ex = event.x
    	ey = event.y
    	print str(ex)+">"+str(ex/50)+" "+str(ey)+">"+str(ey/50)
    	app.nav = Navigator(app.grid, (0,0), (ex/50,ey/50))

    app.canvas.bind("<1>", setEnd)
    app.canvas.focus_set()
    app.update()
    root.mainloop()

main()
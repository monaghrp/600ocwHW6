# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.w=width
        self.h=height
        self.room=[]
        for i in xrange(0,width):
            temp=[]
            for j in xrange(0,height):
                temp.append('dirty')
            self.room.append(temp)
            
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        ##convert position to integers position
        tempx=int(math.ceil(pos.getX()))-1
        tempy=int(math.ceil(pos.getY()))-1
        self.room[tempx][tempy]='clean'
        

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.room[m-1][n-1]!='clean':
            return False
        else:
            return True
        
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return (self.w*self.h)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        temp=0
        ##print str(self.room)
        for i in xrange(0,self.w):
            for j in xrange(0,self.h):
                
                if self.room[i][j]=='clean':
                    temp+=1
        return temp

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        random.seed()
        return Position(random.uniform(0,self.w),random.uniform(0,self.h))
        

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        
        if pos.getX()<=0 or pos.getX()>self.w:
            return False
        elif pos.getY()<=0 or pos.getY()>self.h:
            return False
        else:
            return True
    def printRoom(self):
        print str(self.room)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.r=room
        self.s=speed
        self.d=random.randint(0,360)
        self.pos=room.getRandomPosition()
        


    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos=position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d=direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError
    def getRoom(self):
        return self.r

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.r.cleanTileAtPosition(self.pos)
        new_pos=self.pos.getNewPosition(self.d,self.s)
        if self.r.isPositionInRoom(new_pos):
            self.setRobotPosition(new_pos)
        else:
            self.setRobotDirection(random.uniform(0,360.0))            

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    done=0
    mean_num_steps=0
    num_steps=[]
    for j in xrange(0,num_trials):
            num_steps.append(0)
    ##main num_trials loop
    for i in xrange(0,num_trials):
        ##create room
        room=RectangularRoom(width,height)
        ##initialize robot
        robots=[]
        for j in xrange(0,num_robots):
                robots.append(robot_type(room,speed))
        done=0
        ##anim=ps6_visualize.RobotVisualization(num_robots,width,height)
        while done !=1:
            num_steps[i]+=1
            for j in xrange(0,num_robots):
                ##print 'jth robot: ' + str(j)
                ##print 'room: ' + str(robots[j].r.printRoom())
                ##anim.update(room,robots)
                robots[j].updatePositionAndClean()
            pclean=float(room.getNumCleanedTiles())/float(room.getNumTiles())
            ##print 'num tiles clean: ' +str(room.getNumCleanedTiles())
            ##print 'room: ' + str(room.printRoom())
            if pclean>=min_coverage:
                ##print 'num steps: ' + str(num_steps[i])
                done=1
        ##anim.done()
        ##print 'trial nth: ' + str(i)
    ##print 'num steps: ' + str(num_steps)
    return float(sum(num_steps)/float(num_trials))


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    data=[]
    data.append(0)
    for i in xrange(1,11):
        data.append(runSimulation(i,1,20,20,.8,100,StandardRobot))
    pylab.plot(data)
    pylab.title('Ticks to Clean a 20x20 room to 80%')
    pylab.xlabel('Robots')
    pylab.ylabel('Ticks')
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    data=[]
    data.append(runSimulation(2,1,20,20,.8,100,StandardRobot))
    data.append(runSimulation(2,1,25,16,.8,100,StandardRobot))
    data.append(runSimulation(2,1,40,10,.8,100,StandardRobot))
    data.append(runSimulation(2,1,50,8,.8,100,StandardRobot))
    data.append(runSimulation(2,1,80,5,.8,100,StandardRobot))
    data.append(runSimulation(2,1,100,4,.8,100,StandardRobot))
    pylab.plot(data)
    pylab.title('Ticks to Clean various room sizes to 80%')
    pylab.xlabel('Room Size')
    pylab.ylabel('Ticks')
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        self.r.cleanTileAtPosition(self.pos)
        new_pos=self.pos.getNewPosition(self.d,self.s)
        if self.r.isPositionInRoom(new_pos):
            self.setRobotPosition(new_pos)
            self.setRobotDirection(random.uniform(0,360.0))  
        else:
            self.setRobotDirection(random.uniform(0,360.0))  



# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    data1=[]
    data1.append(0)
    for i in xrange(1,11):
        data1.append(runSimulation(i,1,20,20,.8,100,StandardRobot))
    pylab.plot(data1)
    data2=[]
    data2.append(0)
    for i in xrange(1,11):
        data2.append(runSimulation(i,1,20,20,.8,100,RandomWalkRobot))
    pylab.plot(data2)
    pylab.title('Ticks to Clean a 20x20 room to 80%')
    pylab.xlabel('Robots')
    pylab.ylabel('Ticks')
    pylab.show()

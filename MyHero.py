'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *
from moba4 import *
from behaviortree import *
from mybehaviors import *

##############################################################
### MyHero
#region Helper Functions
def rotateVector(vector,degrees):
	theta = math.radians(degrees)
	x_prime = math.cos(theta)*vector[0] - math.sin(theta)*vector[1]
	y_prime = math.sin(theta)*vector[0] + math.sin(theta)*vector[1]
	return (x_prime,y_prime)
#endregion

class MyHero(Hero, BehaviorTree):
	
	def __init__(self, position, orientation, world, image = AGENT, speed = SPEED, viewangle = 360, hitpoints = HEROHITPOINTS, firerate = FIRERATE, bulletclass = BigBullet, dodgerate = DODGERATE, areaeffectrate = AREAEFFECTRATE, areaeffectdamage = AREAEFFECTDAMAGE):
		Hero.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass, dodgerate, areaeffectrate, areaeffectdamage)
		BehaviorTree.__init__(self)

		pos = self.position
		self.id = 3
		self.node_vectors = [(50,0),(75,-15),(75,15)]
		self.nodes = [(125,145),(150,130),(150,160)]
	
	def update(self, delta):
		Hero.update(self, delta)
		BehaviorTree.update(self, delta)

		# Update Formation Nodes
		healer_vector = rotateVector(self.node_vectors[0], self.orientation)
		companion1_vector = rotateVector(self.node_vectors[1], self.orientation)
		companion2_vector = rotateVector(self.node_vectors[2], self.orientation)
		self.nodes = [healer_vector, companion1_vector, companion2_vector]

	def start(self):
		# Build the tree
		spec = treeSpec(self)
		if spec is not None and (isinstance(spec, list) or isinstance(spec, tuple)):
			self.buildTree(spec)
		else:
			self.setTree(myBuildTree(self))
		# Start the agent
		Hero.start(self)
		BehaviorTree.start(self)


	
	def stop(self):
		Hero.stop(self)
		BehaviorTree.stop(self)




"""This Code is made by Musab Schluck as a small project to mimic an air defence system
	where an object is being intercepted by a missile, while this is super simplified in terms of 
	the number of dimensions and ignoring, the physical limitations that would arise in a real-life 
	situation, but I believe it still is a good way to approximate such a system, conceptually, and 
	coding-wise."""
from random import uniform
import matplotlib.pyplot as plt


class Obj:
	def __init__(self):
		self.traj_co = self.return_traj_co() #[i0, i1, i2]
		self.pos = []

	def return_traj_co(self):
		# traj constrains:
		# - in the domain [0,20] range can't exceed (0,20)
		is_valid_trajectory = False
		while not is_valid_trajectory:
			i0 = uniform(0.5, 19.5)
			i1 = uniform(-5, 5)
			i2 = uniform(-5, 5)
			y = [i0, i1, i2]
			for x in range(20):
				yt = i0 + i1*x +i2*x**2
				if yt > 20 or yt < 0:
					break
				if x == 19:
					is_valid_trajectory = True
		return y

	def move_obj(self, x):
		y = self.traj_co[0] + self.traj_co[1]*x + self.traj_co[2]*x**2
		self.pos = [x, y]

class Msk_hitter:
	def __init__(self):
		self.obj_pos_hist = []
		self.shot_pos = [10,0]
		self.estimated_obj_next_pos = (0, 10)

	def pos_radar_reading(self, other): 
		self.obj_pos_hist.append(other.pos)

	def estimate_new_position(self, x):
		doph = self.obj_pos_hist
		if len(doph) > 3:
			slope = doph[-1][1] - doph[-2][1]
			slop_of_slope = slope - (doph[-2][1] - doph[-3][1])
			estimated_y = doph[-1][1] + slope + slop_of_slope
			self.estimated_obj_next_pos = (x, estimated_y)

	def interseptor_tracking(self):
		oep = self.estimated_obj_next_pos
		ip = self.shot_pos
		x = oep[0] - ip[0]
		y = oep[1] - ip[1]
		# print("estimated object position:",oep)
		d = (x**2 + y **2)**0.5
		if x >= 1 or x <= -1:
			self.shot_pos[0] += x/abs(x) + uniform(-0.2, 0.2)  # uniform(-0.2, 0.2) this is not important, in fact it is bad for the system but it makes it look realistic and so good so I decided to keep it.
		elif x > 0 or x < 0:
			self.shot_pos[0] += x
		if y >= 1 or y <= -1:
			self.shot_pos[1] += y/abs(y)
		elif y > 0 or y < 0:
			self.shot_pos[1] += y


	def is_hit(self, other):
		tolerance = 0.01
		op = other.pos
		ip = self.shot_pos
		x = op[0] - ip[0]
		y = op[1] - ip[1]
		d = (x**2 + y **2)**0.5
		if d < tolerance:
			return True


def main():
	for time in range(500):
		obj_x = []
		obj_y = []
		shot_x = []
		shot_y = []

		obj = Obj()
		hitter = Msk_hitter()
		for x in range(20):
			hitter.pos_radar_reading(obj) # always one step behind, as in real-life 
			obj.move_obj(x)					# this line being here gives meaning to the previous comment
			hitter.estimate_new_position(x)
			hitter.interseptor_tracking()
			obj_x.append(obj.pos[0])				#		These 4 lines
			obj_y.append(obj.pos[1])				#		of code are
			shot_x.append(hitter.shot_pos[0])		#		for collecting the data
			shot_y.append(hitter.shot_pos[1])		#		for the graph
			# print("real pos:", obj.pos, "interseptor pos:", hitter.shot_pos,
			# 	"error:", (obj.pos[0] - hitter.shot_pos[0], obj.pos[1] - hitter.shot_pos[1]))
			if hitter.is_hit(obj) == True:
				# print("the object has been inturpted secsesfully, at {}".format(obj.pos))
				plt.plot(obj_x, obj_y, marker = "o", lw = 0.5, ms = 0.4, c = "red")
				plt.plot(shot_x, shot_y, marker = "s", lw = 0.5, ms = 0.4, c = "Blue")
				obj_x.clear()
				obj_y.clear()
				shot_x.clear()
				shot_y.clear()
				break		
	plt.ylim(0,20)
	plt.xlim(0,20)
	plt.show()
main()

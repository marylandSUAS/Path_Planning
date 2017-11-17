import MAVLink

class Mission_Objective:
	self.wp_list = []

	def _init_(self,mission_type):
		self.mission_type = mission_type

	def _init_(self,mission_type,wp_lst):
		self.mission_type = mission_type
		self.wp_list = wp_lst

	def add_wp(self,wp_id,location):
		self.wp_list.append((wp_id,location))

		# If not found: return -1
		# If found: return 1
	def del_wp(self,wp_id):
		self.wp_list.remove(wp_id)

	def execute(self):

	def abort(self):
		
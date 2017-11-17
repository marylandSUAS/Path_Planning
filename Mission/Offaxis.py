class offaxis(Mission_Objective):
	def execute(self):

	def set_gimbal(self,yaw,pitch,roll):
		gimbal.set(yaw,pitch,roll)
	def send_photo(self):
		#Communcations Group
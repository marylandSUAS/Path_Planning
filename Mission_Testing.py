# mission senario getter

class Mission():
	def __init__(self):
		self.MissionWPs = []
		self.Bounds = []
		self.StaticObs = []
		self.dropLoc = []
		self.offAxisLoc = []
		self.Emergent = []
		self.SearchGridPoints = []



def Mission(mission):

	Mission_Class = Mission()

	if (mission == 'FreeState'):

		self.Home = [39.0827766,-76.9045329,100]
		self.bounds.append([39.0834553,-76.9015503,100])
		self.bounds.append([39.0852209,-76.9020009,100])
		self.bounds.append([39.0858871,-76.9048977,100])
		self.bounds.append([39.0845713,-76.9081593,100])
		self.bounds.append([39.0812734,-76.9091034,100])

		self.dropLoc = [39.0829536,-76.9045517,100]

		self.MissionWPs.append([39.0834845,-76.9032079,100])
		self.MissionWPs.append([39.0823685,-76.9069576,100])
		self.MissionWPs.append([39.0844839,-76.9060671,100])
		self.MissionWPs.append([39.0840008,-76.9036156,100])

		self.offAxisLoc = [39.0823685,-76.9043827,100]

		self.Emergent = [39.0834429,-76.9048011,100]

	if (mission == 'PGRC'):
		pass

	if (mission == 'SouthernMarylandField'):
		self.Home = []
		
		

	if (mission == 'Real1'):
		# N38-08-45.03 W076-25-34.95
		dropspot = Locationwp().Set(38.3652711,-76.5366065,50, 16)


		# self.bounds.append(Locationwp().Set(38.3652015,-76.5390927,0, 16))
		# self.bounds.append(Locationwp().Set(38.3659207,-76.5388942,0, 16))
		# self.bounds.append(Locationwp().Set(38.3658198,-76.5372419,0, 16))
		# self.bounds.append(Locationwp().Set(38.3669806,-76.5368342,0, 16))
		# self.bounds.append(Locationwp().Set(38.3666441,-76.5348816,0, 16))
		# self.bounds.append(Locationwp().Set(38.3659375,-76.5350318,0, 16))
		# self.bounds.append(Locationwp().Set(38.3652309,-76.5335298,0, 16))
		# self.bounds.append(Locationwp().Set(38.3647766,-76.5338302,0, 16))

		# offaxisloc = Locationwp().Set(38.3646505,-76.5376335,0, 16)


	if (mission == 'Real2'):
		pass


	return Mission_Class
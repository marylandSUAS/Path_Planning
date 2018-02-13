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
		self.bounds.append([39.1116984,-77.1371448,0])
		self.bounds.append([39.1076774,-77.1437323,0])
		self.bounds.append([39.1058126,-77.1406960,0])
		self.bounds.append([39.1070114,-77.1330786,0])
		self.bounds.append([39.1085183,-77.1323276,0])
		self.bounds.append([39.1092259,-77.1359754,0])

		self.dropLoc = [39.1095006,-77.1377134,0]

		self.MissionWPs.append([39.1088096,-77.1392906,0])
		self.MissionWPs.append([39.1080354,-77.1418226,0])
		self.MissionWPs.append([39.1067367,-77.1416080,0])
		self.MissionWPs.append([39.1074360,-77.1371663,0])
		self.MissionWPs.append([39.1075442,-77.1357930,0])

		self.offAxisLoc = [39.1100334,-77.1410608,0]


	# Main paved runway
	if (mission == 'CASA1'):
		pass

	# tarp runway
	if (mission == 'CASA2'):
		pass

	if (mission == 'PGRC'):
		pass

	if (mission == 'SouthernMarylandField'):
		pass

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
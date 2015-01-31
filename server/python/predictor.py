from datetime import datetime

def read_sensordata(filename="dummy_data.txt"):
	# Read file lines and convert to integers:
	f = open(filename)
	info = [ map(lambda x : int(float(x)), line.replace("\n","").split()) for line in f.readlines() ]
	f.close()
	
	# Convert time to hours:
	new_info = []
	for line in info:
		d = datetime.fromtimestamp(line[0])
		new_info.append( (line[0], [d.timetuple().tm_hour] + line[1:]) )
	assert len(new_info) > 48, "Provide more than two days of sensory data"
	return new_info
	
def read_used(filename="dummy_times.txt"):
	# Read file lines and convert to integers:
	f = open(filename)
	info = [ int(float(line.replace("\n",""))) for line in f.readlines() ]
	f.close()
	assert len(info) > 0, "Please provide some example uses"
	return info
	
def zip_data(sensory, useds):
	def day_was_used(day_ending, useds):
		for use in useds:
			if day_ending < use and  (24*60*60 + day_ending) > use:
				return True
		return False
	from itertools import chain
	flatten = lambda x : list(chain(*x))
	# Start sensory measurements at 8 o'clock in the morning:
	while sensory[0][1][0] != 8:
		sensory.pop(0)

	days = []
	while len(sensory) >= 24:
		day = [ sensory.pop(0) for _ in xrange(24) ]
		day_sensors = flatten([ l[1] for l in day ])
		day_ending = day[23][0]
		days.append((day_ending, day_sensors))
	
	examples = []
	classes = []
	for ending, sensors in days:
		examples.append(sensors)
		if day_was_used(ending, useds):
			classes.append(1)
		else:
			classes.append(0)
		
	classes.pop()
	last24 = examples.pop()

	return examples, classes, last24
	
	
def predict():
	from sklearn.svm import SVC
	sensory = read_sensordata()
	useds = read_used()
	X, y, last24 = zip_data(sensory, useds)
	clf = SVC()
	clf.fit(X, y)
	prediction = clf.predict([last24])[0]
	return prediction
	
if __name__=="__main__":
	from create_data import gen_measurements
	gen_measurements()
	print predict()
	
				
	
	
	
	
	

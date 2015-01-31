from time import time
from random import random, choice



def gen_measurements(n=10*24, threshold=0.53333):
	t = time()
	r = lambda : choice([-10,10]) * random()
	
	measurements = []
	for i in xrange(n):
		s = [ t - i*60*60, r(), r(), r() ]
		measurements.append(s)
	
	days = []
	for i in xrange(n/24):
		if random() < threshold:
			days.append( t - i*24*60*60 )
	days = sorted(days)
			
	f = open('dummy_data.txt', 'w')
	for line in measurements:
		f.write("".join([ str(e) +" " for e in line]) + "\n")
	f.close()
	
	f = open('dummy_times.txt', 'w')
	for e in days:
		f.write("".join( str(e) +  "\n"))
	f.close()

if __name__=="__main__":
	gen_measurements()
	
			
	

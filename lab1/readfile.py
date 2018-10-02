try:
	fin = open('file', 'r')
except IOError:
	print ("Exception found")
else:
	top = fin.readlines()
	for s in top:
		print (s)



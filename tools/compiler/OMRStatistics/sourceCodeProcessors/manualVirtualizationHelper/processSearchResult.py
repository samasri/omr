file = open('search')

count = 0
for r in file:
	r = r.strip()
	if count == 0: 
		count += 1
		continue
	if count > 0:
		if r == '--------------------':
			count = 0
			continue
		else: 
			r = r.split(':')
			file = r[0]
			line = r[1]
			print file
			count += 1
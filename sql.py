import MySQLdb

def SQLfunc(cmd):

	db = MySQLdb.connect(host="academic-mysql.cc.gatech.edu",
		user="cs4400_Group_17",
		passwd="NBYelv9r",
		db="cs4400_Group_17")
	print cmd
	cur = db.cursor()
	cur.execute(cmd)
	db.commit()
	result = cur.fetchall()
	list = []
	for row in result:
		for col in row:

			list.append(col)

	return list

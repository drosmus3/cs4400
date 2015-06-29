import MySQLdb
 
def SQLfunc(cmd):

	db = MySQLdb.connect(host="academic-mysql.cc.gatech.edu",
		user="cs4400_Group_17",
		passwd="NBYelv9r",
		db="cs4400_Group_17")

	cur = db.cursor()

	cur.execute(cmd)
	return cur.fetchall()

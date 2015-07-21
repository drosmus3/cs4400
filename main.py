from Tkinter import *
import Tkinter as ttk
from sql import *
import re
import string
import datetime

class App(ttk.Tk):
	def __init__(self, *args):
		ttk.Tk.__init__(self, *args)

		container = ttk.Frame(self)

		container.pack(side = "top", fill = "both", expand = True)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}
		for F in (loginScreen, guestwindow, ownerwindow, inspectorwindow):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky="nsew")

		self.show_frame(loginScreen)

	def show_frame(self, clazz):
		# Show the class (frame) passed in
		frame = self.frames[clazz]
		frame.tkraise()

	def resizeWindow(self, sizeStr):
		self.geometry(sizeStr)

class loginScreen(ttk.Frame):
	def __init__(self, master, controller):
		ttk.Frame.__init__(self, master)
		Label(self, text = "Guest").grid(row = 0)

		GuestLog = ttk.Button(self, text = "Login", command = lambda: controller.show_frame(guestwindow))
		GuestLog.grid(row = 0, column = 1)

		ttk.Label(self, text = "Restaurant Owner / Health Inspector Login").grid(row = 2, columnspan = 2, rowspan = 2)

		ttk.Label(self, text = "Username").grid(row = 4)
		ttk.Label(self, text = "Password").grid(row = 5)

		username = ttk.Entry(self)
		password = ttk.Entry(self)
		username.grid(row = 4, column = 1)
		password.grid(row = 5, column = 1)

		#MainLog = Button(root, text = "Login", command = self.openRohiWindow)
		MainLog = Button(self, text = "Login", command = lambda: self.openRohiWindow(controller,username.get(),password.get()))
		MainLog.grid(row = 6, column = 1)

	def openRohiWindow(self,controller,username,password):
		if not SQLfunc("SELECT * FROM registereduser WHERE username = " + "'" + username + "'"):
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow, "User not found")
		elif not SQLfunc("SELECT * FROM registereduser WHERE username = " + "'" + username + "' AND password = " + "'" + password + "'"):
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow, "Incorrect password")
		elif SQLfunc("SELECT * FROM operatorowner WHERE username = " + "'" + username + "'"):
			global globemail
			globemail = SQLfunc("SELECT email FROM operatorowner WHERE username = " + "'" + username + "'")
			globemail = globemail[0]
			controller.show_frame(ownerwindow)

		else:
			global globinspid
			globinspid = SQLfunc("SELECT iid FROM inspector WHERE username = " + "'" + username + "'")
			globinspid = globinspid[0]
			print globinspid
			controller.show_frame(inspectorwindow)

class guestwindow(ttk.Frame):
	def __init__(self, master, controller):
		ttk.Frame.__init__(self, master)

		title = ttk.Label(self, text = "Guest GA Restaurant Health Inspections").grid(row = 0, columnspan = 2)
		search = ttk.Button(self, text = "Search for Restaurant", command = self.openguestsearch)
		complaint = ttk.Button(self, text = "File a complaint", command = self.opencomplaint)
		back = ttk.Button(self, text = "Back to Login Screen", command = lambda: controller.show_frame(loginScreen))
		search.grid(row = 1, column = 0)
		complaint.grid(row = 1, column = 1)
		back.grid(row = 2, columnspan = 2)

	def openguestsearch(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = guestsearch(self.newWindow)

	def opencomplaint(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = guestcomplaint(self.newWindow)

class guestsearch:
	def __init__(self, master):
		self.master = master
		self.frame = ttk.Frame(self.master)

		ttk.Label(self.frame, text = "Restaurant Search").grid(row = 0, columnspan = 2)
		ttk.Label(self.frame, text = "Name").grid(row = 1)
		ttk.Label(self.frame, text = "Score*").grid(row = 2)
		ttk.Label(self.frame, text = "Zipcode*").grid(row = 3)
		ttk.Label(self.frame, text = "Cuisine").grid(row = 4)

		bname = Entry(self.frame)
		bscore = Entry(self.frame)
		bzipcode = Entry(self.frame)
		bname.grid(row = 1, column = 1)
		bscore.grid(row = 2, column = 1)
		bzipcode.grid(row = 3, column = 1)

		lessgreater = [
			">",
			"<"
		]

		lgvariable = StringVar(self.frame)
		lgvariable.set(lessgreater[0])
		apply(OptionMenu, (self.frame, lgvariable) + tuple(lessgreater)).grid(row = 2, column = 2)

		cuisines = SQLfunc("SELECT cuisine FROM cuisines")
		cuisines.insert(0, "All Cuisines")
		cuisineSelect = StringVar(self.frame)
		cuisineSelect.set(cuisines[0])
		apply(OptionMenu, (self.frame, cuisineSelect) + tuple(cuisines)).grid(row = 4, column = 1)

		cancel = ttk.Button(self.frame, text = "Close", command = self.close)
		cancel.grid(row = 5, column = 0)

		submit = ttk.Button(self.frame, text = "Submit", command = lambda: self.submitinfo(bname.get(), bscore.get(), lgvariable.get(), bzipcode.get(), cuisineSelect.get()))
		submit.grid(row = 5, column = 4)

		self.frame.pack()

	def close(self):
		self.master.destroy()

	def submitinfo(self,name,score,lg,zip,cuisine):
		searchResult = []
		self.frame.destroy()
		self.frame = ttk.Frame(self.master)

		ttk.Label(self.frame, text = "Restaurant Search").grid(row = 0, columnspan = 2)
		ttk.Label(self.frame, text = "Name").grid(row = 1)
		ttk.Label(self.frame, text = "Score*").grid(row = 2)
		ttk.Label(self.frame, text = "Zipcode*").grid(row = 3)
		ttk.Label(self.frame, text = "Cuisine").grid(row = 4)

		bname = Entry(self.frame)
		bscore = Entry(self.frame)
		bzipcode = Entry(self.frame)
		bname.grid(row = 1, column = 1)
		bscore.grid(row = 2, column = 1)
		bzipcode.grid(row = 3, column = 1)

		lessgreater = [
			">",
			"<"
		]

		lgvariable = StringVar(self.frame)
		lgvariable.set(lessgreater[0])
		apply(OptionMenu, (self.frame, lgvariable) + tuple(lessgreater)).grid(row = 2, column = 2)

		cuisines = SQLfunc("SELECT cuisine FROM cuisines")
		cuisines.insert(0, "All Cuisines")
		cuisineSelect = StringVar(self.frame)
		cuisineSelect.set(cuisines[0])
		apply(OptionMenu, (self.frame, cuisineSelect) + tuple(cuisines)).grid(row = 4, column = 1)

		if not score or not score.isdigit() or int(score) < 0 or int(score) > 100:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid score")
		elif not zip or not zip.isdigit() or int(zip) <10000 or int(zip) > 99999:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid zip code")
		else:
			searchString = ('SELECT name, street, city, state, zipcode, cuisine, totalscore, lastInspectdate '
				'FROM restaurant '
				'JOIN ('
				'	SELECT rid, totalscore, max(idate) AS lastInspectDate '
				'	FROM inspection '
				'	GROUP BY rid'
				') AS latestInspection '
				'ON restaurant.rid = latestInspection.rid '
				'WHERE (')
			needand = False
			if name:
				searchString = searchString + "name = '" + name + "'"
				needand = True
			if score:
				if needand:
					searchString = searchString + " AND "
				searchString = searchString + "totalscore" + lg + score
				needand = True
			if zip:
				if needand:
					searchString = searchString + " AND "
				searchString = searchString + "zipcode = " + zip
				needand = True
			if cuisine != "All Cuisines":
				if needand:
					searchString = searchString + " AND "
				searchString = searchString + "cuisine = '" + cuisine + "'"
			searchString = searchString + ') ORDER BY totalscore desc'
			searchResult = SQLfunc(searchString)

			if (len(searchResult)):
				Label(self.frame, text = "Restaurant").grid(row = 5)
				Label(self.frame, text = "Address").grid(row = 5, column = 1)
				Label(self.frame, text = "Cuisine").grid(row = 5, column = 2)
				Label(self.frame, text = "Last Inspection Score").grid(row = 5, column = 3)
				Label(self.frame, text = "Date of Last Inspection").grid(row = 5, column = 4)

				for i in range (len(searchResult) / 8):
					Label(self.frame, text = searchResult[0 + i * 8]).grid(row = i + 6)
					Label(self.frame, text = searchResult[1 + i * 8] + ", " + searchResult[2 + i * 8] + ", " + searchResult[3 + i * 8] + " " + str(searchResult[4 + i * 8])).grid(row = i + 6, column = 1)
					#Label(self.frame, text = searchResult[1 + i * 8] + ", " + searchResult[2 + i * 8] + ", " + searchResult [3 + i * 8]).grid(row = i + 1, column = 1)
					Label(self.frame, text = searchResult[5 + i * 8]).grid(row = i + 6, column = 2)
					Label(self.frame, text = str(searchResult[6 + i * 8])).grid(row = i + 6, column = 3)
					Label(self.frame, text = str(searchResult[7 + i * 8])).grid(row = i + 6, column = 4)

				#NEED TO ADD: Actually displaying the restaurants
			else:
				Label(self.frame, text = "No results found").grid(row = 5, columnspan = 2)

		cancel = ttk.Button(self.frame, text = "Close", command = self.close)
		cancel.grid(row = 7 + len(searchResult) / 8)

		submit = ttk.Button(self.frame, text = "Submit", command = lambda: self.submitinfo(bname.get(), bscore.get(), lgvariable.get(), bzipcode.get(), cuisineSelect.get()))
		submit.grid(row = 7 + len(searchResult) / 8, column = 4)
		self.frame.pack()

class guestcomplaint:
	def __init__(self, master):
		self.master = master
		self.frame = ttk.Frame(self.master)

		Label(self.frame, text = "Restaurant").grid(row = 0, column = 0)
		restaurants = SQLfunc('SELECT name FROM restaurant')

		restaurantSelect = StringVar(self.frame)
		restaurantSelect.set(restaurants[0])
		apply(OptionMenu, (self.frame, restaurantSelect) + tuple(restaurants)).grid(row = 0, column = 1)

		Label(self.frame, text = "Date of Meal (YYYY-MM-DD)").grid(row = 2)
		Label(self.frame, text = "First Name").grid(row = 3, column = 0)
		Label(self.frame, text = "Last Name").grid(row = 4, column = 0)
		Label(self.frame, text = "Phone #").grid(row = 5, column = 0)
		Label(self.frame, text = "Complaint Description").grid(row = 6, column = 0)

		date = Entry(self.frame)
		first = Entry(self.frame)
		last = Entry(self.frame)
		phone = Entry(self.frame)
		description = Entry(self.frame)
		date.grid(row = 2, column = 1)
		first.grid(row = 3, column = 1)
		last.grid(row = 4, column = 1)
		phone.grid(row = 5, column = 1)
		description.grid(row = 6, column = 1)

		cancel = Button(self.frame, text = "Cancel", command = self.close)
		cancel.grid(row = 7, column = 0)

		submit = Button(self.frame, text = "Submit", command = lambda: self.submitComplaint(date.get(),first.get(),last.get(),phone.get(),description.get(),restaurantSelect.get()))
		submit.grid(row = 7, column = 1)
		self.frame.pack()

	def close(self):
		self.master.destroy()

	def submitComplaint(self,date,first,last,phone,description,restaurant):
		r = re.compile('\d{4}-\d{2}-\d{2}')
		correctDate = None
		if r.match(date) and (date[0] + date[1] + date[2] + date[3] + date[5] + date[6] + date [8] + date[9]).isdigit():
			try:
				newDate = datetime.datetime(int(date[0] + date[1] + date[2] + date[3]),int(date[5] + date[6]),int(date[8] + date[9]))
				correctDate = True
			except ValueError:
				correctDate = False

		if r.match(date) is None:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid date in the format:YYYY-MM-DD")
		elif not correctDate:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid date in the format:YYYY-MM-DD")
		elif not first or len(first) > 15:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a first name")
		elif not last or len(last) > 30:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a last name")
		elif not phone or not phone.isdigit() or int(phone) < 1000000000 or int(phone) > 9999999999:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid phone number")
		elif not description or len(description) > 80:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid description")
		else:
			if not SQLfunc("SELECT phone FROM customer WHERE phone = " + "'" + phone + "';"):
				SQLfunc("INSERT INTO customer (phone, firstname, lastname) VALUES (" + "'" + phone + "', '" + first + "', '" + last + "')")
			RestID = SQLfunc("SELECT rid FROM restaurant WHERE name = " + "'" + restaurant + "'")
			SQLfunc("INSERT INTO complaint (cdate, rid, phone, description) VALUES (" + "'" + date + "', " + str(RestID[0]) + ", '" + phone + "', '" + description + "')")
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Complaint Submitted")

class ownerwindow(ttk.Frame):
	def __init__(self, master, controller):
		ttk.Frame.__init__(self, master)
		search = ttk.Button(self, text = "Enter information about a restaurant", command = self.openrestrauntinfo)
		complaint = ttk.Button(self, text = "View health inspection reports", command = self.openinspectionreport)
		back = ttk.Button(self, text = "Back to Login Screen", command = lambda: controller.show_frame(loginScreen))
		search.grid(row = 0)
		complaint.grid(row = 1)
		back.grid(row = 2)

	def openrestrauntinfo(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = restrauntinfo(self.newWindow)

	def openinspectionreport(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = inspectionreportsrestaurant(self.newWindow)

# window
class restrauntinfo:
	def __init__(self,master):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Enter All Information").grid(row = 0, columnspan = 4)
		ttk.Label(self.window, text = "Restraunt Name").grid(row = 1)
		ttk.Label(self.window, text = "Phone").grid(row = 2)
		ttk.Label(self.window, text = "Health Permit ID").grid(row = 3)
		ttk.Label(self.window, text = "Health Permit Expiration (YYYY-MM-DD)").grid(row = 4)
		ttk.Label(self.window, text = "Cuisine").grid(row = 5)

		cuisines = SQLfunc("SELECT cuisine FROM cuisines")
		cuisineSelect = StringVar(self.window)
		cuisineSelect.set(cuisines[0])
		apply(OptionMenu, (self.window, cuisineSelect) + tuple(cuisines)).grid(row = 5, column = 1)

		ttk.Label(self.window, text = "Street").grid(row = 1, column = 2)
		ttk.Label(self.window, text = "City").grid(row = 2, column = 2)
		ttk.Label(self.window, text = "State").grid(row = 3, column = 2)
		ttk.Label(self.window, text = "Zipcode").grid(row = 4, column = 2)
		ttk.Label(self.window, text = "County").grid(row = 5, column = 2)

		name = ttk.Entry(self.window)
		street = ttk.Entry(self.window)
		city = ttk.Entry(self.window)
		state = ttk.Entry(self.window)
		zipcode = ttk.Entry(self.window)
		county = ttk.Entry(self.window)
		phone = ttk.Entry(self.window)
		permitid = ttk.Entry(self.window)
		permitexpdate = ttk.Entry(self.window)

		permitid.grid(row = 3, column = 1)
		permitexpdate.grid(row = 4, column = 1)
		name.grid(row = 1, column = 1)
		street.grid(row = 1, column = 3)
		city.grid(row = 2, column = 3)
		state.grid(row = 3, column = 3)
		zipcode.grid(row = 4, column = 3)
		county.grid(row = 5, column = 3)
		phone.grid(row = 2, column = 1)

		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 6)
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(permitid.get(), permitexpdate.get(), name.get(), street.get(), city.get(), state.get(), zipcode.get(), county.get(), phone.get(), cuisineSelect.get()))
		submit.grid(row = 6, column = 6)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitinfo(self,permitid,permitexpdate,name,street,city,state,zipcode,county,phone,cuisine):
		r = re.compile('\d{4}-\d{2}-\d{2}')
		correctDate = None
		if r.match(permitexpdate):
			try:
				newDate = datetime.datetime(int(permitexpdate[0] + permitexpdate[1] + permitexpdate[2] + permitexpdate[3]),int(permitexpdate[5] + permitexpdate[6]),int(permitexpdate[8] + permitexpdate[9]))
				correctDate = True
			except ValueError:
				correctDate = False

		if not name or len(name) > 30:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow, "Please enter a valid name")
		elif not phone or not phone.isdigit() or int(phone) < 1000000000 or int(phone) > 9999999999:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid phone number")
		elif not permitid:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a permit ID")
		elif r.match(permitexpdate) is None:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a permit expiration date in the format: YYYY-MM-DD")
		elif not correctDate:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid permit expiration date in the format:YYYY-MM-DD")
		elif not street or len(street) > 20:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid street")
		elif not city or len(city) > 20:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid city")
		elif not state or len(state) > 2:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid state")
		elif (not zipcode) or int(zipcode) <10000 or int(zipcode) > 99999:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid zip code")
		elif not county or len(county) > 20:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid county")
		elif SQLfunc("SELECT * FROM healthpermit WHERE hpid =" + str(permitid)):
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Health permit ID already exists")
		else:
			rid = SQLfunc("select MAX(rid) FROM restaurant")
			newrid = rid[0] + 1
			print "INSERT INTO restaurant (rid, phone, name, street, city, state, zipcode, county, cuisine, email) VALUES (" + str(newrid) + ", '" + str(phone) + "', '" + str(name) + ", '" + str(street) + "', '" + str(city) + "', '" + str(state) + "', " + str(zipcode) + ", '" + str(county) + "', '" + str(cuisine) + "', '" + str(globemail) + "')"
			SQLfunc("INSERT INTO restaurant (rid, phone, name, street, city, state, zipcode, county, cuisine, email) VALUES (" + str(newrid) + ", '" + str(phone) + "', '" + str(name) + "', '" + str(street) + "', '" + str(city) + "', '" + str(state) + "', " + str(zipcode) + ", '" + str(county) + "', '" + str(cuisine) + "', '" + str(globemail) + "')")
			SQLfunc("INSERT INTO healthpermit (hpid, expirationdate, rid) VALUES (" + permitid + ", '" + permitexpdate + "', " + str(newrid) + ")")
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow, "Restaurant info submitted")

class inspectionreportsrestaurant:
	def __init__(self,master):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Select your restaurant").grid(row = 0, column=0, sticky="W")

		restaurants = SQLfunc("SELECT name FROM restaurant WHERE email = " + "'" + globemail + "'")

		restaurantSelect = StringVar(self.window)
		restaurantSelect.set(restaurants[0])
		apply(OptionMenu, (self.window, restaurantSelect) + tuple(restaurants)).grid(row = 1)

		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitrestaurant(restaurantSelect.get()))
		submit.grid(row = 1, column = 1, sticky="W")
		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 6)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitrestaurant(self,restaurant):

		self.window.destroy()
		self.window = ttk.Frame(self.master)

		ttk.Label(self.window, text = "Select your restaurant").grid(row = 0, column=0, sticky="W")

		restaurants = SQLfunc("SELECT name FROM restaurant WHERE email = " + "'" + globemail + "'")

		restaurantSelect = StringVar(self.window)
		restaurantSelect.set(restaurants[0])
		apply(OptionMenu, (self.window, restaurantSelect) + tuple(restaurants)).grid(row = 1, column=0, sticky="W")
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitrestaurant(restaurantSelect.get()))
		submit.grid(row = 1, column = 1, sticky="W")

		RestID = SQLfunc("SELECT rid FROM restaurant WHERE name = " + "'" + restaurant + "'")
		RestID = str(RestID[0])
		inspections = SQLfunc("SELECT idate, totalscore, passfail FROM inspection WHERE rid = " + RestID + " ORDER BY idate DESC LIMIT 2")

		if len(inspections) > 0:

			self.resultsGrid = ttk.Frame(self.window, background="black")
			self.resultsGrid.grid(sticky="nsew")

			ttk.Label(self.resultsGrid, text = "").grid(row=2, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")
			ttk.Label(self.resultsGrid, text = str(inspections[0])).grid(row = 2, column = 3, padx=1, pady=1)

			ttk.Label(self.resultsGrid, text = "Item Number").grid(row = 3, sticky="nsew", padx=1, pady=1)
			ttk.Label(self.resultsGrid, text = "Item Description").grid(row = 3, column = 1, sticky="nsew", padx=1, pady=1)
			ttk.Label(self.resultsGrid, text = "Score").grid(row = 3, column = 3, sticky="nsew", padx=1, pady=1)

			items = SQLfunc("SELECT itemnum, description FROM item")

			scores2 = SQLfunc("SELECT score FROM contains WHERE rid = " + RestID + " AND idate = " + "'" + str(inspections[0]) + "'")

			for i in range(len(items) / 2):
				ttk.Label(self.resultsGrid, text = str(items[i * 2])).grid(row = 4 + i, column = 0, sticky="nsew", padx=1, pady=1)
				ttk.Label(self.resultsGrid, text = str(items[i * 2 + 1])).grid(row = 4 + i, column = 1, sticky="nsew", padx=1, pady=1)

			for i in range(len(scores2)):
				ttk.Label(self.resultsGrid, text = str(scores2[i])).grid(row = 4 + i, column = 3, sticky="nsew", padx=1, pady=1)

			ttk.Label(self.resultsGrid, text = "TOTAL SCORE").grid(row = 5 + len(scores2), sticky="nsew", padx=1, pady=1)
			ttk.Label(self.resultsGrid, text = "").grid(row = 5 + len(scores2), column=1, sticky="nsew", padx=1, pady=1)
			ttk.Label(self.resultsGrid, text = str(inspections[1])).grid(row = 5 + len(scores2), column = 3, sticky="nsew", padx=1, pady=1)
			ttk.Label(self.resultsGrid, text = "RESULT").grid(row = 6 + len(scores2), sticky="nsew", padx=1, pady=1)
			ttk.Label(self.resultsGrid, text = "").grid(row = 6 + len(scores2), column=1, sticky="nsew", padx=1, pady=1)
			ttk.Label(self.resultsGrid, text = str(inspections[2])).grid(row = 6 + len(scores2), column = 3, sticky="nsew", padx=1, pady=1)

			if len(inspections) > 3:
				ttk.Label(self.resultsGrid, text = "Score").grid(row = 3, column = 2, sticky="nsew", padx=1, pady=1)
				ttk.Label(self.resultsGrid, text = str(inspections[3])).grid(row = 2, column = 2, sticky="nsew", padx=1, pady=1)
				scores1 = SQLfunc("SELECT score FROM contains WHERE rid = " + RestID + " AND idate = " + "'" + str(inspections[3]) + "'")
				ttk.Label(self.resultsGrid, text = str(inspections[4])).grid(row = 5 + len(scores1), column = 2, sticky="nsew", padx=1, pady=1)
				for i in range(len(scores1)):
					ttk.Label(self.resultsGrid, text = str(scores1[i])).grid(row = 4 + i, column = 2, sticky="nsew", padx=1, pady=1)
				ttk.Label(self.resultsGrid, text = str(inspections[5])).grid(row = 6 + len(scores1), column = 2, sticky="nsew", padx=1, pady=1)

			cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
			cancel.grid(row = 7 + len(scores2))

		else:
			ttk.Label(self.window, text = "No inspections for this restaurant: " + restaurant).grid(row = 2)
			cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
			cancel.grid(row = 3)

		self.window.pack()

class inspectorwindow(ttk.Frame):
	def __init__(self, master, controller):
		ttk.Frame.__init__(self, master)
		search = ttk.Button(self, text = "Insert a Restaurant Inspection Report", command = self.openinspreport)
		summarymonth = ttk.Button(self, text = "Summary Report (Search By Specified Month/Year)", command = self.opensummarymonthyear)
		summarycounty = ttk.Button(self, text = "Summary Report (Search By Specified County/Year)", command = self.opensummarycountyyear)
		summarytop = ttk.Button(self, text = "Top Health Inspection Ratings", command = self.opensummarytop)
		summarycomplaints = ttk.Button(self, text = "Customer Complaints", command = self.opensummarycomplaints)
		back = ttk.Button(self, text = "Back to Login Screen", command = lambda: controller.show_frame(loginScreen))

		search.grid(row = 0)
		summarymonth.grid(row = 1)
		summarycounty.grid(row = 2)
		summarytop.grid(row = 3)
		summarycomplaints.grid(row = 4)
		back.grid(row = 5)

	def openinspreport(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = inspreport(self.newWindow)

	def opensummarymonthyear(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = summarymonthyear(self.newWindow)

	def opensummarycountyyear(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = summarycountyyear(self.newWindow)

	def opensummarytop(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = summarytop(self.newWindow)

	def opensummarycomplaints(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = summarycomplaints(self.newWindow)

	def close(self):
		self.master.destroy()

class inspreport:
	def __init__(self,master):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Restaurant ID").grid(row = 0, column = 0)
		ttk.Label(self.window, text = "Inspection Date YYYY-MM-DD").grid(row = 1, column = 0)

		rid = ttk.Entry(self.window)
		date = ttk.Entry(self.window)

		rid.grid(row = 0, column = 1)
		date.grid(row = 1, column = 1)

		items = SQLfunc("SELECT itemnum,description,critical FROM item")

		ttk.Label(self.window, text = "Item Number").grid(row = 2, column = 0)
		ttk.Label(self.window, text = "Item Desctiption").grid(row = 2, column = 1)
		ttk.Label(self.window, text = "Critical").grid(row = 2, column = 2)
		ttk.Label(self.window, text = "Score").grid(row = 2, column = 3)
		ttk.Label(self.window, text = "Comments").grid(row = 2, column = 4)

		for i in range(len(items) / 3):
			ttk.Label(self.window, text = items[3 * i]).grid(row = i + 3, column = 0)
			ttk.Label(self.window, text = items[3 * i + 1]).grid(row = i + 3, column = 1)
			ttk.Label(self.window, text = items[3 * i + 2]).grid(row = i + 3, column = 2)

		score = []
		for i in range(len(items) / 3):
			s = ttk.Entry(self.window)
			s.grid(row = i + 3, column = 3)
			score.append(s)

		comment = []

		for i in range(len(items) / 3):
			c = ttk.Entry(self.window)
			c.grid(row = i + 3, column = 4)
			comment.append(c)

		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 18, column = 0)
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(rid.get(),date.get(),items,score,comment
			))
		submit.grid(row = 18, column = 4)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitinfo(self,rid,date,items,score,comment):
		r = re.compile('\d{4}-\d{2}-\d{2}')
		correctDate = None
		if r.match(date) and (date[0] + date[1] + date[2] + date[3] + date[5] + date[6] + date [8] + date[9]).isdigit():
			try:
				newDate = datetime.datetime(int(date[0] + date[1] + date[2] + date[3]),int(date[5] + date[6]),int(date[8] + date[9]))
				correctDate = True
			except ValueError:
				correctDate = False

		correct = True
		for i in range(len(score)):
			if not score[i].get() or not score[i].get().isdigit() or (items[3 * i + 2] == 'Y' and int(score[i].get()) > 9) or (items[3 * i + 2] == 'N' and int(score[i].get()) > 4) or int(score[i].get()) < 0:
				self.newWindow = ttk.Toplevel(self.master)
				self.app = textwindow(self.newWindow,"Please enter a valid score for item " + str(i + 1))
				correct = False
				break
			if len(comment[i].get()) > 80:
				self.newWindow = ttk.Toplevel(self.master)
				self.app = textwindow(self.newWindow,"Please enter a valid comment for item " + str(i + 1))
				correct = False
				break
		if not correct:
			a = 1
		elif not rid.isdigit() or rid < 0:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid restaurant ID")			
		elif not SQLfunc("SELECT * FROM restaurant WHERE rid = " + str(rid)):
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid restaurant ID")
		elif r.match(date) is None:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid date in the format:YYYY-MM-DD")
		elif not correctDate:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid date in the format:YYYY-MM-DD")
		elif SQLfunc ("SELECT * FROM inspection WHERE rid = " + str(rid) + " AND idate = '" + str(date) + "'"):
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"An inspection already exists for that restaurant and date")		
		else:
			totalscore = 0
			failed = False

			for i in range(len(score)):
				totalscore = totalscore + int(score[i].get())
				if items[3 * i + 2] == 'Y' and int(score[i].get()) < 8:
					failed = True
				print totalscore

			if totalscore < 75:
				failed = True
			if failed:
				passfail = 'FAIL'
			else:
				passfail = 'PASS'

			SQLfunc("INSERT INTO inspection (rid,iid,idate,totalscore,passfail) VALUES (" + str(rid) + "," + str(globinspid) + ",'" + str(date) + "'," + str(totalscore) + ",'" + str(passfail) + "')")

			for i in range(len(score)):
				SQLfunc("INSERT INTO contains (itemnum,rid,idate,score) VALUES (" + str(i + 1) + "," + str(rid) + ",'" + str(date) + "'," + str(score[i].get()) + ")")
				if comment[i].get():
					SQLfunc("INSERT INTO includes (itemnum,rid,idate,comment) VALUES (" + str(i + 1) + "," + str(rid) + ",'" + str(date) + "', '" + str(comment[i].get()) + "')")

			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Inspection Submitted")

class summarymonthyear:
	def __init__(self,master):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Year (YYYY)").grid()
		ttk.Label(self.window, text = "Month (MM)").grid(row = 1)
		
		bmonth = ttk.Entry(self.window)
		byear = ttk.Entry(self.window)

		bmonth.grid(row = 1, column = 1)
		byear.grid(row = 0, column = 1)

		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 2)
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(bmonth.get(), byear.get()))
		submit.grid(row = 2, column = 1)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitinfo(self,month,year):
		if not year or not year.isdigit() or int(year) < 1000 or int(year) > 9999:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid year in the form: YYYY")
		elif not month or not month.isdigit() or int(month) < 0 or int(month) > 12:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a month in the form: MM")
		else:
			self.window.destroy()
			self.window = ttk.Frame(self.master)

			ttk.Label(self.window, text = "Year (YYYY)").grid()
			ttk.Label(self.window, text = "Month(MM)").grid(row = 1)
			
			bmonth = ttk.Entry(self.window)
			byear = ttk.Entry(self.window)
			bmonth.grid(row = 1, column = 1)
			byear.grid(row = 0, column = 1)


			searchString = ("SELECT County,Cuisine,COUNT(*),COUNT(case A.passfail WHEN 'FAIL' THEN 1 ELSE NULL END) "
				"FROM (SELECT * FROM (inspection NATURAL JOIN restaurant) "
				"WHERE idate LIKE '"
				+ str(year) + "-")
			if len(month) == 1:
				searchString = searchString + "0" + str(month)
			else:
				searchString = searchString + str(month)
			searchString = searchString + "%') AS A GROUP BY County,Cuisine"
			results = SQLfunc(searchString)

			ttk.Label(self.window, text = "County").grid(row = 2)
			ttk.Label(self.window, text = "Cuisine").grid(row = 2, column = 1)
			ttk.Label(self.window, text = "Number of Restaurants Inspected").grid(row = 2, column = 2)
			ttk.Label(self.window, text = "Number of Restaurants Failed").grid(row = 2, column = 3)

			counties = SQLfunc("SELECT DISTINCT County FROM restaurant GROUP BY County")
			cuisines = SQLfunc("SELECT cuisine FROM cuisines")

			offset = 3
			inspectedcount = 0
			failedcount = 0
			inspectedcounttotal = 0
			failedcounttotal = 0
			found = False
			for i in range(len(counties)):
				for j in range(len(cuisines)):
					ttk.Label(self.window, text = str(counties[i])).grid(row = offset + j + i * len(cuisines), column = 0)
					ttk.Label(self.window, text = str(cuisines[j])).grid(row = offset + j + i * len(cuisines), column = 1)
					for k in range(len(results) / 4):
						if((results[4 * k] == counties[i]) and (results[4 * k + 1] == cuisines[j])):
							ttk.Label(self.window, text = str(results[4 * k + 2])).grid(row = offset + j + i * len(cuisines), column = 2)
							ttk.Label(self.window, text = str(results[4 * k + 3])).grid(row = offset + j + i * len(cuisines), column = 3)
							inspectedcount = inspectedcount + results[4 * k + 2]
							failedcount = failedcount + results[4 * k + 3]
							inspectedcounttotal = inspectedcounttotal + results[4 * k + 2]
							failedcounttotal = failedcounttotal + results[4 * k + 3]
							found = True
					if not found:
						ttk.Label(self.window, text = "0").grid(row = offset + j + i * len(cuisines), column = 2)
						ttk.Label(self.window, text = "0").grid(row = offset + j + i * len(cuisines), column = 3)
					found = False	
				offset = offset + 1
				ttk.Label(self.window, text = "Sub Total").grid(row = offset + j + i * len(cuisines), column = 1)
				ttk.Label(self.window, text = str(inspectedcount)).grid(row = offset + j + i * len(cuisines), column = 2)
				ttk.Label(self.window, text = str(failedcount)).grid(row = offset + j + i * len(cuisines), column = 3)
				inspectedcount = 0
				failedcount = 0
			ttk.Label(self.window, text = "Grand Total").grid(row = offset + (len(counties) * len(cuisines)), column = 0)
			ttk.Label(self.window, text = str(inspectedcounttotal)).grid(row = offset + (len(counties) * len(cuisines)), column = 2)
			ttk.Label(self.window, text = str(failedcounttotal)).grid(row = offset + (len(counties) * len(cuisines)), column = 3)

			cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
			cancel.grid(row = 1 + offset + (len(counties)) * len(cuisines))
			submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(bmonth.get(), byear.get()))
			submit.grid(row = 1 + offset + (len(counties)) * len(cuisines), column = 3)
			self.window.pack()

class summarycountyyear:
	def __init__(self,master):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Year").grid(row = 0, column = 0)
		ttk.Label(self.window, text = "County").grid(row = 1, column = 0)
		
		byear = ttk.Entry(self.window)
		byear.grid(row = 0, column = 1)

		counties = SQLfunc("SELECT DISTINCT County FROM restaurant")
		countySelect = StringVar(self.window)
		countySelect.set(counties[0])
		apply(OptionMenu, (self.window, countySelect) + tuple(counties)).grid(row = 1, column = 1)

		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 2, column = 0)
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(byear.get(), countySelect.get()))
		submit.grid(row = 2, column = 1)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitinfo(self,year,county):
		if not year or not year.isdigit() or int(year) < 1000 or int(year) > 9999:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid year in the form: YYYY")
		else:
			self.window.destroy()
			self.window = ttk.Frame(self.master)

			ttk.Label(self.window, text = "Year").grid(row = 0, column = 0)
			ttk.Label(self.window, text = "County").grid(row = 1, column = 0)
			
			byear = ttk.Entry(self.window)
			byear.grid(row = 0, column = 1)

			counties = SQLfunc("SELECT DISTINCT County FROM restaurant")
			countySelect = StringVar(self.window)
			countySelect.set(counties[0])
			apply(OptionMenu, (self.window, countySelect) + tuple(counties)).grid(row = 1, column = 1)

			searchString = ("SELECT MONTH(idate),COUNT(*) FROM (inspection NATURAL JOIN restaurant) WHERE YEAR(idate) = "
			+ str(year) + " AND County = "
			+ "'" + str(county) + "' GROUP BY MONTH(idate)")
			results = SQLfunc(searchString)

			months = ['January',
			'February',
			'March',
			'April',
			'May',
			'June',
			'July',
			'August',
			'September',
			'October',
			'November',
			'December']

			ttk.Label(self.window, text = "Month").grid(row = 2)
			ttk.Label(self.window, text = "Restaurants Inspected").grid(row = 2, column = 1)

			found = False
			count = 0
			for i in range(1,12):
				ttk.Label(self.window, text = months[i-1]).grid(row = i + 2, column = 0)
				for k in range(len(results) / 2):
					if(results[2 * k] == i):
						ttk.Label(self.window, text = results[2 * k + 1]).grid(row = i + 2, column = 1)
						count = count + results[2 * k + 1]
						found = True
				if not found:
					ttk.Label(self.window, text = "0").grid(row = i + 2, column = 1)
				found = False

			ttk.Label(self.window, text = "Grand Total").grid(row = 15, column = 0)
			ttk.Label(self.window, text = str(count)).grid(row = 15, column = 1)

			cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
			cancel.grid(row = 16, column = 0)
			submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(byear.get(), countySelect.get()))
			submit.grid(row = 16, column = 1)

			self.window.pack()

class summarytop:
	def __init__(self,master):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Year").grid(row = 0, column = 0)
		ttk.Label(self.window, text = "County").grid(row = 1, column = 0)

		byear = ttk.Entry(self.window)
		byear.grid(row = 0, column = 1)

		counties = SQLfunc("SELECT DISTINCT County FROM restaurant")
		countySelect = StringVar(self.window)
		countySelect.set(counties[0])
		apply(OptionMenu, (self.window, countySelect) + tuple(counties)).grid(row = 1, column = 1)

		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 2, column = 0)
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(byear.get(), countySelect.get()))
		submit.grid(row = 2, column = 1)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitinfo(self,year,county):
		if not year or not year.isdigit() or int(year) < 1000 or int(year) > 9999:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid year in the form: YYYY")
		else:
			self.window.destroy()
			self.window = ttk.Frame(self.master)

			ttk.Label(self.window, text = "Year").grid(row = 0, column = 0)
			ttk.Label(self.window, text = "County").grid(row = 1, column = 0)
			
			byear = ttk.Entry(self.window)
			byear.grid(row = 0, column = 1)

			counties = SQLfunc("SELECT DISTINCT County FROM restaurant")
			countySelect = StringVar(self.window)
			countySelect.set(counties[0])
			apply(OptionMenu, (self.window, countySelect) + tuple(counties)).grid(row = 1, column = 1)

			searchString = ("SELECT Cuisine,name,street,city,state,zipcode,MAX(totalscore) FROM restaurant AS R NATURAL JOIN "
				"(SELECT * FROM inspection WHERE YEAR(idate) = "
				+ str(year) + ") AS I WHERE County = "
				+ "'" + county + "' GROUP BY Cuisine")
			results = SQLfunc(searchString)

			if len(results) is 0:
				ttk.Label(self.window, text = "No results found!").grid(row = 2, column = 0, columnspan = 2)

				cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
				cancel.grid(row = 3, column = 0)
				submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(byear.get(), countySelect.get()))
				submit.grid(row = 3, column = 1)

			else:
				ttk.Label(self.window, text = "Cuisine").grid(row = 2, column = 0)
				ttk.Label(self.window, text = "Restaurant Name").grid(row = 2, column = 1)
				ttk.Label(self.window, text = "Address").grid(row = 2, column = 2)
				ttk.Label(self.window, text = "Inspection Score").grid(row = 2, column = 3)

				for i in range (len(results) / 7):
					Label(self.window, text = results[0 + i * 7]).grid(row = i + 3, column = 0)
					Label(self.window, text = results[1 + i * 7]).grid(row = i + 3, column = 1)
					Label(self.window, text = results[2 + i * 7] + ", " + results[3 + i * 7] + ", " + results[4 + i * 7] + " " + str(results[5 + i * 7])).grid(row = i + 3, column = 2)
					Label(self.window, text = results[6 + i * 7]).grid(row = i + 3, column = 3)

				cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
				cancel.grid(row = 4 + (len(results) / 7), column = 0)
				submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(byear.get(), countySelect.get()))
				submit.grid(row = 4 + (len(results) / 7), column = 3)

			self.window.pack()

class summarycomplaints:
	def __init__(self,master):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Year").grid(row = 0, column = 0)
		ttk.Label(self.window, text = "Min Number of Complaints").grid(row = 1, column = 0)
		ttk.Label(self.window, text = "Max Score").grid(row = 2, column = 0)

		byear = ttk.Entry(self.window)
		bcomplaints = ttk.Entry(self.window)
		bscore = ttk.Entry(self.window)
		byear.grid(row = 0, column = 1)
		bcomplaints.grid(row = 1, column = 1)
		bscore.grid(row = 2, column = 1)

		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 3, column = 0)
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(byear.get(), bcomplaints.get(), bscore.get()))
		submit.grid(row = 3, column = 1)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitinfo(self,year,complaints,score):
		if not year or not year.isdigit or int(year) < 1000 or int(year) > 9999:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid year in the form: YYYY")
		elif not complaints or not complaints.isdigit() or int(complaints) < 0:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid minimum number of complaints")
		elif not score or not score.isdigit() or int(score) < 0 or int(score) > 100:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow,"Please enter a valid max score")	
		else:
			self.window.destroy()
			self.window = ttk.Frame(self.master)

			ttk.Label(self.window, text = "Year").grid(row = 0, column = 0)
			ttk.Label(self.window, text = "Min Number of Complaints").grid(row = 1, column = 0)
			ttk.Label(self.window, text = "Max Score").grid(row = 2, column = 0)

			byear = ttk.Entry(self.window)
			bcomplaints = ttk.Entry(self.window)
			bscore = ttk.Entry(self.window)
			byear.grid(row = 0, column = 1)
			bcomplaints.grid(row = 1, column = 1)
			bscore.grid(row = 2, column = 1)

			searchString = ("SELECT distinct rid "
							"FROM ("
									"SELECT * "
									"FROM ("
											"SELECT * "
											"FROM ("
													"select rid, COUNT(*) AS A "
													"FROM complaint "
													"GROUP BY rid"
													") AS complaintcount "
											"WHERE A >= " + str(complaints)	+
										") AS B "
									"NATURAL JOIN complaint"
								") AS C "
								"NATURAL JOIN ("
												"SELECT rid, MAX(idate) AS idate, totalscore "
												"FROM ("
														"SELECT rid, MAX(idate) AS idate, totalscore "
														"FROM inspection "
														"WHERE totalscore <= " + str(score)	+
														" AND year(idate) = " + str(year) +
														" GROUP BY rid"
													") AS D "
												"NATURAL JOIN ("
																"SELECT rid, idate "
																"FROM (item NATURAL JOIN contains) "
																"WHERE critical = 'Y' AND score < 9 AND year(idate) = " + str(year) +
																" GROUP BY rid, idate"
															") AS E "
												"GROUP BY rid"
											") AS F")

			results = SQLfunc(searchString)

			rowcount = 3
			for i in range(len(results)):
				Label(self.window, text = "Restaurant Name").grid(row = rowcount, column = 0)
				Label(self.window, text = "Address").grid(row = rowcount, column = 1)
				Label(self.window, text = "Restaurant Operator").grid(row = rowcount, column = 2)
				Label(self.window, text = "Operator Email").grid(row = rowcount, column = 3)
				Label(self.window, text = "Score").grid(row = rowcount, column = 4)
				Label(self.window, text = "Complaints").grid(row = rowcount, column = 5)
				rowcount = rowcount + 1
				restaurant = SQLfunc("SELECT DISTINCT name,street,city,state,zipcode,firstname,lastname,email,totalscore FROM (SELECT rid,name,street,city,state,zipcode,MAX(idate),email,totalscore FROM restaurant NATURAL JOIN inspection GROUP BY rid) AS A NATURAL JOIN (SELECT * FROM registereduser NATURAL JOIN operatorowner) AS B where rid = " + str(results[i]))

				Label(self.window, text = restaurant[0]).grid(row = rowcount, column = 0)
				Label(self.window, text = restaurant[1] + ", " + restaurant[2] + ", " + restaurant[3] + " " + str(restaurant[4])).grid(row = rowcount, column = 1)
				Label(self.window, text = restaurant[5] + " " + restaurant[6]).grid(row = rowcount, column = 2)
				Label(self.window, text = restaurant[7]).grid(row = rowcount, column = 3)
				Label(self.window, text = restaurant[8]).grid(row = rowcount, column = 4)

				complaints = SQLfunc("select description FROM complaint WHERE rid = " + str(results[i]) + " AND year(cdate) = " + str(year))
				Label(self.window, text = str(len(complaints))).grid(row = rowcount, column = 5)
				Label(self.window, text = "Customer Complaints").grid(row = rowcount + 1, column = 0, columnspan = 5, sticky = "W")
				rowcount = rowcount + 2
				for j in range(len(complaints)):
					Label(self.window, text = complaints[j]).grid(row = rowcount, column = 0, columnspan = 5, sticky = "W")
					rowcount = rowcount + 1

			if len(results) is 0:
				Label(self.window, text = "No results!").grid(row=rowcount, column=0, columnspan=2)
				rowcount += 1

			cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
			cancel.grid(row = rowcount, column = 0)
			submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(byear.get(), bcomplaints.get(), bscore.get()))
			submit.grid(row = rowcount, column = 1)

			self.window.pack()

class textwindow:
	def __init__(self,master,txt):
		self.master = master
		self.frame = ttk.Frame(self.master)
		Label(self.frame, text = txt).grid(row = 0)
		OK = Button(self.frame, text = "OK", command = self.close)
		OK.grid(row = 1)
		self.frame.pack()

	def close(self):
		self.master.destroy()

if __name__ == "__main__":
	app = App()
	app.title("Georgia Restaurant Inspection")
	app.mainloop()
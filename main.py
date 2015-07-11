from Tkinter import *
import Tkinter as ttk
from sql import *

class App(ttk.Tk):
	def __init__(self, *args):
		ttk.Tk.__init__(self, *args)

		container = ttk.Frame(self)

		container.pack(side = "top", fill = "both", expand = True)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}
		for F in (loginScreen, guestwindow, guestsearch, guestcomplaint):
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

class RestaurantSearch:
	def __init__(self):
		self.results = None

	def doSearch(self, name, score, lg, zip, cuisine):
		#NEED TO ADD: The actual search query and pass it to restaurantsearch
		searchString = "SELECT name, street, city, state, zipcode, cuisine, totalscore, idate FROM (restaurant JOIN inspection ON restaurant.rid=inspection.rid) WHERE ("
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
		if cuisine:
			if needand:
				searchString = searchString + " AND "
			searchString = searchString + "cuisine = '" + cuisine + "'"
		searchString = searchString + ')'
		searchResult = SQLfunc(searchString)
		self.setResults(searchResult)

	def setResults(self, results):
		self.results = results

	def getResults(self):
		return self.results
restaurantSearch = RestaurantSearch()

class loginScreen(ttk.Frame):
	def __init__(self, master, controller):
		ttk.Frame.__init__(self, master)
		controller.resizeWindow("320x150+0+0")
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
		MainLog = Button(self, text = "Login", command = lambda: self.openRohiWindow(username.get(),password.get()))
		MainLog.grid(row = 6, column = 1)
		self.pack()

	def openRohiWindow(self,username,password):
		if not SQLfunc("SELECT * FROM registereduser WHERE username = " + "'" + username + "'"):
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow, "User not found, idiot")
		elif not SQLfunc("SELECT * FROM registereduser WHERE username = " + "'" + username + "' AND password = " + "'" + password + "'"):
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow, "Incorrect password, idiot")
		elif SQLfunc("SELECT * FROM operatorowner WHERE username = " + "'" + username + "'"):
			email = SQLfunc("SELECT email FROM operatorowner WHERE username = " + "'" + username + "'")
			email = email[0]
			self.newWindow = ttk.Toplevel(self.master)
			self.app = ownerwindow(self.newWindow,email)

class guestwindow(ttk.Frame):
	def __init__(self, master, controller):
		ttk.Frame.__init__(self, master)
		controller.resizeWindow("320x150+0+0")

		title = ttk.Label(self, text = "Guest GA Restaurant Health Inspections").grid(row = 0, columnspan = 2)
		search = ttk.Button(self, text = "Search for Restaurant", command = lambda: controller.show_frame(guestsearch))
		complaint = ttk.Button(self, text = "File a complaint", command = lambda: controller.show_frame(guestcomplaint))
		back = ttk.Button(self, text = "Back to Login Screen", command = lambda: controller.show_frame(loginScreen))
		search.grid(row = 1, column = 0)
		complaint.grid(row = 1, column = 1)
		back.grid(row = 2, columnspan = 2)
		self.pack()

class guestsearch(ttk.Frame):
	def __init__(self, master, controller):
		ttk.Frame.__init__(self, master)
		controller.resizeWindow("320x150+0+0")

		ttk.Label(self, text = "Restaurant Search").grid(row = 0, columnspan = 2)
		ttk.Label(self, text = "Name").grid(row = 1)
		ttk.Label(self, text = "Score*").grid(row = 2)
		ttk.Label(self, text = "Zipcode*").grid(row = 3)
		ttk.Label(self, text = "Cuisine").grid(row = 4)

		name = Entry(self)
		score = Entry(self)
		zipcode = Entry(self)
		name.grid(row = 1, column = 1)
		score.grid(row = 2, column = 1)
		zipcode.grid(row = 3, column = 1)

		lessgreater = [
			">",
			"<"
		]

		lgvariable = StringVar(self)
		lgvariable.set(lessgreater[0])
		apply(OptionMenu, (self, lgvariable) + tuple(lessgreater)).grid(row = 2, column = 2)

		cuisines = SQLfunc("SELECT cuisine FROM cuisines")
		cuisineSelect = StringVar(self)
		cuisineSelect.set(cuisines[0])
		apply(OptionMenu, (self, cuisineSelect) + tuple(cuisines)).grid(row = 4, column = 1)

		cancel = ttk.Button(self, text = "Go Back", command = lambda: controller.show_frame(guestwindow))
		cancel.grid(row = 5)

		submit = ttk.Button(self, text = "Submit", command = lambda: self.doSearchAndDisplay(controller, name.get(), score.get(), lgvariable.get(), zipcode.get(), cuisineSelect.get()))
		submit.grid(row = 5, column = 1)
		self.pack()

	def doSearchAndDisplay(self, controller, name, score, lg, zip, cuisine):
		restaurantSearch.doSearch(name, score, lg, zip, cuisine)
		self.newWindow = ttk.Toplevel(self.master)
		self.app = restaurantSearchRes(self.newWindow)

class restaurantSearchRes:
	def __init__(self, master):
		self.master = master
		self.frame = ttk.Frame(self.master)

		searchResult = restaurantSearch.getResults()

		if (searchResult != None):
			Label(self.frame, text = "Restaurant").grid(row = 0)
			Label(self.frame, text = "Address").grid(row = 0, column = 1)
			Label(self.frame, text = "Cuisine").grid(row = 0, column = 2)
			Label(self.frame, text = "Last Inspection Score").grid(row = 0, column = 3)
			Label(self.frame, text = "Date of Last Inspection").grid(row = 0, column = 4)

			for i in range (len(searchResult) / 8):
				Label(self.frame, text = searchResult[0 + i * 8]).grid(row = i + 1)
				Label(self.frame, text = searchResult[1 + i * 8] + ", " + searchResult[2 + i * 8] + ", " + searchResult[3 + i * 8] + " " + str(searchResult[4 + i * 8])).grid(row = i + 1, column = 1)
				#Label(self.frame, text = searchResult[1 + i * 8] + ", " + searchResult[2 + i * 8] + ", " + searchResult [3 + i * 8]).grid(row = i + 1, column = 1)
				Label(self.frame, text = searchResult[5 + i * 8]).grid(row = i + 1, column = 2)
				Label(self.frame, text = str(searchResult[6 + i * 8])).grid(row = i + 1, column = 3)
				Label(self.frame, text = str(searchResult[7 + i * 8])).grid(row = i + 1, column = 4)

			#NEED TO ADD: Actually displaying the restaurants
		self.frame.pack()

class guestcomplaint(ttk.Frame):
	def __init__(self, master, controller):
		ttk.Frame.__init__(self, master)
		controller.resizeWindow("335x180+0+0")

		Label(self, text = "Restaurant").grid(row = 0, column = 0)
		restaurants = SQLfunc('SELECT name FROM restaurant')

		restaurantSelect = StringVar(self)
		restaurantSelect.set(restaurants[0])
		apply(OptionMenu, (self, restaurantSelect) + tuple(restaurants)).grid(row = 0, column = 1)

		Label(self, text = "Date of Meal (YYYY-MM-DD)").grid(row = 2)
		Label(self, text = "First Name").grid(row = 3, column = 0)
		Label(self, text = "Last Name").grid(row = 4, column = 0)
		Label(self, text = "Phone #").grid(row = 5, column = 0)
		Label(self, text = "Complaint Description").grid(row = 6, column = 0)

		date = Entry(self)
		first = Entry(self)
		last = Entry(self)
		phone = Entry(self)
		description = Entry(self)
		date.grid(row = 2, column = 1)
		first.grid(row = 3, column = 1)
		last.grid(row = 4, column = 1)
		phone.grid(row = 5, column = 1)
		description.grid(row = 6, column = 1)

		cancel = Button(self, text = "Cancel", command = lambda: controller.show_frame(guestwindow))
		cancel.grid(row = 7, column = 0)

		submit = Button(self, text = "Submit", command = lambda: self.submitComplaint(date.get(),first.get(),last.get(),phone.get(),description.get(),restaurantSelect.get()))
		submit.grid(row = 7, column = 1)
		self.pack()

	def close(self):
		master.destroy()

	def submitComplaint(self,date,first,last,phone,description,restaurant):
		if not SQLfunc("SELECT phone FROM customer WHERE phone = " + "'" + phone + "';"):
			SQLfunc("INSERT INTO customer (phone, firstname, lastname) VALUES (" + "'" + phone + "', '" + first + "', '" + last + "')")
		RestID = SQLfunc("SELECT rid FROM restaurant WHERE name = " + "'" + restaurant + "'")
		SQLfunc("INSERT INTO complaint (cdate, rid, phone, description) VALUES (" + "'" + date + "', " + str(RestID[0]) + ", '" + phone + "', '" + description + "')")

class ownerwindow:
	def __init__(self,master,email):
		self.master = master
		self.window = ttk.Frame(self.master)
		search = ttk.Button(self.window, text = "Enter information about a restaurant", command = lambda: self.openrestrauntinfo(email))
		complaint = ttk.Button(self.window, text = "View health inspection reports", command = lambda: self.openinspectionreport(email))
		search.grid(row = 0)
		complaint.grid(row = 0, column = 1)
		self.window.pack()

	def openrestrauntinfo(self,email):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = restrauntinfo(self.newWindow,email)

	def openinspectionreport(self,email):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = inspectionreportsrestaurant(self.newWindow,email)

class restrauntinfo:
	def __init__(self,master,email):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Enter All Information").grid(row = 0, columnspan = 4)
		ttk.Label(self.window, text = "Health Permit ID").grid(row = 1)
		ttk.Label(self.window, text = "Health Permit Expiration (YYYY-MM-DD)").grid(row = 1, column = 1)
		ttk.Label(self.window, text = "Cuisine").grid(row = 1, column = 4)

		permitid = ttk.Entry(self.window)
		permitexpdate = ttk.Entry(self.window)
		permitid.grid(row = 2, column = 0)
		permitexpdate.grid(row = 2, column = 1)

		cuisines = SQLfunc("SELECT cuisine FROM cuisines")
		cuisineSelect = StringVar(self.window)
		cuisineSelect.set(cuisines[0])
		apply(OptionMenu, (self.window, cuisineSelect) + tuple(cuisines)).grid(row = 2, column = 4)

		ttk.Label(self.window, text = " ").grid(row = 3)

		ttk.Label(self.window, text = "Restraunt Name").grid(row = 4)
		ttk.Label(self.window, text = "Street").grid(row = 4, column = 1)
		ttk.Label(self.window, text = "City").grid(row = 4, column = 2)
		ttk.Label(self.window, text = "State").grid(row = 4, column = 3)
		ttk.Label(self.window, text = "Zipcode").grid(row = 4, column = 4)
		ttk.Label(self.window, text = "County").grid(row = 4, column = 5)
		ttk.Label(self.window, text = "Phone").grid(row = 4, column = 6)

		name = ttk.Entry(self.window)
		street = ttk.Entry(self.window)
		city = ttk.Entry(self.window)
		state = ttk.Entry(self.window)
		zipcode = ttk.Entry(self.window)
		county = ttk.Entry(self.window)
		phone = ttk.Entry(self.window)
		name.grid(row = 5, column = 0)
		street.grid(row = 5, column = 1)
		city.grid(row = 5, column = 2)
		state.grid(row = 5, column = 3)
		zipcode.grid(row = 5, column = 4)
		county.grid(row = 5, column = 5)
		phone.grid(row = 5, column = 6)

		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 6)
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitinfo(permitid.get(), permitexpdate.get(), name.get(), street.get(), city.get(), state.get(), zipcode.get(), county.get(), phone.get(), cuisineSelect.get(), email))
		submit.grid(row = 6, column = 6)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitinfo(self,permitid,permitexpdate,name,street,city,state,zipcode,county,phone,cuisine,email):
		rid = SQLfunc("select MAX(rid) FROM restaurant")
		newrid = rid[0] + 1
#		print "INSERT INTO restaurant (rid, phone, name, street, city, state, zipcode, county, cuisine, email) VALUES (" + str(newrid) + ", '" + str(phone) + "', '" + str(name) + ", '" + str(street) + "', '" + str(city) + "', '" + str(state) + "', " + str(zipcode) + ", '" + str(county) + "', '" + str(cuisine) + "', '" + str(email) + "')"

		SQLfunc("INSERT INTO restaurant (rid, phone, name, street, city, state, zipcode, county, cuisine, email) VALUES (" + str(newrid) + ", '" + str(phone) + "', '" + str(name) + "', '" + str(street) + "', '" + str(city) + "', '" + str(state) + "', " + str(zipcode) + ", '" + str(county) + "', '" + str(cuisine) + "', '" + str(email) + "')")
		SQLfunc("INSERT INTO healthpermit (hpid, expirationdate, rid) VALUES (" + permitid + ", '" + permitexpdate + "', " + str(newrid) + ")")
		self.newWindow = ttk.Toplevel(self.master)
		self.app = textwindow(self.newWindow, "Info submitted. Idiot")

class inspectionreportsrestaurant:
	def __init__(self,master,email):
		self.master = master
		self.window = ttk.Frame(self.master)
		ttk.Label(self.window, text = "Select your restaurant").grid(row = 0, columnspan = 2)

		restaurants = SQLfunc("SELECT name FROM restaurant WHERE email = " + "'" + email + "'")

		restaurantSelect = StringVar(self.window)
		restaurantSelect.set(restaurants[0])
		apply(OptionMenu, (self.window, restaurantSelect) + tuple(restaurants)).grid(row = 1)

		cancel = ttk.Button(self.window, text = "Cancel", command = self.close)
		cancel.grid(row = 6)
		submit = ttk.Button(self.window, text = "Submit", command = lambda: self.submitrestaurant(restaurantSelect.get(), email))
		submit.grid(row = 6, column = 6)

		self.window.pack()

	def close(self):
		self.master.destroy()

	def submitrestaurant(self,restaurant,email):
		self.newWindow = ttk.Toplevel(self.master)
		RestID = SQLfunc("SELECT rid FROM restaurant WHERE name = " + "'" + restaurant + "'")
		RestID = str(RestID[0])
		self.app = inspectionreportsresult(self.newWindow,RestID,email)

class inspectionreportsresult:
	def __init__(self,master,RestID,email):
		self.master = master
		self.window = ttk.Frame(self.master)

		inspections = SQLfunc("SELECT idate, totalscore, passfail FROM inspection WHERE rid = " + RestID + " ORDER BY idate DESC LIMIT 2")

		ttk.Label(self.window, text = str(inspections[3])).grid(row = 0, column = 2)
		ttk.Label(self.window, text = str(inspections[0])).grid(row = 0, column = 3)

		ttk.Label(self.window, text = "Item Number").grid(row = 1)
		ttk.Label(self.window, text = "Item Description").grid(row = 1, column = 1)
		ttk.Label(self.window, text = "Score").grid(row = 1, column = 2)
		ttk.Label(self.window, text = "Score").grid(row = 1, column = 3)

		items = SQLfunc("SELECT itemnum, description FROM item")
		scores1 = SQLfunc("SELECT score FROM contains WHERE rid = " + RestID + " AND idate = " + "'" + str(inspections[3]) + "'")
		scores2 = SQLfunc("SELECT score FROM contains WHERE rid = " + RestID + " AND idate = " + "'" + str(inspections[0]) + "'")

		for i in range(len(items) / 2):
			ttk.Label(self.window, text = str(items[i * 2])).grid(row = 2 + i, column = 0)
			ttk.Label(self.window, text = str(items[i * 2 + 1])).grid(row = 2 + i, column = 1)
		for i in range(len(scores1)):
			ttk.Label(self.window, text = str(scores1[i])).grid(row = 2 + i, column = 2)
		for i in range(len(scores2)):
			ttk.Label(self.window, text = str(scores2[i])).grid(row = 2 + i, column = 3)

		ttk.Label(self.window, text = "TOTAL SCORE").grid(row = 17)
		ttk.Label(self.window, text = str(inspections[4])).grid(row = 17, column = 2)
		ttk.Label(self.window, text = str(inspections[1])).grid(row = 17, column = 3)

		ttk.Label(self.window, text = "PASS?").grid(row = 18)
		ttk.Label(self.window, text = str(inspections[5])).grid(row = 18, column = 2)
		ttk.Label(self.window, text = str(inspections[2])).grid(row = 18, column = 3)

		close = ttk.Button(self.window, text = "Close", command = self.close)
		close.grid(row = 19, column = 3)

		self.window.pack()

	def close(self):
		self.master.destroy()

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
	app.title("GEOWGIA RETRANT INSPERCTIN")
	app.mainloop()
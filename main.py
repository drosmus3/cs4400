from Tkinter import *
import Tkinter as ttk
from sql import *

class loginScreen:
	def __init__(self, master):
		self.master = master
		self.frame = ttk.Frame(self.master)
		Label(self.frame, text = "Guest").grid(row = 0)

		GuestLog = ttk.Button(self.frame, text = "Login", command = self.openGuestWindow)
		GuestLog.grid(row = 0, column = 1)

		ttk.Label(self.frame, text = "Restaurant Owner / Health Inspector Login").grid(row = 2, columnspan = 2, rowspan = 2)

		ttk.Label(self.frame, text = "Username").grid(row = 4)
		ttk.Label(self.frame, text = "Password").grid(row = 5)

		username = ttk.Entry(self.frame)
		password = ttk.Entry(self.frame)
		username.grid(row = 4, column = 1)
		password.grid(row = 5, column = 1)

		#MainLog = Button(root, text = "Login", command = self.openRohiWindow)
		MainLog = Button(self.frame, text = "Login")
		MainLog.grid(row = 6, column = 1)
		self.frame.pack()

	def openGuestWindow(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = guestwindow(self.newWindow)

class guestwindow:
	def __init__(self,master):
		self.master = master
		self.window = ttk.Frame(self.master)
		search = ttk.Button(self.window, text = "Search for Restaurant", command = self.openguestsearch)
		complaint = ttk.Button(self.window, text = "File a complaint", command = self.openguestcomplaint)
		search.grid(row = 0)
		complaint.grid(row = 0, column = 1)
		self.window.pack()

	def openguestsearch(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = guestsearch(self.newWindow)

	def openguestcomplaint(self):
		self.newWindow = ttk.Toplevel(self.master)
		self.app = guestcomplaint(self.newWindow)

class guestsearch:
	def __init__(self,master):
		self.master = master
		self.frame = ttk.Frame(self.master)
		ttk.Label(self.frame, text = "Restaurant Search").grid(row = 0, columnspan = 2)
		ttk.Label(self.frame, text = "Name").grid(row = 1)
		ttk.Label(self.frame, text = "Score").grid(row = 2)
		ttk.Label(self.frame, text = "Zipcode").grid(row = 3)
		ttk.Label(self.frame, text = "Cuisine").grid(row = 4)

		name = Entry(self.frame)
		score = Entry(self.frame)
		zipcode = Entry(self.frame)
		name.grid(row = 1, column = 1)
		score.grid(row = 2, column = 1)
		zipcode.grid(row = 3, column = 1)

		lessgreater = [
			">",
			"<"
		]

		lgvariable = StringVar(self.frame)
		lgvariable.set(lessgreater[0])
		apply(OptionMenu, (self.frame, lgvariable) + tuple(lessgreater)).grid(row = 2, column = 2)

		cuisines = SQLfunc("SELECT cuisine FROM cuisines")
		cuisineSelect = StringVar(self.frame)
		cuisineSelect.set(cuisines[0])
		apply(OptionMenu, (self.frame, cuisineSelect) + tuple(cuisines)).grid(row = 4, column = 1)

		cancel = ttk.Button(self.frame, text = "Cancel", command = self.close)
		cancel.grid(row = 5)

		submit = ttk.Button(self.frame, text = "Submit", command = lambda: self.openrestaurantsearch(name.get(),score.get(),lgvariable.get(),zipcode.get(),cuisineSelect.get()))
		submit.grid(row = 5, column = 1)
		self.frame.pack()

	def close(self):
		self.master.destroy()

	def openrestaurantsearch(self,name,score,lg,zip,cuisine):
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
		#print searchString
		searchResult = SQLfunc(searchString)
		#print searchResult
		if searchResult:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = restaurantsearch(self.newWindow, searchResult)
		else:
			self.newWindow = ttk.Toplevel(self.master)
			self.app = textwindow(self.newWindow, "No results")

class restaurantsearch():
	def __init__(self, master, searchResult):

		self.master = master
		self.frame = ttk.Frame(self.master)
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

class guestcomplaint:
	def __init__(self,master):
		self.master = master
		self.frame = ttk.Frame(self.master)
		Label(self.frame, text = "Restaurant").grid(row = 0)
		restaurants = SQLfunc('SELECT name FROM restaurant')

		restaurantSelect = StringVar(self.frame)
		restaurantSelect.set(restaurants[0])
		apply(OptionMenu, (self.frame, restaurantSelect) + tuple(restaurants)).grid(row = 1)

		Label(self.frame, text = "Date of Meal (YYYY-MM-DD)").grid(row = 3)
		Label(self.frame, text = "First Name").grid(row = 3, column = 1)
		Label(self.frame, text = "Last Name").grid(row = 3, column = 2)
		Label(self.frame, text = "Phone #").grid(row = 3, column = 3)
		Label(self.frame, text = "Complaint Description").grid(row = 3, column = 4)

		date = Entry(self.frame)
		first = Entry(self.frame)
		last = Entry(self.frame)
		phone = Entry(self.frame)
		description = Entry(self.frame)
		date.grid(row = 4)
		first.grid(row = 4, column = 1)
		last.grid(row = 4, column = 2)
		phone.grid(row = 4, column = 3)
		description.grid(row = 4, column = 4)

		cancel = Button(self.frame, text = "Cancel", command = self.close)
		cancel.grid(row = 5)

		submit = Button(self.frame, text = "Submit", command = lambda: self.submitComplaint(date.get(),first.get(),last.get(),phone.get(),description.get(),restaurantSelect.get()))
		submit.grid(row = 5, column = 4)
		self.frame.pack()

	def close(self):
		self.master.destroy()

	def submitComplaint(self,date,first,last,phone,description,restaurant):
		if not SQLfunc("SELECT phone FROM customer WHERE phone = " + "'" + phone + "';"):
			SQLfunc("INSERT INTO customer (phone, firstname, lastname) VALUES (" + "'" + phone + "', '" + first + "', '" + last + "')")
		RestID = SQLfunc("SELECT rid FROM restaurant WHERE name = " + "'" + restaurant + "'")
		SQLfunc("INSERT INTO complaint (cdate, rid, phone, description) VALUES (" + "'" + date + "', " + str(RestID[0]) + ", '" + phone + "', '" + description + "')")

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
	root = ttk.Tk()
	app = loginScreen(root)
	root.title("GEOWGIA RETRANT INSPERCTIN")
	root.mainloop()
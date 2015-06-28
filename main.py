from Tkinter import *
import Tkinter as ttk

class View(ttk.Frame):
	def __init__(self, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		Label(root, text = "Guest").grid(row = 0)

		GuestLog = Button(root, text = "Login", command = self.guestwindow)
		GuestLog.grid(row = 0, column = 1)

		Label(root, text = "Restraunt Owner / Health Inspector Login").grid(row = 2, columnspan = 2, rowspan = 2)

		Label(root, text = "Username").grid(row = 4)
		Label(root, text = "Password").grid(row = 5)

		username = Entry(root)
		password = Entry(root)
		username.grid(row = 4, column = 1)
		password.grid(row = 5, column = 1)

		MainLog = Button(root, text = "Login", command = self.rohiwindow)
		MainLog.grid(row = 6, column = 1)



	def guestwindow(self):
		window = ttk.Toplevel(self)		
		search = Button(window, text = "Search for Restraunt", command = self.guestsearch)
		complaint = Button(window, text = "File a complaint", command = self.guestcomplaint)
		search.grid(row = 0)
		complaint.grid(row = 0, column = 1)

	def guestsearch(self):
		window = ttk.Toplevel(self)
		Label(window, text = "Restraunt Search").grid(row = 0, columnspan = 2)
		Label(window, text = "Name").grid(row = 1)
		Label(window, text = "Score").grid(row = 2)
		Label(window, text = "Zipcode").grid(row = 3)
		Label(window, text = "Cuisine").grid(row = 4)

		name = Entry(window)
		score = Entry(window)
		zipcode = Entry(window)
		name.grid(row = 1, column = 1)
		score.grid(row = 2, column = 1)
		zipcode.grid(row = 3, column = 1)

		cuisines = [
			"butts",
			"dicks"
		]

		variable = StringVar(window)
		variable.set(cuisines[0])
		apply(OptionMenu, (window, variable) + tuple(cuisines)).grid(row = 4, column = 1)

		cancel = Button(window, text = "Cancel", command = self.quit)
		cancel.grid(row = 5)

		submit = Button(window, text = "Submit", command = self.searchwindow)
		submit.grid(row = 5, column = 1)

	def searchwindow(self):
		window = ttk.Toplevel(self)
		Label(window, text = "Restraunt").grid(row = 0)
		Label(window, text = "Address").grid(row = 0, column = 1)
		Label(window, text = "Cuisine").grid(row = 0, column = 2)
		Label(window, text = "Last Inspection Score").grid(row = 0, column = 3)
		Label(window, text = "Date of Last Inspection").grid(row = 0, column = 4)

	def guestcomplaint(self):
		window = ttk.Toplevel(self)
		

	def rohiwindow(self):
		window = ttk.Toplevel(self)
		Label(window, text = "test").grid(row = 0)

if __name__ == "__main__":
	root = ttk.Tk()
	view = View(root)
	root.title("GEOWGIA RETRANT INSPERCTIN")
	root.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from types import SimpleNamespace
import myfunc


class my_page:

	def __init__(self):

		# save file pdf
		def save_filePdf():
			list_files_to_save = []
			# get name of file fron text on the page
			MyFilePdf = text_name.get(1.0, "end-1c")
			if MyFilePdf == "":
				showinfo(title="Error", message="Empty name of file")
				return
			# read all selected file from self.tree to list
			rows = self.tree.get_children()
			for row in rows:
				row_value_dict = self.tree.item(row)
				row_value = SimpleNamespace(**row_value_dict)
				if row_value.tags[0] == "checked":
					list_files_to_save.append(row_value.values[0])
			# save
			PathNewFile = myfunc.save_filePdf(self.myFolder, MyFilePdf, list_files_to_save)
			# message for user
			if PathNewFile != None:
				showinfo(title="Result", message="New file " + PathNewFile)
			# clear all checkboxs
			rows = self.tree.get_children()
			for row in rows:
				self.tree.item(row,tags="unchecked")

		# change checkbox
		def toggleCheck(event):
			rowid = self.tree.identify_row(event.y)
			tag = self.tree.item(rowid, "tags")[0]
			tags = list(self.tree.item(rowid,"tags"))
			tags.remove(tag)	
			self.tree.item(rowid,tags =tags)	
			if tag == "checked":
				self.tree.item(rowid,tags="unchecked")
			else:
				self.tree.item(rowid,tags="checked")

		# open when Enter preview
		def open_image(event):
			for selected_item in self.tree.selection():
				item = self.tree.item(selected_item)
				image = Image.open(item["values"][0])
				image.show()

		# preview
		def preview(pathtofile):
			image = Image.open(pathtofile)
			koef = max(image.size[0]/500,image.size[1]/700)
			self.image = image.resize((int(image.size[0]/koef), int(image.size[1]/koef)), Image.Resampling.LANCZOS) 
			self.photo = ImageTk.PhotoImage(self.image)
			(iWidth, iHeight) = self.image.size
			image = self.canvas.create_image(0, 0, anchor='nw',image=self.photo)
			self.canvas.place(x=500, y=50)		
			# open when Enter preview
			self.canvas.tag_bind(image,"<Double-1>", open_image)
		
		# preview when selecting a file
		def item_selected(event):
			for selected_item in self.tree.selection():
				item = self.tree.item(selected_item)
				preview(item["values"][0])

		def create_table(myListFilesIpg):
			# heading
			self.tree.heading("#0", text="choice")
			self.tree.heading("#1", text="file jpg")
			# column (checkbox for choice and name of file)
			self.tree.column("#0", width = 50)
			self.tree.column("#1", width = 400)
			# fill out the table from
			for i in range(len(myListFilesIpg)):
				self.tree.insert("", END, values=[myListFilesIpg[i]],tags="unchecked")
			self.tree.place(x=10, y=50)
			scrollbar.place(x=460, y=50, height=685)
			# configure images for checkbox 
			self.style = ttk.Style(self.tree)
			self.style.configure("Treeview", rowheight=30)
			self.tree.tag_configure("checked", image=self.im_checked)
			self.tree.tag_configure("unchecked", image=self.im_unchecked)
			# configure scrollbar
			scrollbar.config(command=self.tree.yview)
			# preview when selecting a file
			self.tree.bind("<<TreeviewSelect>>", item_selected)
			# change checkbox when selecting a file
			self.tree.bind("<Double-1>", toggleCheck)

		# clear self.tree and window with preview
		def clear_tree():
			self.tree.delete(*self.tree.get_children())
			self.canvas.delete("all")

		def get_directory():
			# clear self.tree and window with preview
			clear_tree()
			# select directory
			self.myFolder = filedialog.askdirectory()
			# show directory on the page
			self.Label.config(text=self.myFolder)
			# get all files jpg to list
			myListFilesIpg = myfunc.find_files(self.myFolder)
			# show files in self.tree
			create_table(myListFilesIpg)

		# delete all jpg in directory
		def del_directory():
			if self.myFolder == "":
				return
			myfunc.del_filesJpg(self.myFolder)
			# show message for user
			showinfo(title="Result", message="Deleted all files jpg in " + self.myFolder)
			clear_tree()

		# variable for storing a directory with files 
		self.myFolder = ""

		# create page and elements on it using tkinter
		self.root = Tk()
		self.root.title("Save jpg to pdf")
		self.root.geometry("1100x800")
		self.root.iconbitmap(default="orca.ico")

		open_button = ttk.Button(text="Open directory", command=get_directory)
		open_button.place(x=10, y=10)

		self.Label = ttk.Label(text=self.myFolder)
		self.Label.place(x=100,y=15)

		# table with files in directory
		scrollbar = ttk.Scrollbar(self.root, orient="vertical")
		self.tree = ttk.Treeview(self.root,columns=(1),height=22, yscrollcommand=scrollbar.set)
		# preview of file
		self.canvas = Canvas(self.root, width = 500, height = 700)

		save_button = ttk.Button(text="Save file PDF", command=save_filePdf)
		save_button.place(x=500, y=10)
		
		# to insert name of new file pdf
		text_name = Text(self.root, height=1, width=35)
		text_name.place(x=600, y=12)
		text_name.insert(1.0, "MyFilePdf")

		delete_button = ttk.Button(text="Delete all jpg in directory ", command=del_directory)
		delete_button.place(x=950, y=10)

		# for checkboxs in self.tree
		self.im_checked = ImageTk.PhotoImage(Image.open(r".images\checked.png"))
		self.im_unchecked = ImageTk.PhotoImage(Image.open(r".images\unchecked.png"))

		# show page
		self.root.mainloop()

			
if __name__ == '__main__':
	app = my_page()


# TODO:

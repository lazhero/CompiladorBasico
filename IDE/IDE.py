from tkinter import *
from tkinter import filedialog
from tkinter import font
import subprocess

root = Tk()
root.title("Wage IDE")
# Add main.iconbitmap()
root.geometry("1200x660")

# Global variables
global open_file_name, selected
open_file_name, selected = False, False


# New file function
def new_file():
	# Delete previous text
	my_text.delete("1.0", END)
	# Update status bar
	root.title("New File - Wage IDE")
	status_bar.config(text="New file created        ")

	global open_file_name
	open_file_name = False

# Open file function
def open_file():
	# Grab filename
	text_file = filedialog.askopenfilename(initialdir="C:/", title="Open File", filetypes=(("Text Files", "*.txt"), ("Python Files", "*.py"), ("Wage Files", "*.wage"), ("All Files", "*.*")))

	# Check to see if there is a file name
	if text_file:
		global open_file_name
		open_file_name = text_file
		# Delete previous text
		my_text.delete("1.0", END)
		# Update status bar
		name = text_file
		status_bar.config(text="File opened        ")
		root.title(f'{name} - Wage IDE')
		# Open fle
		text_file = open(text_file, 'r')
		text = text_file.read()
		# Add file to text box
		my_text.insert(END, text)
		# Close the opened file
		text_file.close()

# Save as file function
def save_as_file():
	text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/", title="Save File", filetypes=(("Text Files", "*.txt"), ("Python Files", "*.py"), ("Wage Files", "*.wage"), ("All Files", "*.*")))
	name = text_file
	if text_file:
		# Save the file
		text_file = open(text_file, 'w')
		text_file.write(my_text.get(1.0, END))
		# Close the file
		text_file.close()
		# Update status bar
		status_bar.config(text="File saved        ")
		root.title(f'{name} - Wage IDE')

# Save file function
def save_file():
	global open_file_name
	if open_file_name:
		# Save the file
		text_file = open(open_file_name, 'w')
		text_file.write(my_text.get(1.0, END))
		# Close the file
		text_file.close()
		# Update status bar
		status_bar.config(text="File saved        ")
		root.title(f'{open_file_name} - Wage IDE')
	else:
		save_as_file()

def run_file():
	global open_file_name
	if open_file_name:
		command = f'python {open_file_name}'
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, error = process.communicate()
		code_output.insert('1.0', output)
		code_output.insert('1.0', error)
	else:
		open_file()

# Cut text function
def cut_text(e):
	global selected
	# Check to use if keyboard shortcut used
	if e:
		selected = root.clipboard_get()

	else:
		if my_text.selection_get():
			# Grap selected text from text box
			selected = my_text.selection_get()
			# Delete selected text from text box
			my_text.delete("sel.first", "sel.last")
			# Clear the clipboard the append
			root.clipboard_clear()
			root.clipboard_append(selected)

# Copy text function
def copy_text(e):
	global selected
	# Check to use if keyboard shortcut used
	if e:
		selected = root.clipboard_get()

	if my_text.selection_get():
		# Grap selected text from text box
		selected = my_text.selection_get()
		# Clear the clipboard the append
		root.clipboard_clear()
		root.clipboard_append(selected)

# Paste text function
def paste_text(e):
	global selected
	# Check to use if keyboard shortcut used
	if e:
		selected = root.clipboard_get()

	else:
		if selected:
			position = my_text.index(INSERT)
			my_text.insert(position, selected)


# Create main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create scrollbar for the text box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
my_text.pack()

# Configure scrollbar
text_scroll.config(command=my_text.yview)

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add file menu	
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut       Ctrl+X", command=lambda: cut_text(False))
edit_menu.add_command(label="Copy    Ctrl+C", command=lambda: copy_text(False))
edit_menu.add_command(label="Paste    Ctrl+V", command=lambda: paste_text(False))
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

# Add run menu
run_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Run", command=run_file)

# Add status bar to bottom of app
status_bar = Label(root, text="Ready        ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

#Edit bindings
root.bind('<Control-x>', cut_text)
root.bind('<Control-c>', copy_text)
root.bind('<Control-v>', paste_text)

code_output = Text(height=10)
code_output.pack()



root.mainloop()

#   usr/bin/env python
#------------------------------------------------------------------------------#
#       MODULE:         wikipdf.py
#       INFO:           Accesses a .txt file with each line being a title of    
#                       Wikipedia page you'd like to save a PDF of. It then
#                       downloads all the files, saving them with a nice file
#                       name into the folder that the .txt is already in
#       INSPIRATION:    Data hoarders have problems too.
#       CODED BY:       iivii   @odd_codes
#       EMAIL:          iiviigames@pm.me
#       WEBSITE:        https://odd.codes
#       LICENSE:        BUDDYPACT
#                       BORROW, USE, DONATE, DOWNLOAD!
#                       Your price? A courteous thanks.
#
#
#       Confused about that BUDDYPACT? Well, its simple. You can use my code
#       for anything at all, commercial, personal, erotic or, whatever. The
#       only thing you are required to do if you choose to use it, is to link
#       me to the thing you used it for, or shoot me an email to tell me what
#       you're working on, so I can see the cool shit you are doing, and see
#       the connections forming between disparate groups.
#
#       Maybe we can even get others to do this as well, and before you know it,
#       everybody is connected through collaborative frienships. That's the goal
#       of BUDDYPACT:
#                       Friendship Through Collaboration
#------------------------------------------------------------------------------#


#                                                                       IMPORTS
#_______________________________________________________________________________
from __future__ import print_function
import sys
import os
import requests
import os


#                                                                       GLOBALS
#_______________________________________________________________________________

#       Wikipedia API
BASEURL = "https://en.wikipedia.org/"
APIPDF = "api/rest_v1/page/pdf/"

#       Folders for quick selection during the pathing process.
#       These can be changed to whatever you want, and then quickly
#       selected when prompted, rather than having to type a path
#       every time.
CALLDIR = os.getcwd()
DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
DOCUMENTS = os.path.join(os.path.join(os.path.expanduser('~')), 'Documents')
DOWNLOADS = os.path.join(os.path.join(os.path.expanduser('~')), 'Downloads')
CURRENT = CALLDIR + " (The Current Directory)"
CUSTOM = "Enter a custom directory"

USUAL = [DESKTOP, DOCUMENTS, DOWNLOADS, CURRENT, CUSTOM]


#       Color functions.
ATTRIBUTES = dict(list(zip(['bold','dark','','underline','blink','','reverse','concealed'],list(range(1, 9)))))
del ATTRIBUTES['']
HIGHLIGHTS = dict(list(zip(['_grey','_red','_green','_yellow','_blue','_magenta','_cyan','_white'],list(range(40, 48)))))
COLORS = dict(list(zip(['grey','red','green','yellow','blue','magenta','cyan','white',],list(range(30, 38)))))
RESET = '\033[0m'
#                                                                       FUNCTIONS
#________________________________________________________________________________


#       Alter a single string
def fix_string(words, spacer=" ", replacer=" ", addto=""):
	"""
Fixes a string by removing certain characters and swapping them out for new ones.
	"""
	fixed = words.replace(spacer, replacer)
	fixed += addto
	return fixed


#       Alter a list of strings
def fix_string_list(wordlist, spacer=" ", replacer=" ", addto=""):
	"""
As fix string, however, does this with all items in a list.
	"""
	formatted_list = []
	for i in range(len(wordlist)):
		entry = wordlist[i]
		entry_fixed = entry.replace(spacer,replacer)
		entry_fixed += addto
		formatted_list.append(entry_fixed)

	return formatted_list


#       User input.
def get_data_from(line,color="grey"):
	"""
Retrieves input from a user.
	"""
	msg = line
	msglen = len(msg)
	prompt = "\n::: "
	line = "_" * msglen
	cprint(msg,color)
	res = input(prompt)
	cprint(line + "\r", "cyan", None, ["underline", "concealed"])
	return res

	
#       Colorizer for the terminal
def colored(text, color=None, on_color=None, attrs=None):
	"""
The workhorse that cprint calls upon.
Example:
	colored('Holy Baboons Ass, Robin!, 'grey', '_red', ['blue', 'blink'])
	colored('Napster was an inside job!', 'green', on_color=None, attrs=["bold"])
	"""
	if os.getenv('ANSI_COLORS_DISABLED') is None:
		fmt_str = '\033[%dm%s'
		if color is not None:
			text = fmt_str % (COLORS[color], text)

		if on_color is not None:
			text = fmt_str % (HIGHLIGHTS[on_color], text)

		if attrs is not None:
			for attr in attrs:
				text = fmt_str % (ATTRIBUTES[attr], text)

		text += RESET
		
	return text


#       The easy-bake color print function
def cprint(text, color=None, on_color=None, attrs=None, **kwargs):
	"""
Colored printing in the terminal!
FG:     red, green, yellow, blue, magenta, cyan, white
BG:     _red, _green, _yellow, _blue, _magenta, _cyan, _white
STYLES: bold, dark, underline, blink, reverse, concealed, or any color name!
	"""

	print((colored(text, color, on_color, attrs)), **kwargs)


#       Directory Changing
def dshift():
		print("Enter the associated number to switch to that directory")
		count = 0
		tc = "n"
		bc = ""
		# The color values for printing on console.
		# Change these as you want! Check the cprint function for more
		# information on how these are formatted.
		for entry in USUAL:
				count+=1
				if count == 1:
						tc = "magenta"
						bc = "_grey"
				elif count == 2:
						tc = "green"
						bc = "_grey"
				elif count == 3:
						tc = "red"
						bc = "_grey"
				elif count == 4:
						tc = "cyan"
						bc = "_grey"
				elif count == 5:
						tc = "yellow"
						bc = "_grey"

				cprint(str(count) + ".) " + entry, tc, bc)
	
		cprint("---------------------------------------------------", "cyan", "_grey", ["underline"])
		response = get_data_from("Please type out your choice, and press ENTER")
		if not response in ['1','2','3','4','5']:
				cprint("INVALID ENTRY. EXITING...","blue", "_red")
				raise(sys.exit())
		else:
		# This is where you could add more options for folders you tend to
		# download to.
				if response == '1':
						return DESKTOP
				elif response == '2':
						return DOCUMENTS
				elif response == '3':
						return DOWNLOADS
				elif response == '4':
						return os.curdir
				else:
						return response
		

def get_txt_list():
	"""
This function is responsible for moving to the directory where the 
text file containing the desired wikipedia pages to download is 
located.

It will only seek out text files and has preventative measures to 
ensure no errors will occur if the user types in a directory wrong,
or a file name wrong.

Once the user selects the directory and the file containing the 
list of wikipedia entries, the file is parsed, and passed to the
download function.
	"""
	directory = dshift()
	if directory == "5":        
		directory = get_data_from("Enter the directory to use:", "magenta")
		# Attempt a directory shift to the entered drive point; exit on failure.
		try:
			os.chdir(directory)
		except FileNotFoundError:
			cprint("No directory exists in the provided location.", "red")
			raise(sys.exit())
		
		except OSError:
                        cprint("Nothing entered; so the current directory will be checked!", "magenta", None, ["underline"])
                        directory = os.curdir
                        try:
                                os.chdir(directory)
                        except FileNotFoundError:
                                cprint("Sorry, no valid files in the current directory.\nEXITING!", "red", None, ["dark"])
                                raise(sys.exit())

	# Store all the files in the final directory and create an empty list.
	dirlist = os.listdir(directory)
	txtlist = []

	# Any files ending with the .txt extension will register and append
	# into the txtlist. This is to ensure that the program doesn't attempt
	# to read from other file types based on a user mis-input.
	for i in range(len(dirlist)):
		if str(dirlist[i]).endswith(".txt"):
			txtlist.append(str(dirlist[i]))

	# If after looping there exists no files in the txtlist, this means that
	# no .txt files exist in that directory, and the program exits.
	if len(txtlist) < 1:
		cprint("No .txt files in this directory\nExiting!", "red", None, ["underline"])
		raise(sys.exit())

	# Notify user that they should enter the name of the text file (since
	# it's possible there's more than one in the directory) that they want
	# to parse from. 
	cprint("Please enter one of the following file names to use as the reference:", "green")
	cprint("NOTE: Do not enter .txt to the end of the filename!\n","yellow",None,["underline","bold"])

	# Create a list that will contain the files without their '.txt'
	# extension. This is unnecessary really, and just my preference to
	# not have to type '.txt' every time I want to use this. This would
	# need to be changed (rather easily, too) in order to read other
	# file types.
	striplist = []
	for i in range(len(txtlist)):
		striplist.append(txtlist[i].replace(".txt",""))

	# Output all the file names with their extensions stripped out.
	for i in striplist:
		print(i)
	fname = get_data_from("Enter the name of the .txt file to retrieve page names from:")

	# Error catching for bad entries.
	for i in range(len(striplist)):
		if fname == striplist[i]:
			fname += ".txt"
			break
		elif i == len(striplist) - 1:
			cprint("Entered an invalid filename.\nExiting!","red", None, ["underline", "bold"])
			raise(sys.exit())
			
	# FINALLY! A successful attempt to find a text file and parse it.
	print("Success!\nReading from: " + fname)
	
	# Now, actually parse the lines and prepare them for their insertion
	# into the wikipedia API and eventually, their file names as PDFs.
	text_list = []
	with open(fname, 'r') as text_file:
		file_contents = text_file.readlines()
		for line in file_contents:
			#   Remove the linebreaks at the end of each line
			line_current = line.replace("\n","")
			#   Append the formatted line to an entry in text_list
			text_list.append(line_current)
	
	#   FORMAT text_list INTO PROPER REQUEST FORMAT
	api_titles = fix_string_list(text_list, " ", "_")
	
	#   RETURN LIST FOR REQUESTING
	return api_titles


def download_pdfs(api_list):
	"""
This function is called once a text file has been parsed and passed to it as
a list; entries already formatted for the requests.

For every entry in the .txt file, a call to wikipedia is made, and if that page
exists, it will be downloaded into the desired destination as a PDF.

Works like a fucking charm!
	"""
	addresses = []
	for i in range(len(api_list)):
		title = api_list[i]
		address = BASEURL + APIPDF + title
		addresses.append(address)

	#   Request PDF information from wikipedia.
	for i in range(len(addresses)):
		#   Use the name that was appeneded to the address list
		out_file_name = api_list[i]+".pdf"
		#   Notify the user of the file downloading and what its name will be
		cprint("Downloading: %s" % out_file_name, "blue", "_grey")

		#   Response from server
		r = requests.get(addresses[i], stream=True)

		#   Write the file to PDF in Chunks
		with open(out_file_name, 'wb') as pdf:
			for chunk in r.iter_content(chunk_size=4096):
				if chunk:
					pdf.write(chunk)

		#   Notify user that the file has successfully downloaded.
		cprint("%s downloaded!\n" % out_file_name, "green", "_grey", ["dark", "blink"])

	#   Completed Downloads List!
	cprint("DOWNLOADED ALL FILES!", "blue", "_yellow", ["underline"])
	raise(sys.exit())


#                                                                       MAINLOOP
#_______________________________________________________________________________
if __name__ == '__main__':
	wiki_get_list = get_txt_list()
	download_pdfs(wiki_get_list)

#   usr/bin/env python
#---------------------------------------------------------------------------#
#	MODULE:			wikipdf.py3												#
#	INFO:			Accesses a .txt file with each line being a title of a	#
#					Wikipedia page you'd like to save a PDF of. It then 	#
#					downloads all the files, saving them with a nice file-	#
#					name into the folder that the .txt is already in.		#
#	INSPIRATION:	Data hoarders have problems too.						#
#	CODED BY:		iivii @odd_codes										#
#	EMAIL:			iiviigames@pm.me										#
#	WEBSITE:		https://odd.codes										#
#	LICENSE:		BUDDYPACT												#		
#					BORROW, USE, DONATE, DOWNLOAD!							#
#					Your price? A courteous thanks.							#
#																			#
#																			#
#	Confused about that BUDDYPACT? Well, its simple. You can use my code	#
#	for	anything at all, commercial, personal, erotic or, whatever. The		#
#	only thing you are required to do if you choose to use it, is to link	#
#	me to the thing you used it for, or shoot me an email to tell me what   #
#	you're working on, so I can see the cool shit you are doing, and see	#
#	the connections forming between disparate groups.						#
#																			#
#	Maybe we can even get others to do this as well, and before you know it,#          
#	everybody is connected through collaborative frienships. That's the goal#   
#	of BUDDYPACT:															#
#																			#
#					Friendship Through Collaboration.						#
#---------------------------------------------------------------------------#


#																		IMPORTS
#_______________________________________________________________________________

import sys
import os
import requests


#																		GLOBALS
#_______________________________________________________________________________

BASEURL = "https://en.wikipedia.org/"
APIPDF = "api/rest_v1/page/pdf/"

#																		FUNCTIONS
#________________________________________________________________________________


def fix_string(words, spacer=" ", replacer=" ", addto=""):
	"""
Fixes a string by removing certain characters and swapping them out for new ones.
	"""
	fixed = words.replace(spacer, replacer)
	fixed += addto
	return fixed


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


def get_data_from(line):
	"""
Retrieves input from a user.
	"""
	msg = line
	msglen = len(msg)
	prompt = "\n::: "
	line = "_" * msglen
	res = input(msg+prompt)
	print(line + "\r")
	return res

	
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
	print("Enter the directory name where the text file is located, or,")
	directory = get_data_from("just hit ENTER to use the current directory:")
	if directory == "":
		directory = os.curdir
	else:
		os.chdir(directory)
		
	dirlist = os.listdir(directory)
	txtlist = []
	for i in range(len(dirlist)):
		if str(dirlist[i]).endswith(".txt"):
			txtlist.append(str(dirlist[i]))


	if len(txtlist) < 1:
		print("No .txt files in this directory\nExiting!")
		raise(sys.exit())


	print("Please enter one of the following file names to use as the reference:\n")
	print("NOTE: Do not enter .txt to the end of the filename!\n\n")
	striplist = []
	for i in range(len(txtlist)):
		striplist.append(txtlist[i].replace(".txt",""))

	for i in striplist:
		print(i)

	print("\n")
	
	fname = get_data_from("Enter the name of the .txt file to retrieve page names from:")
	for i in range(len(striplist)):
		if fname == striplist[i]:
			fname += ".txt"
			break
		elif i == len(striplist) - 1:
			print("Entered an invalid filename.\nExiting!")
			raise(sys.exit())
			

	print("Success!\nReading from: " + fname)
	
	#   READ FROM TEXTFILE
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
	
	#   Output API List Contents for Testing
	print("____________________________________________________________\n")
	for i in api_titles:
		print(i)
	print("____________________________________________________________\n")

	#   RETURN LIST FOR REQUESTING
	return api_titles


def download_pdfs(api_list):
	"""
This is the downloading portion of the code.
A list urls is passed into the argument and the names of the files
are created within this code. This loops until the .txt file
list is completely parsed.
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
		print("Downloading: %s" % out_file_name)

		#   Response from server
		r = requests.get(addresses[i], stream=True)

		#   Write the file to PDF in Chunks
		with open(out_file_name, 'wb') as pdf:
			for chunk in r.iter_content(chunk_size=4096):
				if chunk:
					pdf.write(chunk)

		#   Notify user that the file has successfully downloaded.
		print("%s downloaded!\n" % out_file_name)

	#   Completed Downloads List!
	print("DOWNLOADED ALL FILES!")
	raise(sys.exit())


#																		MAINLOOP
#_______________________________________________________________________________

wiki_get_list = get_txt_list()
download_pdfs(wiki_get_list)

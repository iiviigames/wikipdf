#   usr/bin/env python
#################################################################################################
#   MODULE:         wikipdf.py3                                                                 #                                                      #        
#   INFO:           Accesses a .txt file with all the wikipedia pages you want to                #
#                   download a PDF of, then, quickly downloads them to a folder on          #
#                   your PC.                                                                #
#   INSPIRATION:    Data hoarders have problems too.
#   CODED BY:       iivii @odd_codes
#   EMAIL:          iiviigames@pm.me
#   WEBSITE:        https://odd.codes
#   LICENSE:        YUMMYPACT - YOU.USE.MY.MATERIAL?.YOU.PROMISE.AMICABLE.COMMUNICATION.TOO!    #
#   NOTE:           Confused about that YUMMYPACT? Well, its simple. You can use my code for    #
#                   anything at all, commercial, personal, or pornographic. The only thing you      
#                   are required to do if you choose to use it, is to link me to the thing      
#                   you used it for, so I can see the cool shit you are doing, and maybe        
#                   we can even get others to do this as well, and before you know it,          
#                   everybody is connected through collaborative frienships. That's the goal    
#                   of YUMMYPACT - friendship through collaboration.
###############################################################################################
 
import sys
import os
import requests

EASYPDF = "https://en.wikipedia.org/api/rest_v1/page/pdf/Truth_Table"
PDFEXAMPLE = "https://en.wikipedia.org/w/index.php?title=Special:ElectronPdf&page=AI+winter&action=show-download-screen"
BASEURL = "https://en.wikipedia.org/"
php_req = "w/index.php?"
electron_pdf = "Special:ElectronPdf&page="
php_methods = [
    "action=",
    "title=",
    "help=",
    "page="
]
actions = ["show-download-screen"]
APIPDF = "api/rest_v1/page/pdf/"


def fix_string(words, spacer=" ", replacer=" ", addto=""):
    fixed = words.replace(spacer, replacer)
    fixed += addto
    return fixed


def fix_string_list(wordlist, spacer=" ", replacer=" ", addto=""):
    formatted_list = []
    for i in range(len(wordlist)):
        entry = wordlist[i]
        entry_fixed = entry.replace(spacer,replacer)
        entry_fixed += addto
        formatted_list.append(entry_fixed)

    return formatted_list


def get_data_from(line):
    msg = line
    msglen = len(msg)
    prompt = "\n::: "
    line = "_" * msglen
    res = input(msg+prompt)
    print(line + "\r")
    return res

    
def get_wiki_summary():
    page = get_data_from("Enter a page to get information from:")
    print(wikipedia.summary(page))
    if again():
        get_wiki_summary()
    else:
        raise(sys.exit())


def again():
    res = input("Once more? Y or N\n::: ")
    if not "y" in res.lower():
        return False
    else:
        return True


def form_pdf_request():
    pagename = get_data_from("Enter a page to formulate a PDF request from:")
    final = fix_string(pagename, " ", "+", "&")

    front_matter = base_url + php_req + php_methods[1] + electron_pdf
    rear_matter = php_methods[0] + actions[0]

    url = front_matter + final + rear_matter
    return url


def wiki_pdf():
    title = get_data_from("Enter the name of a page to get a PDF copy of:")
    parsed_title = fix_string(title, " ", "_")
    address = base_url + api_pdf + parsed_title
    return address
    
def get_txt_list():
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
    addresses = []
    for i in range(len(api_list)):
        title = api_list[i]
        address = BASEURL + APIPDF + title
        addresses.append(address)
    #   Request PDF information from wikipedia.
    for i in range(len(addresses)):
        #   use the name that was appeneded to the address list
        out_file_name = api_list[i]+".pdf"
        #   write that name to console 
        print("Downloading: %s" % out_file_name)

        #   Response from server
        r = requests.get(addresses[i], stream=True)

        #   Write the file to PDF
        with open(out_file_name, 'wb') as pdf:
            #pdf.write(r.content)
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    pdf.write(chunk)

        #   Log completion
        print("%s downloaded!\n" % out_file_name)

    #   Completed Downloads List!
    print("DOWNLOADED ALL FILES!")
    raise(sys.exit())


#   MAIN    #
#___________#

wiki_get_list = get_txt_list()
download_pdfs(wiki_get_list)

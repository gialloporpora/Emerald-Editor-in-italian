*** What is it? ***
This is a little Python script to help in localizzation of Crimson Editor, and maybe of other programs. It extract strings from a file and save it in a human readable file that is easier  to edit.

This is not perfect, string are  extracted with brute force and not all can be modified, in other words, it may happens that if you translate wrong strings the program stop to compile. 


*** Requirements ***
You need to have Python installed to run this script:
http://www.python.org
I have tested with Python 2.6 on Windows XP, but I think that  it works also with other 2.x Python version, I have not tried with 3., and if you are a newbe of Python don't install the 3.0 version. 
You require also the simplejson module, you can retrieve it using setuptools: easy_install simplejson or downloading it from the Python site.


*** Usage ***

You could begin to translate the cedt_it.txt file, all strings in that file are good string. 
When you have finished to translate all these strings, from commandline (Python need to be associated at .py files or, in the second case, it must be in the System variable %PATH%)
c:\yourdir>tlh.py build


This command save a json file with your translated string. Now use these info to translate your file:

C:\yourpath>tlh.py translate

If you have no download the cedt_us.rc file from Crimson Editor SVN, give this command first:

C:\yourpath>tlh.py forceupdate


It automatically download the last copy of the file from Crimson Editor SVN. 


*** NOTE ****
When you give the command "forceupdate" (or "update", but you don't use it) will be created these files (if they not exists yet):

- cedt_it.txt
- cedt2_it.txt
- rejected.txt


The first is the file that you need to translate. IMPORTANT: if you give the update command before saving your  translated string with "build" command all your work will be lost, please use it carefully. 
The second file contains some strings that, I think, shold no be translated. 
The third file, contains other string that should not be translated, if you think that some string must be good strings, append it to the cedt_it.txt file preserving the structure. 

For info, you could contact me at the Emerald Forum with a private message or send me an email. My username is gialloporpora, both in the forum that on Gmail.




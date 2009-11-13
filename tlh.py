import re, sys
import simplejson
DEFAULT_LANG="it"
DEFAULT_ENCODING=sys.getfilesystemencoding()


class humanFile():
	def __init__(self, filename, sep0="\n*************************************************************************\n", sep1="\n", fileencoding=DEFAULT_ENCODING):
		self. filename=filename
		self.sep0=sep0
		self.sep1=sep1
		self.encoding=fileencoding
		self._content=self.open()
		
	def __len__(self):
		return len(self.getDict())

	def open(self):
		""" Open the file as a normal file, it return the content of the file """
		try:
			f=open(self.filename, "r")
			s=f.read()
			f.close()
		except IOError:
			s=""
		return s
		
	def getContent(self):
		return self._content
		
	def _clear(self):
		self._content=""
		
	def _push(self, data):
		for i in data:
			self._content+="%s%s%s%s" %(i,self.sep1, data[i], self.sep0)
		
	def getDict(self):
		""" Open the file and return the content in a dictionary """
		d={}
		for  i in self._content.split(self.sep0):	
			items=i.strip().split(self.sep1)
			if len(items)==2: d[items[0]]=items[1]
		return d

	def writejson(self, data):
		""" This function write a dictionary in a human readable file. The original data in file are deleted """
		f=open(self.filename, "w")
		self._clear()
		self._push(data)
		self.save()


	def writeList(self, ls, data={}, clone=True):
		""" Save a list into a file, the dictionary is used to assign the second value. 
		If the dictionary not contains the key specified in list, its value could be:
		if clone is True (default) the second value is exactlly the first, key and value are the same, 
		if clone is False the value is 'not translated'. 
		It returns None if all string have been translated, a list of untraslated strings instead """
		self._clear()
		not_translated=[]
		for item in ls:
			if data.has_key(item):value=data[item]
			else:
				not_translated.append(item)
				if clone: value= item
				else: value="not translated"
			self._push({item:value})
		self.save()
		return not_translated
			
	def save(self):
		""" Save the file """
		from types import UnicodeType
		f=open(self.filename, "w")
		s=self._content
		if type(s)==UnicodeType:s=s.encode(self.encoding)
		f.write(s)
		f.close()



def listDiff(list1, list2):
	diffList=[]
	for i in list1:
		if not(i in list2):
			diffList.append(i)
	return diffList

def downloadRC():
	""" Download the cedt_us.rc file from Emerald Editor SVN 
	"""
	from urllib import urlretrieve
	urlretrieve("http://svn.emeraldeditor.com/viewvc.cgi/CrimsonEditor/trunk/res/cedt_us.rc?view=co", "cedt_us.rc")
def getAllStrings(filename="cedt_us.rc"):
	""" Extract all quoted strings from file """
	f=open("cedt_us.rc","r")
	s=f.read()
	f.close()
	regex=re.compile('"([^"]*)"')
	l=regex.findall(s)
	l=unique(l)
	return l

def getStrings(filename=")cedt_us.rc"):
	""" Extract al strings, it returns a tuple. The first element of the tuple
	are all strings with an accesskey, the second are all string without accesskey
		"""
	l=getAllStrings(filename)
	# now I remove some strings that doesn't be translated,  I save them in rejected.txt file
	regex=re.compile("\.h[\\\\0]*$|\.ico$|\.rc2*$|\.bmp$|^[\\d\\\\]+$|^.$|^#|\\\\r\\\\n|\.cur$|^[A-Z0-9]+_[A-Z\d_]+$|^$|^\.\.\.$|^Button[1]*$|^Static$|^separator$|^Sys\w+32$|^msctls_\w+32$|^detab\skey$|^escape\skey$|^Tab1$|^Tree1$|^List1$")
	l1=[i for i in l if not(regex.search(i))]
	l2=listDiff(l,l1)
	return (l1, l2)


def writeHumanFiles():
	filename="cedt_%s.txt" %DEFAULT_LANG
	f=humanFile(filename,)
	(ls1, ls2)=getStrings()
	try:
		d=getPermanentDict()
	except:
			d={}
	not_translated=f.writeList(ls1,d)
	g=humanFile("not_translated.txt")
	g.writeList(not_translated, {}, False)
	h=humanFile("rejected.txt")
	h.writeList(ls2, {})
	return (len(f), len(g), len(h))

		




def getPermanentDict():
	filename="cedt_%s.json" %DEFAULT_LANG
	f=open(filename,"r")
	data=simplejson.load(f, encoding=DEFAULT_ENCODING)
	f.close()
	return data

def saveDict():
	filename="cedt_%s.json" %DEFAULT_LANG
	f=open(filename,"w")
	filename="cedt_%s.txt" %DEFAULT_LANG
	g=humanFile(filename)
	d=g.getDict()
	simplejson.dump(d, f, indent=2, encoding=DEFAULT_ENCODING)
	f.close()

def updateRC():
	d=getPermanentDict()
	f=open("cedt_us.rc","r")
	s=f.read()
	f.close()
	for i in d:
		original='"%s"' %i		
		translated='"%s"' %d[i]
		s=s.replace(original, translated)
	filename="cedt_%s.rc" %DEFAULT_LANG
	f=open(filename,"w")
	s=s.encode(DEFAULT_ENCODING)
	f.write(s)
	f.close()
	
	
	
		

		
		

def unique(l):
	d={}
	for i in l:
		d[i]=i
		l2=[]
	for i in l:
		if d.has_key(i):
			l2.append(i)
			del(d[i])
	return l2
		
if __name__ == '__main__':
	args=sys.argv
	if len (args)==1:
		print "\tThis is a little program to help extract strings from RC files\n\n"
		print "\tUsage: tlh.py [action] \n\n"
		print "Action are:\n\n"
		print "FORCEUPDATE: download the new RC file from Emerald editor SVN and create two files with localizzation strings\n"
		print "UPDATE: create files for localizzation using the local copy  - if exist - of cedt_us.rc\n\n"
		print "BUILD: force the creation of a new dictionary from the txt file. The dictionary will be deleted and created using strings in txt file"
		print "UPDATEDICT: update the dictionary adding only translated strings\n\n"
		print "TRANSLATE: create the RC file using strings  in the dictionary (JSON file)\n\n\n"
	else:
		action=args[1].upper()
		if  (action=="FORCEUPDATE"):
			downloadRC()
			info=writeHumanFiles()
		elif (action=="UPDATE"): info=writeHumanFiles()
		elif action=="BUILD":	
			saveDict()
		elif action=="TRANSLATE":
				updateRC()
		else: print "Bad action..."
	try:
		print "- You have translated %s\n" %info[0]
		print "%s new strings to translate\n" %info[1]
		print "%s strings have been automatically rejected\n\n" %info[2]
	except:
		pass
			
		
		
		
		
		
import re, sys
import simplejson
SEP="----------"

DEFAULT_LANG="it"
DEFAULT_ENCODING=sys.stdin.encoding


def downloadRC():
	""" Download the cedt_us.rc file from Emerald Editor SVN 
	"""
	from urllib import urlretrieve
	urlretrieve("http://svn.emeraldeditor.com/viewvc.cgi/CrimsonEditor/trunk/res/cedt_us.rc?view=co", "cedt_us.rc")
def getStrings(filename=")cedt_us.rc"):
	""" Extract al strings, it returns a tuple. The first element of the tuple
	are all strings with an accesskey, the second are all string without accesskey
		"""
	f=open("cedt_us.rc","r")
	s=f.read()
	f.close()
	regex=re.compile('"([^"]*)"')
	l=regex.findall(s)
	l=unique(l)
	l1=[i for i in l if i.find("&")!=-1]
	l2=[i for i in l if i.find("&")==-1]
	return (l1,l2)
	
def writeHumanFile():
	filename="cedt_%s.txt" %DEFAULT_LANG
	f=open(filename,"w")
	s=""
	(ls1, ls2)=getStrings()
	try:
		d=getPermanentDict()
	except:
			d={}
	for i in ls1:
		j="not translated"
		if d.has_key(i): j=d[i]
		s+="%s\n%s\n%s\n" %(i,j,SEP)
	s=s.encode("cp850")
	f.write(s)
	f.close()
	filename="cedt2_%s.txt" %DEFAULT_LANG
	f=open(filename,"w")
	s=""
	for i in ls2:
		s+="%s\n%s\n%s\n" %(i,i,SEP)
	s=s.encode(DEFAULT_ENCODING)	
	f.write(s)
	f.close()	

def getDict():
	filename="cedt_%s.txt" %DEFAULT_LANG
	f=open(filename,"r")
	s=f.read()
	f.close()
	d={}
	for  i in s.split(SEP):
		items=i.strip().split("\n")
		if len(items)==2: d[items[0]]=items[1]
	return d
def getPermanentDict():
	filename="cedt_%s.json" %DEFAULT_LANG
	f=open(filename,"r")
	data=simplejson.load(f, encoding=DEFAULT_ENCODING)
	f.close()
	return data

def saveDict():
	filename="cedt_%s.json" %DEFAULT_LANG
	f=open(filename,"w")
	d=getDict()
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
		print "\tUsage: tlhelper.py [action] \n\n"
		print "Action are:\n\n"
		print "UPDATE: download the new RC file from Emerald editor SVN and create two files with localizzation strings\n"
		print "FORCE: force the creation of a new dictionary from the txt file. The dictionary will be deleted and created using strings in txt file"
		print "TRANSLATE: create the RC file using strings  in the dictionary (JSON file)\n\n\n"
	else:
		action=args[1].upper()
		if  (action=="UPDATE"):
			downloadRC()
			writeHumanFile()
		elif action=="FORCE":	
			saveDict()
		elif action=="TRANSLATE":
				updateRC()
		else: print "Bad action..."

			
		
		
		
		
		
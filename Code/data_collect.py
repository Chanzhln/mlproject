import urllib, json, csv, sys, os
from data_process import *
from constant import *

reload(sys)
sys.setdefaultencoding('utf-8')



def getJson(url):
	page = urllib.urlopen(url)
	content = page.read()
	#print content
	return content

def changeTitle(name):
	str = ''
	for i in range(0,len(name)):
		if name[i] == ' ':
			str += '+'
		else:
			str += name[i]
	return str
	
def makeUrl(movie):
	lst = str(movie).split(',')

	if len(lst) == 1:
		url = "http://www.omdbapi.com/?t="+changeTitle(lst[0]) + "&plot=short&r=json"
	else:
		url = "http://www.omdbapi.com/?t="+changeTitle(lst[0]) + "&y="+lst[1]+"&plot=short&r=json"
	return url
	
def sparse_json(content):
	json_dict = json.loads(content)
	data = []
	index = 0
	while index < len(attribute_dict):
		if index == 2:
			genre = json_dict['Genre']
			g_list = str(genre).split(',')
			for i in range(0,3):
				if i < len(g_list):
					data.append(sanctify(g_list[i]))
				else:
					data.append('?')
			index = 5
		elif index == 6:
			writer = json_dict['Writer']
			w_list = str(writer).split(',')
			for i in range(0,3):
				if i < len(w_list):
					data.append(sanctify(w_list[i]))
				else:
					data.append('?')
			index = 9
		elif index == 9:
			actors = json_dict['Actors']
			a_list = str(actors).split(',')
			for i in range(0,4):
				if i < len(a_list):
					data.append(sanctify(a_list[i]))
				else:
					data.append('?')
			index = 13
		else:
			val = json_dict[attribute_dict[index]]
			val = val.split(',')[0]
			if index == 14:
				val = val.replace(',','')

			if index ==13 or index == 14 or index == 17:
				if val == 'N/A':
					val = '?'
				else:
					val = (float)(val)
			else:
				val = sanctify(val)
			data.append(val)
			index += 1
	
	return data

def collect():
	# open the list
	# read the movies name and year we want to use
	f = open('../Data/list.txt','r')
	line = f.readline()


	movies_list = []
	
	# open a new csv file
	csv_file = open('../Data/Movie_Data.csv','w')
	writer = csv.writer(csv_file)
	
	# write the first row, name of attribute
	attribute = []
	for key in attribute_dict:
		attribute.append(attribute_dict[key])
	writer.writerow(attribute)
	
	count = 0
	# read the file row by row.
	while line:
		print line
		url = makeUrl(line)
		content = getJson(url)
		json_dict = json.loads(content)
		#print line
		if json_dict['Response'] == 'True' and json_dict['imdbRating'] != 'N/A' and json_dict['Type'] == 'movie':
			#print json_dict['Title']
			if json_dict['Title'] not in movies_list:
				movies_list.append(json_dict['Title'])
				data = sparse_json(content)
				writer.writerow(data)
				count += 1
		line = f.readline()
	
	csv_file.close()
	f.close()

	print '\nData collection finish!'


#collect()

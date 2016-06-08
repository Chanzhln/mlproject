import urllib, json, csv, sys, os, pickle, random
from constant import *
import Queue
reload(sys)
sys.setdefaultencoding('utf-8')

def sanctify(text):
    ret = text

    while ret[0] == ' ':
        ret = ret[1:]

    while ret.find('(') != -1:
        left = ret.find('(')
        right = ret.find(')')

        if right > left:
            ret = ret[:left] + ret[right+1:]
        else:
            ret = ret[:left]

    ret = ret.replace('\'','')
    ret = ret.replace('\"','')

    while ret[-1] == ' ':
        ret = ret[:-1]

    return ret

def save(dObj, sFilename):
    """Given an object and a file name, write the object to the file using pickle."""
    f = open(sFilename, "w")
    p = pickle.Pickler(f)
    p.dump(dObj)
    f.close()

def load(sFilename):
    """Given a file name, load and return the object stored in the file."""
    f = open(sFilename, "r")
    u = pickle.Unpickler(f)
    dObj = u.load()
    f.close()
    return dObj

def make_classification():
    finput = '../Data/Movie_Data.csv'
    foutput = '../Data/Movie_Class.csv'

    csv_read = open(finput,'r')
    csv_write = open(foutput,'w')

    reader = csv.reader(csv_read)
    writer = csv.writer(csv_write)

    count = 0
    for line in reader:
        if count > 0:
            idx = attribute_index['imdbRating']
            rating = (float)(line[idx])
            if rating >= 8.5:
                level = 'S'
            elif rating >= 7.5 and rating < 8.5:
                level = 'A'
            elif rating >= 6.5 and rating < 7.5:
                level = 'B'
            elif rating >= 5.5 and rating < 6.5:
                level = 'C' 
            else:
                level = 'F'
            print line[idx],level
            line[idx] = level
        
        writer.writerow(line)
        count += 1

    csv_read.close()
    csv_write.close()

def remove_column():
    finput = '../Data/train-test/train.csv'
    foutput = '../Data/train-test/removed-train.csv'

    csv_read = open(finput,'r')
    csv_write = open(foutput,'w')

    reader = csv.reader(csv_read)
    writer = csv.writer(csv_write)

    remove_lst = [0,14,15,16]
    row = 0
    for line in reader:
        tmp = []
        for i in range(0,len(line)):
            if i not in remove_lst:
                tmp.append(line[i])
        writer.writerow(tmp)

    csv_read.close()
    csv_write.close()

def gather(finput, gather_list,fileName):
    #finput = '../Data/Movie_Data_1990-now.csv'
    gather_dict = {}

    csv_read = open(finput,'r')
    reader = csv.reader(csv_read)

    #gather_list = [5]
    rating = 17
    row = 0
    for line in reader:
        if row > 0:
            for idx in gather_list:
                if line[idx] == 'N/A' or line[idx] == '?':
                    continue

                if gather_dict.has_key(line[idx]):
                    gather_dict[line[idx]][0] += (float)(line[rating])
                    gather_dict[line[idx]][1] += 1
                else:
                    gather_dict[line[idx]] = [(float)(line[rating]),1]
        row += 1

    for key in gather_dict:
        gather_dict[key][0] = (float)(gather_dict[key][0])/(float)(gather_dict[key][1])
        #print key,gather_dict[key]

    path = '../Data/pkl/' + fileName
    save(gather_dict,path)
    return gather_dict

def clean():
    finput = '../Data/Movie_Data.csv'
    foutput = '../Data/Movie_Data_clean.csv'

    csv_read = open(finput,'r')
    csv_write = open(foutput,'w')

    reader = csv.reader(csv_read)
    writer = csv.writer(csv_write)

    for line in reader:
        data = line
        for i in range(0,len(data)):
            data[i] = sanctify(data[i])
        
        writer.writerow(data)

    csv_read.close()
    csv_write.close()

def topK(finput, foutput, k, valve):
    pq = Queue.PriorityQueue()

    #finput = '../Data/pkl/Director.pkl'
    #foutput = '../'
    dic = load(finput)

    #print dic
    for key in dic:

        if pq.qsize() < k and dic[key][1] > valve:
            pq.put((dic[key][0],[key,dic[key]]))
        elif pq.qsize() == k:
            top = pq.get()
            if top[1][1][0] < dic[key][0] and dic[key][1] > valve:
                pq.put((dic[key][0],[key,dic[key]]))
            else:
                pq.put(top)

    top_lst = []
    while pq.empty() == False:
        tmp = pq.get()[1]
        top_lst.append(tmp)
        print tmp

    #save(top_lst,foutput)

def numeric():
    director = load('../Data/pkl/Director.pkl')
    genre = load('../Data/pkl/Genre.pkl')
    actor = load('../Data/pkl/Actors.pkl')
    write = load('../Data/pkl/Writer.pkl')
    year = load('../Data/pkl/Year.pkl')


    finput = '../Data/Movie_Class.csv'
    foutput = '../Data/Movie_Data_numeric.csv'

    csv_read = open(finput,'r')
    csv_write = open(foutput,'w')

    reader = csv.reader(csv_read)
    writer = csv.writer(csv_write)

    row = 0
    for line in reader:
        data = line
        if row > 0:
            for i in range(0,len(data)):

                if data[i] == '?' or data[i] == 'N/A':
                    data[i] == '?'

                elif i in [2,3,4]: #Genre
                    data[i] = genre[data[i]][0]
                elif i in [9,10,11,12]: #Actors
                    data[i] = actor[data[i]][0]
                elif i in [6,7,8]: #Writer
                    data[i] = write[data[i]][0]
                elif i in [5]: #Director
                    data[i] = director[data[i]][0]
                elif i in [2]: # Year
                    data[i] = year[data[i]][0]

        writer.writerow(data)

        row += 1

    csv_read.close()
    csv_write.close()

def filter():
    finput = '../Data/Movie_Data.csv'
    foutput = '../Data/Year/Movie_Data_2006-2010.csv'

    csv_read = open(finput,'r')
    csv_write = open(foutput,'w')

    reader = csv.reader(csv_read)
    writer = csv.writer(csv_write)


    row = 0
    for line in reader:
        if row == 0 or (float)(line[1]) in [2006, 2007,2008,2009,2010]:
            writer.writerow(line)
        row += 1

    csv_read.close()
    csv_write.close()

'''
filter()

gather([9,10,11,12],'Actors.pkl')
gather([6,7,8],'Writer.pkl')
gather([1],'Year.pkl')
'''

def check():
    obj = load('Director.pkl')
    for key in obj:
        print key,obj[key]

def pick():
    finput = '../Data/Movie_Class_numeric.csv'
    foutput = '../Data/PS4.csv'

    csv_read = open(finput,'r')
    csv_write = open(foutput,'w')

    reader = csv.reader(csv_read)
    writer = csv.writer(csv_write)

    row = 0
    data = []
    for line in reader:
        if row == 0:
            writer.writerow(line)
        else:
            data.append(line)
        row += 1

    
    ps4 = random.sample(data,1000)
    for sample in ps4:
        writer.writerow(sample)

    csv_read.close()
    csv_write.close()

#check()
#clean()
def p_analysis():
    dir =    '../Data/Year/Movie_Data_'#'../Data/Year/Movie_Data_2015.csv'
    for year in range(2006,2011):
        print year
        finput = dir + str(year) + '.csv'
        gather(finput, [5], 'Director.pkl')
        topK('../Data/pkl/Director.pkl','',3,1)

#p_analysis()
#filter()
'''
filter()
gather('../Data/Year/Movie_Data_2006-2010.csv', [2,3,4],'Genre.pkl')
gather('../Data/Year/Movie_Data_2006-2010.csv', [5],'Director.pkl')
gather('../Data/Year/Movie_Data_2006-2010.csv', [6,7,8],'Writer.pkl')
gather('../Data/Year/Movie_Data_2006-2010.csv', [9,10,11,12],'Actors.pkl')
'''
#topK('../Data/pkl/Actors.pkl','',5, 2)
#pick()
def year_changes():
    gather_dict = gather('../Data/Movie_Data.csv',[1], 'Year.pkl')
    foutput = '../Data/year_changes.csv'
    csv_write = open(foutput,'w')
    writer = csv.writer(csv_write)

    year = []
    imdb = []
    for y in range(1990,2017):
        year.append(y)
        imdb.append(gather_dict[str(y)][0])

    writer.writerow(year)
    writer.writerow(imdb)

    csv_write.close()

    print imdb


def split_data():
    finput = '../Data/Movie_Class_numeric.csv'

    csv_total = open(finput,'r')
    csv_train= open('../Data/train.csv','w')
    csv_test = open('../Data/test.csv','w')

    train = []
    test  = []
    total = []
    row = 0
    reader = csv.reader(csv_total)
    train_writer = csv.writer(csv_train)
    test_writer  = csv.writer(csv_test)

    for line in reader:
        if row == 0:
            train.append(line)
            test.append(line)
        else:
            total.append(line)
        row += 1

    test += random.sample(total, 3427)

    for line in test:
        test_writer.writerow(line)

    for line in total:
        if line not in test:
            train.append(line)

    for line in train:
        train_writer.writerow(line)

    csv_total.close()
    csv_train.close()
    csv_test.close()

def step_train():
    finput = '../Data/train-test/train.csv'
    fdir = '../Data/train-test/train_'

    csv_read = open(finput,'r')

    reader = csv.reader(csv_read)

    title = []
    examples = []
    row = 0

    for line in reader:
        if row == 0:
            title = line
        else:
            examples.append(line)
        row+=1

    print 'total number: ',len(examples)

    for i in range(1,11):
        foutput = fdir + str(i) + '.csv'
        csv_write = open(foutput, 'w')
        writer = csv.writer(csv_write)
        writer.writerow(title)

        num = 10000 * i / 10
        part_examples = random.sample(examples, num)
        print "Number of part example: ", len(part_examples)
        for line in part_examples:
            for i in range(0,len(line)-1):
                if line[i] == '?' or line[i] == 'N/A':
                    line[i] = '?'
                else:
                    line[i] = (float)(line[i])
            writer.writerow(line)

        csv_write.close()

def useful():
    finput = '../Data/train-test/test.csv'
    foutput = '../Data/train-test/test-2.csv'

    csv_read = open(finput, 'r')
    csv_write = open(foutput, 'w')

    reader = csv.reader(csv_read)
    writer = csv.writer(csv_write)

    row = 0
    for line in reader:
        if row == 0:
            writer.writerow(line)
        else:
            for i in range(0,len(line)-1):
                if line[i] == '?' or line[i] == 'N/A':
                    line[i] = '?'
                else:
                    line[i] = (float)(line[i])

            writer.writerow(line)
        row += 1

    csv_read.close()
    csv_write.close()

useful()






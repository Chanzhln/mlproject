attribute_dict = {
 0:'Title',
 1:'Year',
 2:'Genre_1',
 3:'Genre_2',
 4:'Genre_3',
 5:'Director',
 6:'Writer_1',
 7:'Writer_2',
 8:'Writer_3',
 9:'Actors_1',
10:'Actors_2',
11:'Actors_3',
12:'Actors_4',
13:'Metascore',
14:'imdbVotes',
15:'Language',
16:'Country',
17:'imdbRating'
}

attribute_index = {
'Title':0,
'Year':1,
'Genre_1':2,
'Genre_2':3,
'Genre_3':4,
'Director':5,
'Writer_1':6,
'Writer_2':7,
'Writer_3':8,
'Actors_1':9,
'Actors_2':10,
'Actors_3':11,
'Actors_4':12,
'Metascore':13,
'imdbVotes':14,
'Language':15,
'Country':16,
'imdbRating':17
}


def sanctify(text):
    ret = text

    while ret.find('(') != -1:
        left = ret.find('(')
        right = ret.find(')')
        if right > left:
            ret = ret[:left] + ret[right+1:]
        else:
            ret = ret[:left]
    while ret[-1] == ' ':
        ret = ret[:-1]
        
    ret = ret.replace('\'','')
    ret = ret.replace('\"','')

    return ret

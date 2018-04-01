'''
@author：KongWeiKun
@file: panduola.py
@time: 18-4-1 上午9:37
@contact: kongwiki@163.com
'''
items	=	{"Dr	Dog/Fate":	[2.5,	4,	3.5,	3,	5,	4,	1],
			"Phoenix/Lisztomania":	[2,	5,	5,	3,	2,	1,	1],
			"Heartless	Bastards/Out":	[1,	5,	4,	2,	4,	1,	1],
			"Todd	Snider/Don't	Tempt	Me":	[4,	5,	4,	4,	1,	5,	1],
			"The	Black	Keys/Magic	Potion":	[1,	4,	5,	3.5,	5,	1,	1],
			"Glee	Cast/Jessie's	Girl":	[1,	5,	3.5,	3,	4,	5,	1],
			"La	Roux/Bulletproof":	[5,	5,	4,	2,	1,	1,	1],
			"Mike	Posner":	[2.5,	4,	4,	1,	1,	1,	1],
			"Black	Eyed	Peas/Rock	That	Body":	[2,	5,	5,	1,	2,	2,	4],
			"Lady	Gaga/Alejandro":	[1,	5,	3,	2,	1,	2,	1]}
users	=	{"Angelica":	{"Dr	Dog/Fate":	"L",
																						"Phoenix/Lisztomania":	"L",
																						"Heartless	Bastards/Out	at	Sea":	"D",
																						"Todd	Snider/Don't	Tempt	Me":	"D",
																						"The	Black	Keys/Magic	Potion":	"D",
																						"Glee	Cast/Jessie's	Girl":	"L",
																						"La	Roux/Bulletproof":	"D",
																						"Mike	Posner":	"D",
																						"Black	Eyed	Peas/Rock	That	Body":	"D",
																						"Lady	Gaga/Alejandro":	"L"},
									"Bill":	{"Dr	Dog/Fate":	"L",
																		"Phoenix/Lisztomania":	"L",
																		"Heartless	Bastards/Out	at	Sea":	"L",
																		"Todd	Snider/Don't	Tempt	Me":	"D",
																		"The	Black	Keys/Magic	Potion":	"L",
																		"Glee	Cast/Jessie's	Girl":	"D",
																		"La	Roux/Bulletproof":	"D",
																		"Mike	Posner":	"D",
																		"Black	Eyed	Peas/Rock	That	Body":	"D",
																		"Lady	Gaga/Alejandro":	"D"}}

def manhattan(vector1,vector2):
    distance = 0
    total = 0
    n = len(vector1)
    for i in range(n):
        distance += abs(vector1[i] - vector2[i])
    return distance

def computerNearestNeighboor(itemName,itemVector,items):
    """按照距离排序，返回邻近物品列表"""
    distances = []
    for otherItem in items:
        if otherItem != itemName:
            distance = manhattan(itemVector,items[otherItem])
            distances.append((distance,otherItem))
    distances.sort()
    return distances

def classify(user,itemName,itemVector):
    nearest = computerNearestNeighboor(itemName,itemVector,items)[0][1]
    rating = users[user][nearest]
    return rating

if __name__ == '__main__':
    s = classify('Angelica', 'Chris	Cagle/I	Breathe	In.	I	Breathe	Out', [1, 5, 2.5, 1, 1, 5, 1])
    print(s)

'''
@author: xclee

#https://grouplens.org/datasets/movielens/ rating.csv
'''

import os
import sys 
import math
from itertools import islice

class ItemCF:
    def __init__(self, filename = None):
        self.filename = filename
        
    def loadData(self):
        self.list = []
        self.train = {}
        self.train2 = {}
        file = open(self.filename, 'r')
        for line in islice(file, 1, None):
            userid, itemid, score, time = line.split(',')
            self.list.append((userid, itemid, float(score)))
            self.train.setdefault(itemid,{})
            self.train[itemid][userid] = float(score) # 

            self.train2.setdefault(userid,{})
            self.train2[userid][itemid] = float(score) # 
            
    def cal_sim_martix(self):
        self.sim_martix = dict()
        count = dict()
        item_user_like_count = dict() #like itemi count

        for item, users in self.train.items():
            for useri in users.keys():
                item_user_like_count.setdefault(useri,0)
                item_user_like_count[useri] += 1
                for userj in users.keys():
                    if useri == userj:
                        continue
                    count.setdefault(useri,{})
                    count[useri].setdefault(userj,0)
                    count[useri][userj] += 1

#       print "martix start:\n"
#       print count.items()
#       print "martix end:\n"

        for useri, users in count.items():
            self.sim_martix.setdefault(useri,{})
            for userj,cnt in users.items():
                if useri == userj:
                    continue
                self.sim_martix[useri].setdefault(userj, 0)
                self.sim_martix[useri][userj] = cnt / math.sqrt(item_user_like_count[useri] * item_user_like_count[userj])
        
        print "done ~~\n"

    def recommend(self, user):
        self.loadData()
        self.cal_sim_martix()
        rank = dict()
        user_items = self.train2.get(user,{})

        k = 10

        for v, wuv in sorted(self.sim_martix[user].items(), key = lambda x:x[1], reverse = True)[0:k]:
            v_items = self.train2.get(v,{})
            for i,rvi in v_items.items():
                if i in user_items:
                    continue
                rank.setdefault(i,0)
                rank[i] += wuv * rvi

        limit = 5
        list = sorted(rank.items(), key = lambda x:x[1], reverse = True)[0:limit]
        print list
        
if __name__ == "__main__":

    if len(sys.argv) < 2 :
        print "please input ratings.csv file path~"
        os._exit(0)
    
    filepath = sys.argv[1]
    if os.path.exists(filepath) == False :
        print filepath + "not exists!\n"
        os._exit(0)

    item = ItemCF(filepath)
    item.recommend('A')

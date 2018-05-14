
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
        file = open(self.filename, 'r')
        for line in islice(file, 1, None):
            #print line
            userid, itemid, score, time = line.split(',')
            self.list.append((userid, itemid, float(score)))
            self.train.setdefault(userid,{})
            self.train[userid][itemid] = float(score)
            
    def cal_sim_martix(self):
        self.sim_martix = dict()
        count = dict()
        item_user_like_count = dict() #like itemi count

        for user, items in self.train.items():
            for itemi in items.keys():
                item_user_like_count.setdefault(itemi,0)
                item_user_like_count[itemi] += 1
                for itemj in items.keys():
                    if itemi == itemj:
                        continue
                    count.setdefault(itemi,{})
                    count[itemi].setdefault(itemj,0)
                    count[itemi][itemj] += 1
                
        for itemi, items in count.items():
            self.sim_martix.setdefault(itemi,{})
            for itemj,cnt in items.items():
                if itemi == itemj:
                    continue
                self.sim_martix[itemi].setdefault(itemj, 0)
                self.sim_martix[itemi][itemj] = cnt / math.sqrt(item_user_like_count[itemi] * item_user_like_count[itemj])
        
        print "done ~~\n"

    def recommend(self, user):
        self.loadData()
        self.cal_sim_martix()
        rank = dict()
        user_items = self.train.get(user,{})
        #print user_items
        k = 10

        for itemi,score in user_items.items():
            for itemj,wj in sorted(self.sim_martix[itemi].items(), key = lambda x:x[1], reverse = True)[0:k]:
                if itemj in user_items:
                    continue # has this item,not recommend
                rank.setdefault(itemj,0)
                rank[itemj] += score * wj
        
        #print rank
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
    item.recommend('2')

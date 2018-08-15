#Algorithmic Trading with Machine Learning


#imports
from sklearn import tree
    
# - Using Analysis of Highs Lows and Trading Volume
def HLV_tree(t,h,l,v,acc=10):

    features = []
    labels = []

    for i in range(len(t) - acc):
        
        temp_t = t[acc + i - 1]
        temp_h = h[acc + i - 1]
        temp_l = l[acc + i - 1]
        temp_v = v[acc + i - 1]
        
        features.append([temp_t, temp_h, temp_l, temp_v])
    
        #1 means price went up
        if t[acc + i] > t[acc + i - 1]:
            labels.append([1])
        else:
            labels.append([0])
            
    clf = tree.DecisionTreeClassifier()
    clf.fit(features, labels)
    temp_list = []
    
    for i in range(acc):
        temp_list.append([])
        temp_list[i].append(t[-1*(acc - i)])
        temp_list[i].append(h[-1*(acc - i)])
        temp_list[i].append(l[-1*(acc - i)])
        temp_list[i].append(v[-1*(acc - i)])
        
    if clf.predict(temp_list)[0] == 1:
        return 1
    else:
        return 0


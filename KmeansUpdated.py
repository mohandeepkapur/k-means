# Mohandeep Kapur
# goal: implement K-means with classes and numpy arrays
# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

# FOR N-DIMENSIONAL PROGRAM, look at MAIN.PY

import numpy as np
import matplotlib.pyplot as plt
import random as rnd

class Point: #coords randomly generated, can be changed to read coords from a file
    def __init__(self, numdim, choice=0, domain=100):
        if choice >= 0:
            self._coord = np.random.randint(0, domain, numdim) #randomly generate points for K-means
        else:
            self._coord = np.array([])
            for i in range(numdim):
                a = int(input(f'k-nearest point, enter coordinates for ur your point, indx {i}: '))
                self.coord = np.append(self.coord, a)
    
    @property
    def coord(self):
        return self._coord
    
    @coord.setter
    def coord(self, value):
        self._coord = value

    def __str__(self):
        return f'{self.coord}'

class Head(Point):
    def __init__(self, numdim, domain=100):
        super().__init__(numdim, domain)

    def __str__(self):
        return f'head:{self.coord}'

class Kmeans:
    def __init__(self, n, numdim, k):
        self.n = n
        self.numdim = numdim
        self.k = k
        self.A = np.array([], dtype=Point)
        self.initA()
        self.H = np.array([], dtype=Head)
        self.initHeads()
        self.clusterGroup = np.array([], dtype=Point)
        self.rgb = np.random.rand(self.k,3)
    
    def initA(self):
        for i in range(self.n):
            self.A = np.append(self.A, Point(self.numdim))

    def initHeads(self):
        for i in range(self.k):
            self.H = np.append(self.H, Head(self.numdim))

    def getDistance(self, clusterHead, clusterPt):
        val = 0
        for i in range(self.numdim):
            #print(str(type(clusterHead)) + 'check')
            val += ((int(clusterHead.coord[i]) - int(clusterPt.coord[i]))**2)
        return val

    def getAverage(self, points): #checked
        newCoord = np.array([])
        for i in range(self.numdim):
            sum = 0
            for j in range(len(points)):
                sum += points[j].coord[i] #check
            #x = len(points)
            #if(x==0): x=1
            newCoord = np.append(newCoord, int(sum/len(points)))
        return newCoord

    def assignGroup(self):
        for i in range(self.n):
            compare = np.array([], dtype=int)
            #print(compare)
            for j in range(self.k):
                #print(type(self.H[j]), type(self.A[i]))
                compare = np.append(compare, self.getDistance(self.H[j], self.A[i]))
                #print(compare)
            self.clusterGroup = np.append(self.clusterGroup, np.where(compare == min(compare)))
    
    def newHeads(self): #checked
        for i in range(self.k):
            collect = np.array([])
            for j in range(self.n):
                if(self.clusterGroup[j]==i):
                    collect = np.append(collect, self.A[j]) #collect array index corresponds to pt in array
                    #print(collect)
            self.H[i].coord = self.getAverage(collect)
            #print(f'{self.H[i]} {i}')

    def runTrial(self):
        print("\nOUR RANDOMLY GENERATED CLUSTER POINTS:")
        for obj in self.A:
            print(obj, end=' ')
        print("\n\nINITIAL CLUSTER HEADS:")
        for obj in self.H:
            print(obj, end=' ')
        self.assignGroup()
        print("\n\nINITIAL POINT GROUP ASSIGNMENTS:\n" + str(self.clusterGroup))

        i = 0
        temp = np.array([], dtype=int)
        while(np.array_equal(temp, self.clusterGroup)!=True and i < 200):
            self.newHeads()
            temp = np.copy(self.clusterGroup)
            self.clusterGroup = np.array([])
            self.assignGroup()
            i+=1
            #print(f'TRIAL {i}: {np.array_equal(temp, self.clusterGroup)}')

        print(f"\n\nFINAL CLUSTER HEADS of Groups 0 to {len(self.H)-1} in order:")
        for obj in self.H:
            print(obj, end=' ')
        print("\n\nFINAL POINT GROUP ASSIGNMENTS:\n" + str(self.clusterGroup))
        print(f"\nNUMBER OF ITERATIONS: {i}")
        
        #self.graph()
        return self.A, self.clusterGroup, self.H

    def kNearest(self, value):
        if(isinstance(value, Point)!=True):
            raise ValueError("pls use a point object for KNearest algorithm!")
        else:
            self.A = np.append(self.A, value)
        compare = np.array([])
        for i in range(len(self.H)):
            compare = np.append(compare, self.getDistance(self.H[i], value))
        self.clusterGroup = np.append(self.clusterGroup, np.where(compare == min(compare)))
        print(f'\nK NEAREST:\nthis point {value.coord} has been assigned to Group: {int(self.clusterGroup[-1])}, out of Groups {0} to {len(self.H)-1}')       

class Plot:
    def __init__(self):
        pass

    def graph(self, kmeans_instance):
        self.plotPoints('points', kmeans_instance)
        self.plotPoints('heads', kmeans_instance)
        plt.show()

    def plotPoints(self, type, kmeans_instance):
        for i in range(kmeans_instance.k):
            if type == 'heads':
                plt.plot(kmeans_instance.H[i].coord[0], kmeans_instance.H[i].coord[1], \
                    marker="o", markersize=5, markeredgecolor="black", markerfacecolor="black")
            elif type == 'points':
                for j in range(kmeans_instance.n):
                    if(kmeans_instance.clusterGroup[j]==i):
                        plt.scatter(kmeans_instance.A[j].coord[0], kmeans_instance.A[j].coord[1], color=kmeans_instance.rgb[i])        

def main():
    cat = input('would you like to run K-means? [y] [n]: ')
    if (cat=='y'):
        inputs = int(input('how many points would you like to generate: '))
        numdim = int(input('how many dimensions would you like each point to inhabit: '))
        k = int(input('how many groups do you want to classify all points into: '))
        if(inputs - k > 0):
            trial1 = Kmeans(inputs, numdim, k)
            trial1.runTrial()
            plotter = Plot()
            plotter.graph(trial1)
        else:
            raise ValueError('need more input pts for the # of the groups you\'ve defined')
    elif (cat=='n'):
        print('bye')
    else:
        raise ValueError('please input either y or n, nothing else')
    
    dog = input("would you like to run the K-nearest algorithm [y] [n]: ")
    if (dog=='y'):
        trial1.kNearest(Point(2, -1))
    elif (dog=='n'):
        print('bye')
    else:
        raise ValueError('please input either y or n, nothing else')

if __name__ == '__main__':
    main()

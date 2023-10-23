import numpy as np
import matplotlib.pyplot as plt
import random as rnd


# generate random pts to populate array
# assign cluster to group by comparing distance --> assigned to group/clusterhead it is closest to via distance

#gets stuck at local optimums, need global max
#what if instead of comparing intrapoint distances, we compared the total point capture # of each group, and try to distribute that evenly after groups are formed?

def main(): # n = 20000 k = <30 is the coolest thing ever. the density of points is so much -> k = 600 tho
    #INPUTS: 
    n = 500 # of points
    z = 2 # of dimensions --> above 2, loss of information due to mapping from R^(>2) to R2 visualy
    domain = 100
    A = [] # n x z
    k = 6 #if k very high but k<n, error still thrown, think issue w sort logic
    Heads = []
    ClusterGroup1 = [] #new
    ClusterGroup2 = [] #old

    rgb = colorValues(k)
    A = populateA(A, n, z, domain)
    Heads = assign_init_CH(Heads, A, k, n)
    ClusterGroup1 = assignGroup(A, Heads, ClusterGroup1)
    print("CLUSTER POINTS: " + str(A))
    print(str(Heads) + " <- INITIAL CLUSTER HEADS")
    print(str(ClusterGroup1) + " <- INITIAL ASSIGNMENTS")
    #graph(A, Heads, ClusterGroup1, rgb) #<-- create list of rgb values so i can graph each iteration w same color

    i = 0
    while(ClusterGroup1 != ClusterGroup2 and i < 200): 
        # end case is if assignments don't update, doesnt mean Heads are stationary tho
        # other end case could be when average of cluster pts in group = prev head of group --> no motion
        print("ITERATION: " + str(i+1))
        Heads = average_CH(Heads, ClusterGroup1, A)
        print(str(Heads) + " <- NEW CLUSTER HEADS")

        ClusterGroup2 = ClusterGroup1[:]
        ClusterGroup1 = [] 
        #ClusterGroup1.clear()
        ClusterGroup1 = assignGroup(A, Heads, ClusterGroup1)
        #print("CLUSTER POINTS: " + str(A))

        print(str(ClusterGroup1) + " <- NEW ASSIGNMENTS ")

        print(ClusterGroup2 == ClusterGroup1)
        #graph(A, Heads, ClusterGroup1, rgb)

        i+=1
    #Heads = average_CH(Heads, ClusterGroup1, A) # to check if heads move, end condition assignment dep not movy dep
    graph(A, Heads, ClusterGroup1, rgb)
    
# after initial cluster assignment, the Heads will be determined by an average function for the group! 
# no need to get rid of redundancy btwn Heads and A

def populateA(A, n, z, domain): # UPDATED TO BE SCALABLE
    for i in range(n):
        A.append(list(np.random.randint(0, domain, z)))
    return A

def assign_init_CH(Heads, A, k, n): 
    I = rnd.sample(range(n), k)
    for i in range(k):
        Heads.append(A[I[i]])
    return Heads

def assignGroup(A, Heads, ClusterGroup):
    # compare each point to the heads --> choose minimum value
    assign = []
    for i in range(len(A)):
        #{compare index A to all three clusterheads. whichever has the min compare val distance wins}}
        for j in range(len(Heads)): 
            assign.append(getDistance(Heads[j], A[i]))
        ClusterGroup.append(assign.index(min(assign))) 
        #if one point is equidistant to both heads, first group(index) may recieve bias
        assign = []
    return ClusterGroup

def average_CH(Heads, ClusterGroup, A): 
    #for each k group, find the average of all values and replace current Head with the average coord vals.
    Points = []
    for i in range(len(Heads)):
        for j in range(len(A)):
            if(ClusterGroup[j] == i):
                Points.append(A[j])
        Heads[i] = getAverage(Points)
        Points = []
    return Heads

def getDistance(ClusterHead, Clusterpt): #Updated for scalability just have for loops
    val = 0
    for i in range(len(Clusterpt)):
        val += ((ClusterHead[i] - Clusterpt[i])**2)
    return val

def getAverage(Points): # MADE SCALABLE
    Head = []
    for i in range(len(Points[0])):
        sum = 0
        for j in range(len(Points)):
            sum += Points[j][i]
        Head.append(int(sum/len(Points)))
    return Head

def colorValues(k):
    rgb = []
    for i in range(k):
        rgb.append([rnd.random(), rnd.random(), rnd.random()])
    return rgb

def plotArray(Array, color, ClusterGroup, rgb):
    if color == 'points':
        for i in range(len(Array)): #k -> len(Heads)
            for j in range(len(Array)):
                if(ClusterGroup[j] == i):
                   plt.scatter(Array[j][0], Array[j][1], color = rgb[i])
            
    if color == 'heads':
        for i in range(len(Array)):
            plt.plot(Array[i][0], Array[i][1], marker="o", markersize=5, markeredgecolor="black", markerfacecolor="black")
    return 0

def plotArray3(Array, color, ClusterGroup, k, rgb): # If z = 3!!!! not working rn
    plt.axes(projection='3d')
    return 0

def graph(A, Heads, ClusterGroup, rgb):
    plotArray(A, 'points', ClusterGroup, rgb)
    plotArray(Heads, 'heads', ClusterGroup, rgb)
    plt.show()
    return 0
    
main()
#max optimization for closest pt to head forming group -> head location locally optimized tho!

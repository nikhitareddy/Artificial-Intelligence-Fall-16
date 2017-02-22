from Queue import *
from collections import deque
from Queue import PriorityQueue


f=open('test43.txt','r')
algo=f.readline()
word=algo.strip()
l=[]
p=[]

l=f.readlines()
for i in l:
	p.append(i.strip())


start=p[0]
end=p[1]
lines=p[2]
r=[]
for i in range(3,(3+int(lines))):
    #if not p[i].isdigit() :
    r.append(p[i])
m=3+int(lines)+1
for i in range(m,len(p)):
        r.append(p[i])

e=[]
n = int(lines) 
for i in range(n):
	e.append(r[i].split())
f=[]
for i in range(n,len(r)):
        f.append(r[i].split())
y=[]
for i in range(len(e)):
        y.append(e[i][0])
        y.append(e[i][1])

if f:
        o={}
        for i in range(len(f)):
                o[f[i][0]]=f[i][1]


        
size=len(r)
paths = []
parent=[]
child=[]

j = 0
while j < n:
    u,v,d = r[j].split()
    j += 1
    parent.append(u)
    child.append(v)
    paths.append(d)

k=n

nodes=[]
path1=[]
while k<len(r):
    c,h=r[k].split()
    k+=1
    nodes.append(c)
    path1.append(h)
 
d={}
w=list(set(y))
for i in range(len(e)):
        if e[i][0] in w:
                d.setdefault(e[i][0], []).append(e[i][1])
       

totalNodes=len(nodes)


def bfs(graph, src, dest):
    frontier = deque()
    #cost=[]
    out=open('output.txt','w')
    #c=0
    copy=''
    shortestpath = (start, )
    frontier.append(shortestpath)
    o=list(d.values())
    explored = set([src])
    while frontier:
        shortestpath = frontier.popleft()
        lastnode = shortestpath[-1]
        if lastnode == dest:
            for i in range(0,len(shortestpath)):
                copy=copy+shortestpath[i]+' '+str(i)+'\n'
            print copy            
            out.write(copy)
            break
        if lastnode in d:
            for node in graph[lastnode]:
                if node not in explored:
                 
                    explored.add(node)
                  
                    frontier.append(shortestpath + (node,))
                     



def dfs(graph, src, dest):
    
    frontier = deque()
    cost=[]
    out=open('output6.txt','w')
   # c=0
    copy=''
    shortestpath = (src, )
    frontier.append(shortestpath)
    
    explored = set([src])
    print explored
    while frontier:
        shortestpath = frontier.pop()
        lastnode = shortestpath[-1]
        print shortestpath, '//',lastnode
        if lastnode == dest:
            for i in range(0,len(shortestpath)):
                copy=copy+shortestpath[i]+' '+str(i)+'\n'
            print copy            
            out.write(copy)
            break
        if lastnode in d:
            for node in reversed(graph[lastnode]):
                if node not in explored:
             
                    explored.add(node)
                 
                    frontier.append(shortestpath + (node,))
           

def ucs(graph, start, end):
    
    frontier = PriorityQueue()
    frontier.put((0,0,start))
    parent= {}
    parent[start] = None
    pathcost = {}
    pathcost[start] = 0
    out=open('output2.txt','w')
    c=0
    copy=''
    path=[]
    while frontier:
        v,s,lastnode = frontier.get()
       
        if lastnode == end:
            path.append(lastnode)
            while parent[lastnode] != None:
                lastnode = parent[lastnode]
                path.append(lastnode)
          
            path.reverse() 
            for i in range(0,len(path)):
                copy=copy+path[i]+' '+str(pathcost[path[i]])+'\n'
            print copy            
            out.write(copy)
            break
        if lastnode in d:
                for node in graph[lastnode]:
                   
                    updatedcost = pathcost[lastnode] + cost(lastnode, node)
                  
                    if node not in pathcost or updatedcost < pathcost[node]:
                        pathcost[node] = updatedcost
                        priority=updatedcost
                      
                        frontier.put((priority,pathcost[lastnode],node))
                        parent[node] = lastnode
                       # print'came from',parent[node]
               # print 'parent',parent
##    reconstruct_path(came_from, start, goal)
##    return came_from, cost_so_far
##def reconstruct_path(came_from, start, goal):
##    current = end
##    path = [current]
##    while current != start:
##        current = parent[current]
##        path.append(current)
##   # path.append(start) # optional
##    path.reverse() # optional
##   # print path
##   # print pathcost[start]
##    for i in range(0,len(path)):
##            copy=copy+path[i]+' '+str(pathcost[path[i]])+'\n'
##    print copy            
##    out.write(copy)


def astar(graph, start, end):
   
    frontier = PriorityQueue()
    frontier.put((0,0,start))
    parent= {}
    pathcost = {}
    parent[start] = None
    pathcost[start] = 0
    out=open('output2.txt','w')
    c=0
    copy=''
    path=[]
    z=0
    while frontier:
        v,p,lastnode = frontier.get()
       
        if lastnode == end:
           
             path.append(lastnode)
             while parent[lastnode] != None:
                lastnode = parent[lastnode]
                path.append(lastnode)
              
             path.reverse() 
             for i in range(0,len(path)):
                copy=copy+path[i]+' '+str(pathcost[path[i]])+'\n'
             print copy            
             out.write(copy)
             break
        if lastnode in d:
                for node in graph[lastnode]:
                 
                    pastcost = pathcost[lastnode] + cost(lastnode, node)
                    c+=1
                  
                    if node not in pathcost or pastcost < pathcost[node]:

                        pathcost[node] = pastcost
                     
                        estimatedcost=pastcost+int(o[node])
                      
                        frontier.put((estimatedcost,pathcost[lastnode],node))
                        parent[node] = lastnode
                        
   

def cost(node,node1):
        src=node1
        cost=0
        for i in range(len(e)):
                if src==e[i][1] and node==e[i][0]:
                        cost=cost+int(e[i][2])
                        break
        return cost



if word=='BFS':
        bfs(d,start,end)
elif word=='DFS':
        dfs(d,start,end)
elif word=='UCS':
        ucs(d,start,end)
elif word=='A*':
        astar(d,start,end)





    
    


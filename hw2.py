import copy
import os

class GetState:

    def __init__ (self,node_score,node_state):

        self.node_score = node_score

        self.node_state = node_state

        #self.node_pos=node_pos
infile = open('input38.txt','r')

width = int(infile.readline())
#width=width.strip()

board_weights = [[0 for col in range(width)] for row in range(width)]

board_state = [[0 for col in range(width)] for row in range(width)]

col_stri =["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
col_string=[]
for i in range(width):
    col_string.append(col_stri[i])

algo = infile.readline()
algo=algo.strip()

player = infile.readline()
player=player.strip('\n')

maxdepth = int(infile.readline().strip('\n'))


for i in range(width):

    rowscore = infile.readline().strip('\n').split(' ')

    for j in range(width):

        board_weights[i][j] = int(rowscore[j])

for i in range(width):

    statescore = infile.readline().strip('\n')

    for j in range(width):

        if statescore[j] == '.':

            board_state[i][j] = int(0)

        elif statescore[j] == 'X':

            board_state[i][j] = 1

        elif statescore[j] == 'O':

            board_state[i][j] = -1
board1_state=copy.deepcopy(board_state)

#print board1_state,'board'

infile.close()

def evaluate(board_weights, curstate, player):

    gamescore = 0

    for i in range(width):

            for j in range(width):

                gamescore = gamescore + board_weights[i][j] * curstate[i][j]


    if player == 'X':

        return gamescore

    else:

        return -gamescore

def getrs(d,c):
    s=[]
    for i in range(len(d)):
        for j in range(len(d[i])):
            if d[i][j]!=c[i][j] and d[i][j]==0:
                #print i,j
                if i-1>=0 and c[i-1][j]==-d[i-1][j] and d[i-1][j]!=0:
                    s.append(col_string[j]+str(i+1)+' '+'Raid')
                    #print col_string[j]+str(i+1)+' '+'Raid'
                if i+1<width and c[i+1][j]==-d[i+1][j] and d[i+1][j]!=0:
                    s.append(col_string[j]+str(i+1)+' '+'Raid')
                    #print col_string[j]+str(i+1)+' '+'Raid1'
                if j-1>=0 and c[i][j-1]==-d[i][j-1] and d[i][j-1]!=0:
                    s.append(col_string[j]+str(i+1)+' '+'Raid')
                    #print col_string[j]+str(i+1)+' '+'Raid2'
                if j+1<width and c[i][j+1]==-d[i][j+1] and d[i][j+1]!=0:
                    s.append(col_string[j]+str(i+1)+' '+'Raid')
                    #print col_string[j]+str(i+1)+' '+'Raid3'
                else:
                    s.append(col_string[j]+str(i+1)+' '+'Stake')
                    #print col_string[j]+str(i+1)+' '+'Stake'
    #print s
    return s[0]

def isstake(d,c):
    p=0
    for i in range(len(d)):
        for j in range(len(d[i])):
            if d[i][j]!=c[i][j] and d[i][j]==0:
           
                if i-1>=0 and c[i-1][j]==d[i-1][j] :
                    p+=1
                   
                elif i-1>=0 and c[i-1][j]==-d[i-1][j] and d[i-1][j]!=0 :
                    p-=1
                   
                if i+1<width and c[i+1][j]==d[i+1][j] :
                    p+=1
                    
                elif i+1<width and c[i+1][j]==-d[i+1][j] and d[i+1][j]!=0:
                    p-=1
                
                if (j-1>=0 and c[i][j-1]==d[i][j-1]) :
                    p+=1
                   
                elif j-1>=0 and c[i][j-1]==-d[i][j-1]and d[i][j-1]!=0 :
                    p-=1

                if j+1<width and c[i][j+1]==d[i][j+1] :
                    p+=1
                  
                elif j+1<width and c[i][j+1]==-d[i][j+1] and d[i][j+1]!=0:
                    p-=1
        
    if p>1:
        return True
    else:
        return False
    
def israid(d,c):
    for i in range(len(d)):
        for j in range(len(d[i])):
            if d[i][j]!=c[i][j] and d[i][j]==0:
                #print i,j
                if i-1>=0 and c[i-1][j]==-d[i-1][j] and d[i-1][j]!=0 or (i+1<width and c[i+1][j]==-d[i+1][j] and d[i+1][j]!=0) or (c[i][j-1]==-d[i][j-1] and d[i][j-1]!=0) or (j+1<width and c[i][j+1]==-d[i][j+1] and d[i][j+1]!=0) :
                    return True
                else:
                    return False

def stake_move(i,j,cur_state,playerlabel):

    cur_state[i][j]=playerlabel
    #print 'q'
    return cur_state



def raid_move(i, j, cur_state, playerlabel):

    cstate=[]
    cur1_state=copy.deepcopy(cur_state)
    flag = False
    raid_val=''
    #s=''
    flag = flag or ((i - 1 >= 0) and (cur_state[i - 1][j] == playerlabel))

    flag = flag or (i + 1 < width and cur_state[i + 1][j] == playerlabel)

    flag = flag or (j - 1 >= 0 and cur_state[i][j - 1] == playerlabel)

    flag = flag or (j + 1 < width and cur_state[i][j + 1] == playerlabel)

   
    if(flag ):
      
        if i == 0:

            if cur_state[i + 1][j] == -playerlabel:

                cur_state[i + 1][j] = playerlabel
        
        elif i > 0 and i < width-1 :

            if cur_state[i - 1][j] == -playerlabel:

                cur_state[i - 1][j] = playerlabel
                

            if cur_state[i + 1][j] == -playerlabel:

                cur_state[i + 1][j] = playerlabel
                

        else:

            if cur_state[i - 1][j] == -playerlabel:

                cur_state[i - 1][j] = playerlabel
                

        if j == 0 :

            if cur_state[i][j + 1] == -playerlabel:

                cur_state[i][j + 1] = playerlabel
        
        elif(j > 0 and j < width-1):

            if cur_state[i][j - 1] == -playerlabel:

                cur_state[i][j - 1]= playerlabel
                
            if cur_state[i][j + 1] == -playerlabel:

                cur_state[i][j + 1]= playerlabel
                
        else:

            if cur_state[i][j - 1] == -playerlabel:

                cur_state[i][j - 1] = playerlabel


    cur_state[i][j] = playerlabel

    return cur_state

def get_pos(i,j):

    return col_string[j] +str(i+1)



def is_full(cur_state):

    for i in range(width):

            for j in range(width):

                if(cur_state[i][j] == 0):

                    return False

    return True




# mini_max function pos is a string function

def mini_max(depth, maxdepth, gamestate, player, pos):

    result = GetState(float('-inf'),gamestate)

    if depth >= maxdepth or is_full(gamestate):

        result.node_score = evaluate(board_weights,gamestate,player)

        result.node_state = gamestate

        return result


    if depth % 2 == 0: 

        if player == 'X':

            playerlabel = 1

        elif player == 'O':

            playerlabel = -1

        result.node_score = float('-inf')



        for i in range(width):

            for j in range(width):

                if gamestate[i][j] == 0:


                    cur_state = copy.deepcopy(gamestate)
                    cur1_state=copy.deepcopy(gamestate)
                    
                    cur1_state[i][j]=playerlabel
                    
                    cur_state = raid_move(i,j,cur_state,playerlabel)

                    
                    new_pos =get_pos(i,j)
                    cur_score = mini_max(depth + 1, maxdepth,cur_state,player,new_pos)
                    
                    if cur1_state!=cur_state:
                        cur1_score = mini_max(depth + 1, maxdepth,cur1_state,player,new_pos)
                        if cur_score.node_score==cur1_score.node_score:
                            cur_state=cur1_state
                       
                    
                    if cur_score.node_score > result.node_score:

                        result.node_state = cur_state

                       
                        result.node_score = cur_score.node_score
                    if cur_score.node_score == result.node_score:
                        if isstake(board1_state,cur_state) and israid(board1_state,result.node_state) :
                            result.node_state = cur_state
                            result.node_score = cur_score.node_score
                            



    if depth %2 == 1: 
        

        if player == 'X':  

            opponentlabel = -1

        elif player == 'O':

            opponentlabel = 1

        result.node_score = float('inf')

        for i in range(width):

            for j in range(width):
                

                if gamestate[i][j] == 0:
                   
                    cur_state = copy.deepcopy(gamestate)
                    cur1_state=copy.deepcopy(gamestate)
                    cur1_state[i][j]=opponentlabel
                    
                    cur_state = raid_move(i,j,cur_state,opponentlabel)
    

                    new_pos =get_pos(i,j)
                    cur_score=mini_max(depth + 1, maxdepth,cur_state,player,new_pos)
                    if cur1_state!=cur_state:
                        cur1_score = mini_max(depth + 1, maxdepth,cur1_state,player,new_pos)
                        if cur_score.node_score==cur1_score.node_score:
                            cur_state=cur1_state

                    
                    if cur_score.node_score < result.node_score:

                        result.node_state = cur_state

                        result.node_score = cur_score.node_score
    
                    if cur_score.node_score == result.node_score:
                        if isstake(board1_state,cur_state) and israid(board1_state,result.node_state) :
                            result.node_state = cur_state
                            result.node_score = cur_score.node_score
                            
    return result





def alpha_beta(depth,maxdepth,gamestate,player, alpha,beta,pos):

    result = GetState(float('-inf'),gamestate)

    if depth >= maxdepth or is_full(gamestate):

        result.node_score = evaluate(board_weights,gamestate,player)

        result.node_state = gamestate


        return result



    if depth % 2 == 0:#player x

        result.node_score = float('-inf')

        if player == 'X':

            playerlabel = 1

        elif player == 'O':

            playerlabel = -1
        for i in range(width):

            for j in range(width):

                if gamestate[i][j] == 0:

                    cur_state = copy.deepcopy(gamestate)
                    cur1_state=copy.deepcopy(gamestate)
                    cur1_state[i][j]=playerlabel

                    cur_state = raid_move(i,j,cur_state,playerlabel)
                    

                    new_pos =get_pos(i,j)
                    cur_score = alpha_beta(depth + 1, maxdepth,cur_state,player,alpha,beta,new_pos)
                    if cur1_state!=cur_state:
                        cur1_score = alpha_beta(depth + 1, maxdepth,cur1_state,player,alpha,beta,new_pos)

                    
                        if cur_score.node_score==cur1_score.node_score:
                            cur_state=cur1_state

                    if cur_score.node_score > result.node_score:

                        result.node_state = cur_state

                        result.node_score = cur_score.node_score

                    if result.node_score >= beta :

                        return result
            

                    if result.node_score > alpha:

                        alpha = result.node_score

                    if cur_score.node_score == alpha :
                        if isstake(board1_state,cur_state) and israid(board1_state,result.node_state) and evaluate(board_weights,cur_state,player)==evaluate(board_weights,result.node_state,player):
                            result.node_state = cur_state
                            alpha = cur_score.node_score
                   



    if depth %2 == 1: 

        if player == 'X':  

            opponentlabel = -1

        elif player == 'O':

            opponentlabel = 1

        result.node_score = float('inf')

        
        for i in range(width):

            for j in range(width):

                if gamestate[i][j] == 0:

                    cur_state = copy.deepcopy(gamestate)
                    cur1_state=copy.deepcopy(gamestate)
                    cur1_state[i][j]=opponentlabel

                    cur_state = raid_move(i,j,cur_state,opponentlabel)
                    

                    new_pos =get_pos(i,j)
                    cur_score = alpha_beta(depth + 1, maxdepth,cur_state,player,alpha,beta,new_pos)
                    if cur1_state!=cur_state:
                        cur1_score = alpha_beta(depth + 1, maxdepth,cur1_state,player,alpha,beta,new_pos)


                        if cur_score.node_score==cur1_score.node_score:
                            cur_state=cur1_state
                    if cur_score.node_score < result.node_score:

                        result.node_state = cur_state

                        result.node_score = cur_score.node_score
           
                    if result.node_score <= alpha:


                       return result
                

                    if result.node_score < beta:

                        beta = result.node_score
                    if cur_score.node_score == beta:
                        if isstake(board1_state,cur_state) and israid(board1_state,result.node_state) and evaluate(board_weights,cur_state,player)==evaluate(board_weights,result.node_state,player):
                            result.node_state = cur_state
                            beta = cur_score.node_score
    return result






if algo == 'MINIMAX':
    
    board_state = mini_max(0,maxdepth,board_state,player,'maxnode').node_state
    
    #print board_state
    seq=getrs(board1_state,board_state)
    #print seq,'actual move,'
                    
    

if algo == 'ALPHABETA':


    board_state = alpha_beta(0,maxdepth,board_state,player,float('-inf'), float('inf'),'maxnode').node_state
    #print board_state
    #print isstake(board1_state,board_state)
    seq=getrs(board1_state,board_state)
    #print seq,'actual move,'



output = open('output.txt', 'w')
output.write(seq)
output.write('\n')


for i in range(width):

    line = ''

    for j in range(width):

        if board_state[i][j] == 0:

            line += '.'

        elif board_state[i][j] == 1:

            line += 'X'

        elif board_state[i][j] == -1:

            line += 'O'

    line += '\n'
    output.write(line)

output.close()

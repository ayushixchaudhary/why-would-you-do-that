# -*- coding: utf-8 -*-
"""EvolGame_by_conceited_altruists.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z4xKteuubfgQPKHHmewvQaywMLNw9VU0

# **Model Explaination**

We have four types of strategy : 


*   Always Cooperate (AC) : Has the maximum probability of sharing food and getting food in return.
*   Tit For Tat (TFT) : Decides based on the history of the agent at mercy.
*   Alternatively cooperate and defect (ALT) : Alternates between cooperate and defect.
*   Always Defect (AD) : Least willing to share food.
"""

import numpy as np
import matplotlib.pyplot as plt
import random

strat_names = ['AC','TFT','ALT','AD','none']
basket_of_strat = {'AC':[0.8],'TFT':[],'ALT':[0.6,0.4],'AD':[0.2],'none':[]}
num_to_strat = {0:'AC',1:'TFT',2:'ALT',3:'AD',4:'none'}
strat_to_num = {'AC':0,'TFT':1,'ALT':2,'AD':3,'none':4}


class special_Agent():
    def __init__(self,size,Q_table):
        self.clas = 'sp'
        self.id = id
        self.size = size
        self.pos = {'x':0,'y':0}
        self.food = 0
        self.age = 0
        self.strat_name = 'none'
        self.strat = basket_of_strat[self.strat_name]
        self.Q = Q_table
        self.reward = 0
        self.lr = 0.3
        self.epsilon = 0.2
        self.gamma = 0.99
        self.state = 'none'
        self.hist_strat = basket_of_strat['none']
        #self.done = False

    def choose_action(self,state,t):
        self.state = state
        #if state == 'none':
         #   self.strat_name = 'AC'
        if t and (np.random.random() < self.epsilon or state == 'none') :
            self.strat_name = np.random.choice(['AC','TFT','ALT','AD'])

        else :
            self.strat_name = num_to_strat[np.argmax(self.Q[strat_to_num[state]])]
            #print(num_to_strat[np.argmax(self.Q[strat_to_num[state]])])
        self.strat = basket_of_strat[self.strat_name]
        #self.epsilon -= 0.002 
        self.hist_strat = self.strat
        #print('id = ',self.id,'strat name = ',self.strat_name,'state = ',self.state)
    def update(self,pop_info,len):
        #print(Q_table)
        if self.strat_name != 'none':
            self.next_state = self.next(pop_info,len)
            self.Q[strat_to_num[self.state],strat_to_num[self.strat_name]] += self.lr*(self.reward + self.gamma*np.argmax(self.Q[np.random.randint(4,size=1)])-self.Q[strat_to_num[self.state],strat_to_num[self.strat_name]])
            self.strat_name = 'none'
    def next(self,pop_info,len):
        prob = [0.0,0.0,0.0,0.0,0.0]
        for key in pop_of_strat.keys():
            prob[strat_to_num[key]] = float(pop_of_strat[key][-1])/len
        return random.choices(strat_names,prob)[0]
class Agent():
    '''
        This is the class of agents. Every agent will be an instance
        of this class. Each Agent has some food at any time and we'll
        store it's age also.
    '''
    def __init__(self,size,strat):
        '''
            Initialize properties of agent
        '''
        self.clas = 'n'
        self.id = id
        self.size = size
        self.pos={'x':0,'y':0}
        self.food = 0
        self.age = 0
        self.strat_name = strat
        self.strat = basket_of_strat[self.strat_name]
        self.hist_strat = self.strat

class Environment():
    '''
        This class is for the environment. An environment is modelled as
        an n by n matrix. Each cell can host 1 unit of food, or 1 agent.
        Our simulation will have a day and a night in 1 iteration. In a 
        day, our agents will be spawned at random places in the grid and
        along with some food. the goal for an agent is to aquire as much
        food as it could. At night, the agents can choose to share excess
        food with another agent or to reproduce based on some probability.
        Agents that could not aquire food in the day would die in night. 
        We'll test what strategy lead to higher chance of survival of the
        population.
    '''
    def __init__(self,n=45,foodperday=100,repChance=0.5):
        '''
            Initializes environment
            n : Env Matrix size
            foodperday : Food unit to spawn everyday
            repChance : prob of agents to reproduce if they have >2 unit food.
        '''
        self.n = n #matrix size
        self.foodPerDay = foodperday
        self.reproductionChance = repChance
        self.pop_hist = []
        self.agents = []
        self.grid = self.__getEmptyMat()
        self.range = range # Range in which an agent can pick food
        self.curr_total_lived=0
        #self.sp_agentpop = 0 # population count of sp agents
        pop_of_strat = {'AC':[0],'TFT':[0],'ALT':[0],'AD':[0],'none':[0]}
        pop_of_size = {1:[0],2:[0]}
    def setup(self, agents : list):
        '''
            Sets environment's agents to `agents`
            agents : List of Agents initialized using `Agent` class
        '''
        self.agents=agents
        print('population : ',len(self.agents))
        self.curr_total_lived=len(agents)
        for i in range(len(agents)):
            agents[i].id=i+1
            pop_of_size[agents[i].size][-1] += 1
            pop_of_strat[agents[i].strat_name][-1] += 1 
        self.__update()
        return
    def __update(self):
        '''
            updating the data of population.
        '''
        pop_of_size[1].append(pop_of_size[1][-1])
        pop_of_size[2].append(pop_of_size[2][-1])
        pop_of_strat['AC'].append(pop_of_strat['AC'][-1])
        pop_of_strat['TFT'].append(pop_of_strat['TFT'][-1])
        pop_of_strat['ALT'].append(pop_of_strat['ALT'][-1])
        pop_of_strat['AD'].append(pop_of_strat['AD'][-1])
        pop_of_strat['none'].append(pop_of_strat['none'][-1])
        #print(pop_of_strat)
        return
    def __getEmptyMat(self):
        '''
            Private Method. Initializes empty grid. 
        '''
        return np.zeros((self.n,self.n),dtype=int)
    def __populateMat(self, agent : Agent):
        '''
            Private Method. Populate grid with Agent. 
        '''
        y = agent.pos['y']
        x = agent.pos['x']
        self.grid[y][x] = agent.id
        return
    def __chooseXYrand(self):
        '''
            Private Method. Choose a cell randomly in the grid
        '''
        x,y = np.random.choice(self.n),np.random.choice(self.n)
        # If cell is occupied, choose again
        while self.grid[y][x]!=0:
            x,y = self.__chooseXYrand()
        return x,y
    def __assignPosRand(self):
        '''
            Private Method. Spawns agents randomly on the grid. 
        '''
        for i in range(len(self.agents)):
            x,y = self.__chooseXYrand()
            self.agents[i].pos = {'x':x,'y':y}
            self.__populateMat(self.agents[i])
        return
    def __populateFood(self):
        '''
            Private Method. Spawns Food randomly. 
        '''
        for i in range(self.foodPerDay):
            x,y = self.__chooseXYrand()
            self.grid[y][x] = -1
        return
    def displayMat(self):
        '''
            Print current grid in numbers.
        '''
        for i in range(self.n):
            for j in range(self.n):
                print(self.grid[j][i],end=' ')
            print("")
        return
    def __pickFood(self):
        '''
           performing BFS to find nearest fox which will have food at a given cell. 
        '''
        dirn =[(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        idlist = [agent.id for agent in self.agents]
        pos = np.argwhere(self.grid == -1).tolist()
        for inx in pos:
            que = []
            que.append(inx)
            if len(que)!=0:
                for idx in que:            #x,y = agent.pos['x'],agent.pos['y']
                    for dir in dirn:
                        i = idx[0]+dir[0]
                        j = idx[1]+dir[1]
                        chk = [i,j]             #print(type(inx))
                        if chk in que:
                            continue            #for j in range(y-r,y+r):
                        elif i>=0 and j>=0 and i<self.n and j<self.n:
                            if self.grid[i][j] != -1 and self.grid[i][j] != 0:
                                self.agents[idlist.index(self.grid[i][j])].food+=1;
                                que.clear()
                                break
                            else:
                                que.append([i,j])

           

        return
    def __night(self):
        '''
            Private Method. Checks agent's food and shares food based on
            Agent's sttrategy. Then kills the ones who couldn't precure 
            food and then creates new agents for Agents had more food.

            I am forming the probability in such a manner that big foxes are more altruistic by instinct (they already had a 1 at the beggining
            of their stratergy ) and their altruistic behaviour is further determined by what had the fox , at his mercy
            done last time he met someone and hence i am multiplying the previous stratergy of that fox also.

            conclusively the fox which has defected will have less chance of food being shared with him 
            so he will probabily die out in the long run. 
        '''
        to_delete = []
        shared_food = 0
        #a,b = 0,0
        for i in range(len(self.agents)):
            agent = self.agents[i]
            # for every agent, check it's food and strategy if it has more food
            # Increase age
            agent.age+=1
            if agent.food<1 or agent.age>10:
                to_delete.append(i)
        for i in range(len(self.agents)):
            agent = self.agents[i]
            if to_delete != []:
                if agent.food>1:
                    j = np.random.choice(to_delete)
                    atmercy = self.agents[j]
                    if agent.clas == 'sp':
                        agent.choose_action(atmercy.strat_name,self.train)
                        #print('j:',j ,'agent',agent.strat_name , agent.id , agent.food,'atmercy',atmercy.strat_name , atmercy.id , atmercy.food)                        
                    if agent.strat != []:    # If agent stratergy is AC or AD or ALT
                        prob = (agent.size/(atmercy.size+agent.size))*agent.strat[0]*(atmercy.hist_strat[-1] if atmercy.hist_strat != [] else 1)
                        agent.strat.reverse() # this line alternates the strategy of ALT type since it 
                                              #reverses the list and puts the latest used strategy at back
                                              # which others will look at  while sharing food with him.
                    else:                    # If agent is using TFT strategy
                        #if atmercy.clas == 'sp':
                            #atmercy.choose_action(agent.strat_name,self.train)
                        prob = (agent.size/(atmercy.size+agent.size))*(atmercy.hist_strat[-1] if atmercy.hist_strat != [] else 0.8)
                    choices = ['share']*(int(prob*100))+['self']*(100-int(prob*100))
                    decision = np.random.choice(choices)
                    if decision=='share':

                        atmercy.food+=1
                        agent.food-=1
                        to_delete.remove(j)
                        if agent.food == 0:
                            to_delete.append(i)

        # Kill everyone who didn't get food and have aged.
        if len(to_delete)>0:
            for i in sorted(to_delete,reverse=True):
                pop_of_size[self.agents[i].size][-1] -= 1
                if self.agents[i].clas == 'sp':
                    pop_of_strat['none'][-1] -= 1
                    #self.sp_agentpop -= 1
                else:
                    pop_of_strat[self.agents[i].strat_name][-1] -= 1

                self.agents.pop(i)
                
        # reproduce
        for agent in self.agents:
            if agent.food>=2:
                #*agent.strat[0] if agent.strat !=[] else 0.5
                tok = int((self.reproductionChance)*100)
                choices=['reproduce']*(tok)+['sad']*(int(100-tok))
                decision=np.random.choice(choices)
                if decision == 'reproduce':
                    agent.food -= 2
                    if agent.clas == 'sp':
                        self.agents.append(special_Agent(agent.size,agent.Q))
                       # self.sp_agentpop += 1
                    else:
                        self.agents.append(Agent(agent.size,agent.strat_name))
                    self.curr_total_lived+=1
                    self.agents[-1].id = self.curr_total_lived
                    pop_of_size[self.agents[-1].size][-1] += 1
                    pop_of_strat[self.agents[-1].strat_name][-1] += 1
        self.__update()

        return

    def __update_Q(self,agents):
        pop_new = {'AC':0,'TFT':0,'ALT':0,'AD':0,'none':0}
        for agent in agents:
            if agent.clas == 'sp':
                pop_new['none'] += 1
            else:
                pop_new[agent.strat_name] += 1
        for agent in agents:
            if agent.clas == 'sp':
                for i,key in enumerate(pop_new.keys()):
                    if pop_new[key] > pop_of_strat[key][-1] and i<4:
                        agent.reward -= 1
                    elif i<4:
                        agent.reward += 1
                    elif i==4 and pop_new[key] > pop_of_strat[key][-1]:
                        agent.reward += 1
                    else:
                        agent.reward -= 1
                agent.update(pop_of_strat,len(self.agents))
                #print('updated: ', agent.strat_name,'hist:',agent.hist_strat , agent.id)
    def __resetFood(self):
        '''
            Private Method. reset Agent's food numbers and matrix.
        '''
        self.grid = self.__getEmptyMat()
        for agent in self.agents:
            agent.food=0

    def display(self,iterate):
        '''
            Private Method. Planned to use pygame to display grid.
            animation loop would be controlled from here.
        '''
        
        x = [i for i in range(iterate+1)]
        a = pop_of_size[2][:-1]
        b = pop_of_size[1][:-1]
        s1,s2,s3,s4,s5 = pop_of_strat.values()
        total = [a[i] + b[i] for i in range(iterate+1)]
        #plotting begins
        plt.figure(figsize = (15,13))
        plt.subplot(2,1,1)
        plt.title('size wise population')
        plt.plot(x,a,'ro-',label = 'Agent size: 2')
        plt.plot(x,b,'bo-',label = 'Agent size: 1')
        plt.plot(x,total,'go-',label = 'total Agents')
        plt.xticks(x)
        plt.legend(loc = 'best')

        plt.subplot(2,1,2)

        plt.title('strategy wise population')
        plt.plot(x,s1[:-1],'ro-',label = 'AC')
        plt.plot(x,s2[:-1],'bo-',label = 'TFT')
        plt.plot(x,s3[:-1],'ko-',label = 'ALT')
        plt.plot(x,s4[:-1],'go-',label = 'AD')
        plt.plot(x,s5[:-1],'mo-',label = 'intelligent')
        plt.legend(loc = 'upper left')
        plt.xticks(x)
        plt.show()
        return

    def iterate(self,t):
        '''
            Runs a single Iteration. Calls Internal methods in a 
            logical sequence. 
        '''
        self.__assignPosRand()
        self.__populateFood()
        self.__pickFood()
        self.__night()
        self.pop_hist.append(self.getPopNumber())
        if t:
            self.__update_Q(self.agents)
        self.__resetFood()
    def run(self, num_iterate, train=False):
        '''
            Runs the simulation for `num_iterate` iterations. 
        '''
        self.train = train
        #for i in range(len(self.agents)):
         #   print(self.agents[i].strat_name)
        for i in range(num_iterate):
            self.iterate(self.train)
            if not self.train:
                print(f'Iteration {i}/{num_iterate}: TotalPopulation = {self.pop_hist[-1]} , Bigfox = {pop_of_size[2][-1]} , Smallfox = {pop_of_size[1][-1]} , sp_fox = {pop_of_strat[num_to_strat[4]][-1]}')
            #, sp_fox = {pop_of_strat['none'][-1]}
        if not self.train:
            self.display(num_iterate)
    def getPopNumber(self):
        '''
            Print current population
        '''
        return len(self.agents)

def summary(table):
    keys = np.argmax(table,axis=1)
    for i,key in enumerate(keys):
        print('play ',num_to_strat[key],'against ',num_to_strat[i])
    return

"""# **Part B ( Q learning )**

**Training the Policy**
"""

# Initialize the Q-table with zeros 
print('Training begins ->')
Q_table = np.zeros((len(basket_of_strat),len(basket_of_strat)-1))
pop_of_strat = {'AC':[0],'TFT':[0],'ALT':[0],'AD':[0],'none':[0]}
pop_of_size = {1:[0],2:[0]}

# Create Env
num_agents = 100
foodperday = 5*num_agents
e = Environment(foodperday=500,repChance=0.5)
n = 44   #number of iterations

# Initializing agents
agents=[]
for i in range(num_agents):
    agents.append(Agent(1,'AD'))
for i in range(num_agents):
    agents.append(Agent(1,'AC'))
for i in range(num_agents):
    agents.append(Agent(1,'TFT'))
for i in range(num_agents):
    agents.append(Agent(1,'ALT'))
for i in range(num_agents):
    agents.append(special_Agent(1,Q_table))

# pass agents in the env
e.setup(agents)

# Run sim to train the agent/policy
for i in range(10):
    e.run(n,train=True)

# Get Current Population
print(e.getPopNumber())
print('Here is the summary of strategy learned')
summary(Q_table)
print("Training complete!")

"""**Testing the policy**"""
print('Testing the policy ->')
# Create Env
pop_of_strat = {'AC':[0],'TFT':[0],'ALT':[0],'AD':[0],'none':[0]}
pop_of_size = {1:[0],2:[0]}
n2 = 30 # number of agents of each type
foodperday = n2*5
e = Environment(foodperday=foodperday,repChance=0.5)
n = 44   #number of iterations
#Q_table = np.array([[0,0,0,1],
 #                   [1,0,0,0],
  #                  [1,0,0,0],
   #                 [0,1,0,0],
    #                [1,0,0,0]])
# Initializing agents

agents=[]
for i in range(n2):
    agents.append(Agent(2,'AD'))
for i in range(n2):
    agents.append(Agent(2,'AC'))
for i in range(n2):
    agents.append(Agent(2,'TFT'))
for i in range(n2):
    agents.append(Agent(2,'ALT'))
for i in range(n2):
    agents.append(special_Agent(2,Q_table))

# pass agents in the env
e.setup(agents)
# Run sim
e.run(n)
# Get Current Population
print(e.getPopNumber())
print(summary(Q_table),Q_table)

"""#  **Part A ( Behavioral Analysis )**

# Sim number 1 , TFT and AC dominant
"""
print("SIM 1 ->")
# Create Env
pop_of_strat = {'AC':[0],'TFT':[0],'ALT':[0],'AD':[0],'none':[0]}
pop_of_size = {1:[0],2:[0]}
e = Environment(foodperday=160,repChance=0.5)
n = 44   #number of iterations

# Initializing agents

agents=[]
for i in range(40):
    agents.append(Agent(2,'AD'))
for i in range(40):
    agents.append(Agent(2,'AC'))
for i in range(40):
    agents.append(Agent(2,'TFT'))
for i in range(40):
    agents.append(Agent(2,'ALT'))

# pass agents in the env
e.setup(agents)
# Run sim
e.run(n)
# Get Current Population
print(e.getPopNumber())

"""
# Sim number 2 , AD is dominant
"""
print("SIM 2 ->")
# In this one I am showing a condition where AD is most favourable.
# for this , eliminating the TFT type is important
# or else AD will get punished for non cooperation.
pop_of_strat = {'AC':[0],'TFT':[0],'ALT':[0],'AD':[0],'none':[0]}
pop_of_size = {1:[0],2:[0]}

e = Environment(foodperday=75,repChance=1)


n1 = 40   #number of iterations
n2 = 25   # number of agents of each type
# Initializing agents

agents=[]
for i in range(n2):
    agents.append(Agent(1,'AD'))
for i in range(n2):
    agents.append(Agent(2,'AC'))
#for i in range(n2):
 #   agents.append(Agent(1,'TFT'))
for i in range(n2):
    agents.append(Agent(2,'ALT'))


e.setup(agents)

e.run(n1)

e.getPopNumber()

"""# **Final Conclusion**

We know that TFT and AC can dominate sometimes and AD can dominate on other ocassions . Our agent learns how to handle each agent in each environment with satisfactory accuracy. for ex , it learns that TFT is to be played against AD and AC is to be played against TFT it also learns to cooperate with other sp agents. Sometimes it may happen that our agent doesn't perform well in training but it performs very well in testing.

# **Implementational Details**
In the second part of the project , we have tried to teach our "special Agent" how to deal with different strategies . Our sp. agent learns this through Q learning .For analysis we first train our agents i.e obtain the optimal strategy and then test it . The Q table is initialised with (states,actions) where states are defined as whichever agent is our sp. agent interacting at the time of sharing while actions are nothing but the strategies that it considers. Here one episode is one iteration i.e one day the Q table is global that means every sp agent will refer to this table for choosing the action . By this method ,we can gain large number of experiences which is n (no. of iterations ) * p (population of sp agent).

Rewards: our agent gets a positive reward if either the population of other agents gets low as compared to previous oteration or it's own population increases and vice-versa. thereby making the environment more competitive.

 We also get some drawbacks in this implementation .
Namely :

1.   ALT means nothing to the sp agent since it will change it's strategy in the next iteration and not get a chance to alternate .
2.   the current action doesn't lead to next state . That means there is no ralation between action taken and next state because the next state is only obtained in the next iteration and that is random. In other words, we cannot predict which agent is going to be 'atmercy' if we take a particular action . But we have tried to overcome this by randomising the probability of next state according to the population of the herd .Take a look at it .
```        
prob = [0.0,0.0,0.0,0.0,0.0]
for key in pop_of_strat.keys():
        prob[strat_to_num[key]] = float(pop_of_strat[key][-1])/len
return random.choices(strat_names,prob)[0]
```

\* len is the total population while pop_of_strat gives us the info on population, strategy wise.

So we have assumed that the next state is approximately correct and therefore we can conclude that our RL agent learns to survive accordingly.
"""
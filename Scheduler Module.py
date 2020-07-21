import numpy as np 
import scipy as sp 
import matplotlib.pyplot as plt
import numpy as np
import copy



def HPF(process,cs):
    ta=list()
    ta.append(process[0][2])
    wta=list()
    wta.append(1.0)
    waiting=list()
    waiting.append(0.0)
    p=list()
    p.append(process[0])
    timer= cs+ta[0]+p[0][1]
    del(process[0])

    while len(process)!=0:
        ready= [i for i in process if i[1]<=timer]
    
        ready =sortp(ready)
        #print(ready,timer)
        if len(ready)==0:
            timer+=1
            continue
        p.append(ready[-1])
        ta.append(timer+ready[-1][2]-ready[-1][1])
        wta.append((ta[-1]/ready[-1][2]))
        waiting.append((ta[-1]-ready[-1][2]))
        timer+=cs+ready[-1][2]
        process.remove(ready[-1])

    return p,ta,wta,waiting

def FCFS (process,cs):
    ta=list()
    ta.append(process[0][2])
    wta=list()
    wta.append(1.0)
    waiting=list()
    waiting.append(0.0)
    clock=process[0][2]+process[0][1]+cs
    for i in range (1,len(process)):
        if clock >= process[i][1]:
            ta.append(clock+process[i][2]-process[i][1])
            clock+=process[i][2]+cs
        else:
            clock=process[i][1]
            ta.append(clock+process[i][2]-process[i][1])
            clock+=process[i][2]+cs

        wta.append(ta[i]/process[i][2])
        waiting.append(ta[i]-process[i][2])

    return process,ta,wta,waiting

def RR(process_original,cs,Q):
    process = copy.deepcopy(process_original)
    return_p = list()
    ta =  np.zeros([1,len(process)])[0]
    wta = np.zeros([1,len(process)])[0]
    waiting = np.zeros([1,len(process)])[0]
    current_t = process[0][1]
    i=0
    while len(process)>0:
        if i >= len(process):
            i=0
        elif process[i][1] > current_t:
            if len(process)==1:
                current_t = process[0][1]
            else:
                i+=1
                continue
                
        if process[i][2]<=Q:
            x = [process[i][0],process[i][1],process[i][2],process[i][3]]
            current_t += process[i][2]
            p = int(process[i][0])-1
            ta[p] = current_t -process[i][1]
            wta[p] = ta[p]/process_original[i][2]
            waiting[p]= ta[p] - process_original[i][2]
            del process[i] 
            del process_original[i] 
            return_p.append(x)
            i-=1
            
        else:
            x = [process[i][0],process[i][1],Q,process[i][3]]
            return_p.append(x)
            process[i][2]-=Q
            current_t+=Q
            
        if i+1<len(process) and process[i+1][1]<=current_t:
            current_t+=cs
            
        i+=1 
    return return_p,ta,wta,waiting


def SRTN(process_original,cs):
    process = copy.deepcopy(process_original)
    return_p = list()
    ta =  np.zeros([1,len(process)])[0]
    wta = np.zeros([1,len(process)])[0]
    waiting = np.zeros([1,len(process)])[0]
    current_t = process[0][1]
    srtn =0
    flag1 = 0
    flag2 = 0
    while len(process)>0:
        print(process)
        print(current_t)
        
        if process[srtn][1]>current_t:
            current_t = process[srtn][1]
        for j in range(1,len(process)):
            if process[j][1] > current_t:
                break
            if(process[srtn][2]>process[j][2]):
                srtn = j
                flag1 = 1
                
        
        if flag1 == 1 or flag2 == 1:
            current_t+=cs
            flag1 = 0
            flag2 = 0    
        x = [process[srtn][0],process[srtn][1],1,process[srtn][3]]
        return_p.append(x)
        process[srtn][2]-=1
        current_t+=1
        if process[srtn][2] == 0:
            p = int(process[srtn][0])-1
            ta[p] = current_t -process[srtn][1]
            wta[p] = ta[p]/process_original[srtn][2]
            waiting[p]= ta[p] - process_original[srtn][2]
            del process_original[srtn]
            del process[srtn]
            srtn=0
            if len(process) > 0 and process[srtn][1]<=current_t+1:
                flag2 = 1
            
       
        
    print(ta)
    print(wta)
    print(waiting)
        
    return return_p,ta,wta,waiting



##################sorting Priorty####################     

def lastp(n): 
    return n[3]   
      
def sortp(tuples): 
    return sorted(tuples, key = lastp) 
###########################################
##################sorting Arrival time ####################     

def last(n): 
    return n[1]   
      
def sort(tuples): 
    return sorted(tuples, key = last) 
###########################################

##########################################################
#########################plot my graph####################
##########################################################

def draw(data,cs,algo):
    current_t =0
    time = []
    end = []
    process = []
    
    #start my graph
    time.append(0)
    time.append(data[0][1])
    process.append(-1)
    process.append(-1)
    
    for i in range(0,len(data)):
        arrival_t = abs(data[i][1])
        burst_t = abs(data[i][2])
        process_id = abs(data[i][0])
        if arrival_t >= current_t:
            process.pop()
            process.append(-1)
            time[len(time)-1]-=cs
            current_t = arrival_t
            time.append(arrival_t)
            process.append(-1)
        time.append(current_t)
        time.append(current_t + burst_t)
        process.append(process_id)
        process.append(process_id)
        
        #cs time
        if (i+1 < len(data) and data[i+1][0] != process_id):
            time.append(current_t + burst_t)
            time.append(current_t + burst_t + cs)
            process.append(0)
            process.append(0)
            current_t+=cs
            
        if  i+1 == len(data):
            time.append(current_t + burst_t)
            process.append(-1)
        current_t = current_t + burst_t 
  
    plt.plot(time, process)  
    plt.xlabel('time - axis')  
    plt.ylabel('process - axis')  
    plt.title(algo) 
    plt.grid()
 
    plt.show() 
    return
###########################################


def main():
    filename=input("Enter File Name \n")
    

    try:
        file = open(filename, "r")
    except IOError:
        print("Error: File does not appear to exist ! \n")
        return


    stat= open("solution.txt", "a")

    f_list = [float(i) for line in file for i in line.split(' ') if i.strip()]
   
    process=list()

    for i in range(1,len(f_list),4):
        x=[f_list[i],int(abs(f_list[i+1])),int(abs(f_list[i+2])),int(abs(f_list[i+3]))]
        process.append(x)
    process=sort(process)
   
    algo = -1
    while algo != 1 and algo !=2 and algo !=3 and algo !=4: 
        algo =abs(int(input("Select one of scheduling algorithms \n"+
                    "\"Enter the number of the algorithm\"\n"+
                    "1 - HPF \n"+
                    "2 - FCFS\n"+
                    "3 - RR\n"+
                    "4 - SRTN\n ")))
        if algo != 1 and algo !=2 and algo !=3 and algo !=4:
            print("Invalid input !\n")
            
    cs=abs(int(input("Context Switching time \n")))
    algo_name = ""
    if algo == 1:
        to_be_print,ta,wta,waiting=HPF (process,cs)
        algo_name ="HPF"
        print(ta)
        print(wta)
        print(waiting)
    elif algo ==2:
        to_be_print,ta,wta,waiting=FCFS (process,cs)
        algo_name ="FCFS"
    elif algo==3:
        Q = input("Enter your time quantum\n")
        to_be_print,ta,wta,waiting = RR(process,cs,int(Q))
        algo_name ="RR with Q = "+Q
    else:
        to_be_print,ta,wta,waiting=SRTN(process,cs)
        algo_name ="SRTN"
    
    #print(to_be_print)
    for i in range(0,len(to_be_print)-1):
	print((to_be_print)-1)
        stat.write("process #"+str(int(to_be_print[i][0]))+" "+str(ta[i])+" "+str(wta[i])+" "+str(waiting[i])+"\n")

    stat.write("Average Turnaround Time = "+str(sum(ta)/len(ta))+"\n")
    stat.write("Average Weighted Turnaround Time = "+str(sum(wta)/len(wta))+"\n")
    
    #draw
    draw(to_be_print,cs,algo_name)

if __name__== "__main__" :
    main()

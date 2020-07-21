import numpy as np 
import scipy as sp 

filename=input("Enter File Name \n")
file = open(filename, "r")
output= open("output.txt", "a")

#split input data
f_list = [float(i) for line in file for i in line.split(' ') if i.strip()]

Num_process=int(f_list[0])
mu1, sigma1=f_list[1],f_list[2]
mu2, sigma2=f_list[3],f_list[4]
lam=f_list[5]

# generate random arrival time, burst_time and Priority to number of processes 
arrival_time=np.random.normal(mu1, sigma1, Num_process)
burst_time=np.random.normal(mu2, sigma2,Num_process )
Priority=sp.random.poisson(lam=lam, size=Num_process) 

# write the output in file for using it then in simulation 
output.write(str(Num_process)+"\n")
for i in range(0,Num_process):
    output.write(str(i)+" "+str(int(abs(arrival_time[i])))+" "+str(int(abs(burst_time[i])))+" "+str(int ( abs(Priority[i])))+"\n")

import numpy
import time
import math

FLP = 'k_center_ss'

all_data = [] 
for line in open('1000x4000.txt'):
    data = line.strip('\n').split('\t')
    for i in range(len(data)):
        if data[i] != '':
            all_data.append(float(data[i]))
        
allfacilities = int(all_data[0])
allcustomers = int(all_data[1])

c_all,d_all,o_all,t_all = [],[],[],[]
for i in range(2,allcustomers+2):
    d_all.append(int(all_data[i]))

for i in range(allcustomers+2, allcustomers+2+allfacilities):
    c_all.append(math.floor(all_data[i]))

for i in range(allcustomers+2+allfacilities, allcustomers+2+2*allfacilities):
    o_all.append(all_data[i])

for j in range(allfacilities):
    row=[]
    for i in range(allcustomers+2+2*allfacilities+j*allcustomers,allcustomers+2+2*allfacilities+(j+1)*allcustomers):
        row.append(all_data[i])
    t_all.append(row)
t_all = numpy.transpose(t_all)

customers = 25
facilities = 250
d = d_all[:customers]
c = c_all[:facilities]
o = o_all[:facilities]

t = []
for i in range(customers):
    row=[]
    for j in range(facilities):
        row.append(t_all[i][j])
    t.append(row)
      
tstart = time.time()

if FLP == 'k_center_ms':
    d_copy = d.copy()
    t_copy = numpy.array(t)                 
    dist_of_demands = numpy.zeros((customers,facilities), dtype = int)
    
    while sum(d_copy) > 0: 
        # sorting customers according to min_t (decreasing order)
        min_t = numpy.amin(t, axis=1)
        indices = sorted(range(len(min_t)), key=min_t.__getitem__,reverse=True)
        for i in range(customers):
            cust = indices[i]
            if d_copy[cust] > 0: 
                minimum = 1000000
                ind = 0
                for j in range(facilities):
                    if t_copy[cust,j] + t_copy[cust,j]*dist_of_demands[cust][j] < minimum:
                        minimum = t_copy[cust,j] + t_copy[cust,j]*dist_of_demands[cust][j]
                        ind = j 
                c[ind] -= 1
                d_copy[cust] -= 1
                dist_of_demands[cust][ind] += 1
                if c[ind] == 0:
                    for z in range(customers):
                        t_copy[z,ind] = 1000000 #some value larger than all transportation costs  #update
    
    list_opened_facilities = []
    for j in range(facilities):
        sum_supply = 0
        for i in range(customers):
            sum_supply += dist_of_demands[i][j]
        if sum_supply > 0:
            list_opened_facilities.append(j+1)
    
    tend = time.time()
    dtimest = numpy.multiply(dist_of_demands,t)
    print("Objective = ",numpy.max(dtimest))
    print("Opened Facilities:")
    print(list_opened_facilities)
    print('k ', len(list_opened_facilities))
    print("Time Taken = ",tend-tstart)
    for i in range(customers):
        for j in range(facilities):
            if dist_of_demands[i][j] > 0:
                print(str(i+1), str(j+1), str(dist_of_demands[i][j]))
                
elif FLP == 'k_center_ss':
    # finding order in which to serve customers (decreasing demands)    
    indices = sorted(range(len(d)), key=d.__getitem__,reverse=True)
        
    # saving vector of demands in decreasing order 
    d_copy_sorted = d.copy()
    d_copy_sorted.sort(reverse = True)  
    
    t_copy = numpy.array(t)       
    
    # updating matrix t_copy
    dist_of_demands = numpy.zeros((customers,facilities), dtype = int)
    for j in range(facilities):    
        for i in range(customers):
            if c[j] < d_copy_sorted[i]:
                t_copy[indices[i],j] = 1000000  #not enough capacity to satisfy demand
            else:
                break  
       
    for i in indices:          
         min_t = numpy.amin(t_copy, axis=1)[i]
         ind = numpy.argmin(t_copy, axis=1)[i]                   
         c[ind] -= d[i]
         for k in range(customers):
                if c[ind] < d_copy_sorted[k]:
                    t_copy[indices[k],ind] = 1000000
                else:
                    break
         dist_of_demands[i,ind] = d[i]   
       
    list_opened_facilities = []
    for j in range(facilities):
        sum = 0
        for i in range(customers):
            sum += dist_of_demands[i][j]
        if sum > 0:
            list_opened_facilities.append(j+1)
             
    tend = time.time()
    dtimest = numpy.multiply(dist_of_demands,t)
    print("Objective = ",numpy.max(dtimest))
    print("Number of opened facilities: ", len(list_opened_facilities))
    print("Opened Facilities:")
    print(list_opened_facilities)
    print("Time Taken = ",tend-tstart)
    for i in range(customers):
        for j in range(facilities):
            if dist_of_demands[i][j] > 0:
                print(str(i+1), str(j+1), str(dist_of_demands[i][j]))
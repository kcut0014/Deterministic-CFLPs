#new data format

import gurobipy as grb
import numpy

k=15

kmedianms = grb.Model("k median multi-source FLP")    

b, o, c, d, t = [], [], [], [], []

#------------------------------------------------------------------------------------------------------------------------

all_data = [] 
for line in open('1000x4000.txt'):
    data = line.strip('\n').split('\t')
    for i in range(len(data)):
        if data[i] != '':
            all_data.append(float(data[i]))
        
print(all_data[-1])     # printing last element in all_data
    
allfacilities = int(all_data[0])
allcustomers = int(all_data[1])
customers = 50
facilities = 250 # data set considers only till 1000 facilities


print('facilities = ', facilities)
print('customers = ', customers)

for i in range(2,allcustomers+2):
    d.append(all_data[i])

for i in range(allcustomers+2, allcustomers+2+allfacilities):
    c.append(all_data[i])

for i in range(allcustomers+2+allfacilities, allcustomers+2+2*allfacilities):
    o.append(all_data[i])

for j in range(allfacilities):
    row=[]
    for i in range(allcustomers+2+2*allfacilities+j*allcustomers,allcustomers+2+2*allfacilities+(j+1)*allcustomers):
        row.append(all_data[i])
    t.append(row)

t = numpy.transpose(t)    
print(t.max())
print(t.min())
print(numpy.median(t))
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

# #k center single source

# x,y ={},{}

# z = {}           
# z = kcenterss.addVar(vtype=grb.GRB.CONTINUOUS, name = "z")
  
# for j in range(facilities):
#     x[j] = kcenterss.addVar(vtype = grb.GRB.BINARY, name = "x[%s]"%(j+1))     #decision variable if facility is open or not
#     for i in range(customers):
#         y[i,j] = kcenterss.addVar(vtype = grb.GRB.BINARY, name = "y[%s,%s]"%((i+1),(j+1)))   #demand of customer i satisfied by facility j 
  
# kcenterss.addConstr(grb.quicksum(x[j] for j in range(facilities)) == k)

# for i in range(customers):
#     kcenterss.addConstr(grb.quicksum(y[i,j] for j in range(facilities)) == 1)
    
# for j in range(facilities):
#     kcenterss.addConstr(grb.quicksum(d[i]*y[i,j] for i in range(customers)) <= c[j]*x[j])
#     for i in range(customers):    
#         kcenterss.addConstr(z >= d[i]*t[i][j]*y[i,j])

# objective = z

# kcenterss.ModelSense = grb.GRB.MINIMIZE
# kcenterss.setObjective(objective)
# kcenterss.update()
# kcenterss.optimize()

# for j in kcenterss.getVars():
#     if(j.x>0): print('%s %g ' %(j.varName,j.x))
    
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

# # k center multi source

# x,dem = {},{}

# z = {} 
# z = kcenterms.addVar(vtype=grb.GRB.CONTINUOUS, name = "z")
  
# for j in range(facilities):
#     x[j] = kcenterms.addVar(vtype = grb.GRB.BINARY, name = "x[%s]"%(j+1))     #decision variable if facility is open or not
#     for i in range(customers):
#         dem[i,j] = kcenterms.addVar(vtype = grb.GRB.INTEGER, name = "dem[%s,%s]"%((i+1),(j+1)))   #some units of the demand d_i

# kcenterms.addConstr(grb.quicksum(x[j] for j in range(facilities)) == k)

# for i in range(customers):
#     kcenterms.addConstr(grb.quicksum(dem[i,j] for j in range(facilities)) == d[i])

# for j in range(facilities):
#     kcenterms.addConstr(grb.quicksum(dem[i,j] for i in range(customers)) <= c[j]*x[j])

# for i in range(customers):
#     for j in range(facilities):
#         kcenterms.addConstr(z >= t[i][j]*dem[i,j])

# objective = z 

# kcenterms.ModelSense = grb.GRB.MINIMIZE
# kcenterms.setObjective(objective)
# kcenterms.update()
# kcenterms.optimize()

# for j in kcenterms.getVars():
#     if(j.x>0): print('%s %g ' %(j.varName,j.x))


#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

# #k median single source

# x,y ={},{}
# for j in range(facilities):
#     x[j] = kmedianss.addVar(vtype = grb.GRB.BINARY, name = "x[%s]"%(j+1))     #decision variable if facility is open or not
#     for i in range(customers):
#         y[i,j] = kmedianss.addVar(vtype = grb.GRB.BINARY, name = "y[%s,%s]"%((i+1),(j+1)))   #demand of customer i satisfied by facility j 
        
# kmedianss.addConstr(grb.quicksum(x[j] for j in range(facilities)) == k)

# for i in range(customers):
#     kmedianss.addConstr(grb.quicksum(y[i,j] for j in range(facilities)) == 1)
    
# for j in range(facilities):
#     kmedianss.addConstr(grb.quicksum(d[i]*y[i,j] for i in range(customers)) <= c[j]*x[j])
    
# objective = grb.quicksum(d[i]*t[i][j]*y[i,j] for i in range(customers) for j in range(facilities)) + grb.quicksum(o[j]*x[j] for j in range(facilities))

# kmedianss.ModelSense = grb.GRB.MINIMIZE
# kmedianss.setObjective(objective)
# kmedianss.update()
# kmedianss.optimize()

# for j in kmedianss.getVars():
#     if(j.x>0): print('%s %g ' %(j.varName,j.x))

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
# k median multi source

#defining the variables
x,dem={},{}

for j in range(facilities):
    x[j] = kmedianms.addVar(vtype = grb.GRB.BINARY, name = "x[%s]"%(j+1)) #decision variable if facility is open or not
    for i in range(customers):
        dem[i,j] = kmedianms.addVar(vtype = grb.GRB.INTEGER, name = "dem[%s,%s]"%((i+1),(j+1))) #some units of the demand d_i

kmedianms.addConstr(grb.quicksum(x[j] for j in range(facilities)) == k)

for i in range(customers):
    kmedianms.addConstr(grb.quicksum(dem[i,j] for j in range(facilities)) == d[i])

for j in range(facilities):
    kmedianms.addConstr(grb.quicksum(dem[i,j] for i in range(customers)) <= c[j]*x[j])

objective = grb.quicksum(t[i][j]*dem[i,j] for i in range(customers) for j in range(facilities)) + grb.quicksum(o[j]*x[j] for j in range(facilities))

kmedianms.ModelSense = grb.GRB.MINIMIZE
kmedianms.setObjective(objective)
kmedianms.update()
kmedianms.optimize()

for j in kmedianms.getVars():
    if(j.x>0): print('%s %g ' %(j.varName,j.x))
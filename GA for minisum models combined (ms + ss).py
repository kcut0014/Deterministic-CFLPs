import random as rnd
import numpy
import time
import operator
import math

size = 30
best_sample = 10
lucky_few = 10
chance_of_mutation = 2
solution_dic={}

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

FLP = 'k_median_ms'
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

def convert_x_to_int(stringx):
    listx = list(stringx)
    listx= [int(value) for value in listx]
    return listx

def convert_x_to_string(x):
    stringx = ""
    for value in x:
        stringx += str(value)
    return stringx

if FLP == 'k_median_ms':

    def is_feasible(stringx):
        x = convert_x_to_int(stringx)
        demands = sum(d)
        capacities = sum(list(map(operator.mul, c, x)))
        return capacities >= demands
    
    def generate_first_random_feasible_soln():
        x_all_closed = [0 for j in range(facilities)]
        for i in range(1,facilities+1):          
            list_random = rnd.sample(range(1, facilities + 1),i)
            x = x_all_closed.copy()
            for value in list_random:
                x[value-1] = 1
            if(is_feasible(x)):
                return convert_x_to_string(x)
               
    indices = sorted(range(len(d)), key=d.__getitem__,reverse=True)   
            
    def fitness_kmedian_ms(stringx):
        x = convert_x_to_int(stringx)
        c_copy = c.copy()
        d_copy = d.copy()
        t_copy = numpy.array(t)                 
    
        dist_of_demands = numpy.zeros((customers,facilities), dtype = int)
        total = 0
        for j in range(facilities):
            if x[j] == 0:                
                c_copy[j] = 0
                for i in range(customers):
                    t_copy[i,j] = 1000000 
         
        for i in range(customers):
            cust = indices[i]
            demand_satisfied = False
            while demand_satisfied == False:
                minimum = 1000000
                ind = 0
                for j in range(facilities):
                    if t_copy[cust,j] < minimum:
                        minimum = t_copy[cust,j]
                        ind = j 
                if d_copy[cust] <= c_copy[ind]:
                    total += t_copy[cust,ind]*d_copy[cust]
                    c_copy[ind] -= d_copy[cust]
                    dist_of_demands[cust][ind] = d_copy[cust]
                    demand_satisfied = True
                else:
                    total += t_copy[cust,ind]*c_copy[ind] 
                    d_copy[cust] -= c_copy[ind] 
                    dist_of_demands[cust,ind] = c_copy[ind] 
                    c_copy[ind] = 0 
                    for z in range(customers):
                        t_copy[z,ind] = 1000000 
                    demand_satisfied = d_copy[cust] == 0
        
        for j in range(facilities):
            if x[j] == 1:
                sum = 0
                for i in range(customers):
                    sum += dist_of_demands[i][j]
                if sum == 0:
                    x[j] = 0
                else:
                    total += o[j]
        newx = convert_x_to_string(x)
                 
        return total, dist_of_demands, newx
    
elif FLP == 'k_median_ss':
    indices = sorted(range(len(d)), key=d.__getitem__,reverse=True)
    d_copy_sorted = d.copy()
    d_copy_sorted.sort(reverse = True)  
    
    def initial_is_feasible(stringx):
        x = convert_x_to_int(stringx)
        demands = sum(d)
        capacities = sum(list(map(operator.mul, c, x)))
        return capacities >= demands
    
    def is_feasible(stringx):
            x = convert_x_to_int(stringx)
            c_copy = c.copy()
            t_copy = numpy.array(t)       
            
            # updating matrix t_copy
            dist_of_demands = numpy.zeros((customers,facilities), dtype = int)
            for j in range(facilities):    
                if x[j] == 0:                #facility not selected, its capacity should be 0
                    c_copy[j] = 0
                    t_copy[:,j] = 1000000    #some value larger than all transportation costs
                else:
                    for i in range(customers):
                        if c_copy[j] < d_copy_sorted[i]:
                            t_copy[indices[i],j] = 1000000  #not enough capacity to satisfy demand
                        else:
                            break  
       
            total = 0
            for i in range(customers): 
                 cust = indices[i]
                 minimum = 1000000
                 ind = 0
                 for j in range(facilities):
                    if t_copy[cust,j] < minimum:
                        minimum = t_copy[cust,j]
                        ind = j 
                 if minimum == 1000000:
                     return False, stringx
                        
                 c_copy[ind] -= d[cust]
                 for k in range(i+1,customers):
                        if c_copy[ind] < d_copy_sorted[k]:
                            t_copy[indices[k],ind] = 1000000
                        else:
                            break
                 dist_of_demands[cust,ind] = d[cust]        
                 total += t_copy[cust,ind]*d[cust] 
    
            for j in range(facilities):
                if x[j] == 1:
                    sum = 0
                    for i in range(customers):
                        sum += dist_of_demands[i][j]
                    if sum == 0:
                        x[j] = 0    
                    else:
                        total += o[j]
            newx = convert_x_to_string(x)
            solution_dic[newx] = total, dist_of_demands           
            return True, newx
               
    def generate_first_random_feasible_soln():
        x_all_closed = [0 for j in range(facilities)]
        for i in range(1,facilities+1): 
            list_random = rnd.sample(range(1, facilities + 1),i)
            x = x_all_closed.copy()
            for value in list_random:
                x[value-1] = 1
            if(initial_is_feasible(x)):
                feasible, stringx = is_feasible(x) 
                if(feasible == True):
                    return stringx    

def generate_first_population():
    population = []
    for i in range(size):
        sol_exists = True
        while(sol_exists):
            new_sol = generate_first_random_feasible_soln()
            sol_exists = new_sol in population
        population.append(new_sol)      
    return population

if FLP == 'k_median_ms':
    def compute_fitness_population(population):
        population_fitness = {}
        for individual in population:
            if(individual in solution_dic):
                population_fitness[individual] = solution_dic[individual]
            else:
                total, matrix, newx = fitness_kmedian_ms(individual)
                individual = newx
                population_fitness[individual] = total
                solution_dic[individual] = population_fitness[individual]
        return sorted(population_fitness.items(), key = operator.itemgetter(1), reverse = False) 

elif FLP == 'k_median_ss': 
    def compute_fitness_population(population):
        population_fitness = {}
        for individual in population:
            population_fitness[individual] = solution_dic[individual][0]
        return sorted(population_fitness.items(), key = operator.itemgetter(1), reverse = False)    

def select_from_population(population_sorted):
    next_generation = []
    population_array = numpy.array(population_sorted)[:,0].tolist()
    population_array.reverse()
    for i in range(best_sample):
        next_generation.append(population_array.pop(-1))
    for i in range(lucky_few):
        selected_sol = rnd.choice(population_array)
        next_generation.append(selected_sol)
        population_array.remove(selected_sol)
    return next_generation

if FLP == 'k_median_ms':
    def create_child(individual1,individual2):
        child_is_feasible = False
        while child_is_feasible == False:
            child = ''
            for i in range(len(individual1)):
                number = int(100*rnd.random())
                if number < 50:
                    child += individual1[i]
                else:
                    child += individual2[i]
            child_is_feasible = is_feasible(child)
        return child

elif FLP == 'k_median_ss':
    def create_child(individual1,individual2):
        child_is_feasible = False
        while child_is_feasible == False:
            child = ''
            for i in range(len(individual1)):
                number = int(100*rnd.random())
                if number < 50:
                    child += individual1[i]
                else:
                    child += individual2[i]
            if(initial_is_feasible(child)):               
                child_is_feasible, new_child = is_feasible(child)
        return new_child

def create_children(breeders):
    next_population =[]
    next_population.extend(breeders[:best_sample]) 
    for i in range(size - best_sample):
            child_exists = True
            while child_exists:
                random_breeders = rnd.choices(breeders, k = 2)
                new_child = create_child(random_breeders[0], random_breeders[1])
                child_exists = new_child in next_population
            next_population.append(new_child)
    return next_population

def mutate_population(population):
    for i in range(len(population)):
        r = rnd.random()*100
        if r < chance_of_mutation:
            new_sol = generate_first_random_feasible_soln()     
            mutated_sol_exists = new_sol in population
            if mutated_sol_exists == False:
                population[i] = new_sol
    return population

def next_generation(first_generation):
    population_sorted = compute_fitness_population(first_generation)
    next_breeders = select_from_population(population_sorted)
    next_population = create_children(next_breeders)
    next_generation = mutate_population(next_population)
    return next_generation

def multiple_generation():
    historic = []
    historic.append(generate_first_population())
    tstart = time.time()
    gen_count = 0
    while(time.time() - tstart <= 7200):
        print("Generation Number =",gen_count+1)
        historic.append(next_generation(historic[gen_count]))
        gen_count += 1
    return historic

def get_best_individual_from_population(population):
    return compute_fitness_population(population)[0]

def get_list_best_individual_from_history(historic):
    best_individuals = []
    for population in historic:
        individual = get_best_individual_from_population(population) 
        if individual not in best_individuals:      
            best_individuals.append(get_best_individual_from_population(population))
    return best_individuals

if FLP == 'k_median_ms':
    def best_of_best(historic):     
        listofbest = get_list_best_individual_from_history(historic)
        listofbest.sort(key=operator.itemgetter(1))    
        overall_best_fitness = listofbest[0][1]
        for individual in listofbest:
            if individual[1] == overall_best_fitness:
                soln = list(str(individual[0]))
                soln = [int(x) for x in soln]
                indices_opened = []
                for i in range(len(soln)):
                  if soln[i] == 1:
                      indices_opened.append(i+1)
                print()
                print(indices_opened)
                print("k: " + str(sum(soln)), "fitness: " + str(individual[1]))
                matrix = fitness_kmedian_ms(str(individual[0]))[1]
                for i in range(customers):
                    for j in range(facilities):
                        if matrix[i][j] > 0:
                            print(str(i+1), str(j+1), str(matrix[i][j]))          
            else:
                break

elif FLP == 'k_median_ss':
    def best_of_best(historic):     #best over all populations
        listofbest = get_list_best_individual_from_history(historic)
        listofbest.sort(key=operator.itemgetter(1))    
        overall_best_fitness = listofbest[0][1]
        for individual in listofbest:
            if individual[1] == overall_best_fitness:
                soln = list(str(individual[0]))
                soln = [int(x) for x in soln]
                indices_opened = []
                for i in range(len(soln)):
                  if soln[i] == 1:
                      indices_opened.append(i+1)
                print()
                print(indices_opened)
                print("k: " + str(sum(soln)), "fitness: " + str(individual[1]))
                matrix = solution_dic[individual[0]][1]
                for i in range(customers):
                    for j in range(facilities):
                        if matrix[i][j] > 0:
                            print(str(i+1), str(j+1), str(matrix[i][j]))          
            else:
                break    

def genetic_algorithm():
    historic = multiple_generation()
    best_of_best(historic)

def seeds():
    for seed_number in range(3):   
        rnd.seed(seed_number)
        print('seed :', seed_number)
        genetic_algorithm()
        print('-------------------------------------------------------------------------------------------------------------')

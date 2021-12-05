""" 
Main function to use in other scripts: find_all_paths
Given the list of coordinates for starting position, obstacle vertices and goal position,
create a visibility graph that can later be explored.

Inputs:
    - list_vertices = [[v1.1, v1.2, ..., v1.N1], [v2.1, ..., v2.N2], ..., [vO.1, ..., vO.NO]]
    where O is the total number of obstacles,
    N1,N2,...,NO is the number of vertices for obstacles 1,2,...,O
    vk.1, vk.2,...,vk.Nk are tuples (x,y) with coordinates of k-th obstacle's vertices
    
    - start = (xstart, ystart) is the initial coordinates of Thymio
    
    - goal = (xgoal, ygoal) is the goal coordinates
    
Outputs:
    - list_neighbours = [ngb_start,ngb_1, ..., ngb_N, ngb_goal]
    
    where ngb_start = [(name_1, dist_1), (name_2, dist_2), ..., (name_L, dist_L)]
    with name_i the name of i-th neighbour of start, and dist_i its distance from start
    (and so on with ngb_1, ngb2, ..., ngb_N, ngb_goal)
    Here, N is the total number of obstacles' vertices.

"""


import math
import check_intersection #credits: Ansh Riyal, https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/ (cons. 27.11.2021)


def find_all_paths(list_vertices, start, goal):
    # 1. Initialisation
    
    #transform list_vertices into a list of all points including start & goal. 
    #store them without any distinction between obstacles/start/goal
    #every entry is an instance of class Point (see check_intersection.py)
    list_points = flatten_list_points(list_vertices, start, goal)
    N = len(list_points) - 2    #number of obstacle vertices
    
    #extract list_sides, the list of all obstacle sides e.g. (vertex1,vertex2),(vertex2,vertex3),etc
    #list_sides is grouped by obstacle:  list_sides = [[obstacle1.sides], [obstacle2.sides], ...]
    list_sides = obtain_list_sides(list_vertices) 



    # 2. Search algorithm
    # Determine for each point, what other points it can "see"
    # or in other terms, what connections are considered as valid    
    
    # There are 5 possibilities with our type of obstacles, implemented in code:
        # 1. (point1,point2) is a side of the obstacle --> valid connection
        # 2. both points lie on the obstacle, but (point1,point2) is not a side of the obstacle --> not valid
        # 3. 1st & 2nd condition false, and at least one of the points is equal to a vertex being tested --> valid
        # 4. other conditions false, and (point1,point2) intersects (vertex1, vertex2) --> not valid
        # 5. after testing, none of these conditions are fulfilled --> valid
    
    dist = lambda x1,y1,x2,y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    list_neighbours = []                        #final output: list of neighbours of all points
    for point1_name in range(N+2):
        ngb_current_point = []                  #list of neighbours of the current point
        
        for point2_name in range(N+2):
            if point1_name==point2_name:        #do not check self-connection
                pass
            
            
            else:
                point1 = list_points[point1_name]
                point2 = list_points[point2_name]
                valid_connection = True         #valid until proven wrong
                
                #Test the 5 conditions listed above
                for obstacle in list_sides:
                    obstacle_flattened = [item for sublist in obstacle for item in sublist]
                    
                    
                    condition1 = (((point1_name,point2_name) in obstacle)\
                                  or ((point2_name,point1_name) in obstacle))
                        
                    condition2 = ((point1_name in obstacle_flattened)\
                                  and (point2_name in obstacle_flattened))
                    
                    if condition1:     
                        pass
                        
                    elif condition2:        
                        valid_connection = False                        
                        
                    else:
                        for side_vertices in obstacle:
                            vertex1_name = side_vertices[0]
                            vertex2_name = side_vertices[1]
                            vertex1 = list_points[vertex1_name]
                            vertex2 = list_points[vertex2_name]
                            
                            
                            condition3 = ((point1_name==vertex1_name) or (point2_name==vertex2_name)\
                                or (point2_name==vertex1_name) or (point1_name==vertex2_name))
                            
                            condition4 = check_intersection.doIntersect(point1, point2, vertex1, vertex2)
                                
                            
                            if condition3:         
                                    pass
                                    
                            elif condition4:          
                                    valid_connection = False
                               
                            #else: condition5=True ; pass
                          
                
                
                if valid_connection:
                    ngb_current_point.append((point2_name, dist(point1.x, point1.y, point2.x, point2.y)))
        
        list_neighbours.append(ngb_current_point)
        
    return list_neighbours


#%%
def flatten_list_points(list_vertices, start, goal):
    """
    Returns a "flat" (i.e. list without sublists or tuples) version of
    all point coordinates including start and goal.
    Each entry is an instance of class check_intersection.Point
    
    Inputs: as in find_all_paths
    Outputs:
        list_points = [Point0, Point1, Point2, ..., PointN, Point(N+1)]
        where all entries are of class check_intersection.Point, 
        Point0 corresponds to start and Point(N+1) corresponds to goal.
    """    
    
    list_points = []         
    for obstacle in range(len(list_vertices)):
        for vertex in range(len(list_vertices[obstacle])):
            x = list_vertices[obstacle][vertex][0]
            y = list_vertices[obstacle][vertex][1]
            list_points.append(check_intersection.Point(x,y))                   #insert obstacle vertices
                                                            
    list_points.insert(0, check_intersection.Point(start[0],start[1]))          #insert start
    list_points.append(check_intersection.Point(goal[0],goal[1]))               #insert goal
    
    return list_points


#%%
def obtain_list_sides(list_vertices):
    """
    Given the list of obstacle vertices sorted by obstacle,
    this function returns the list of obstacle sides sorted by obstacle.
    
    Inputs: list_vertices as in find_all_paths
    
    Outputs: list_sides = [[obstacle_1.sides], [obstacle_2.sides], ...]
    where obstacle_k.sides = [(name_vertex1, name_vertex2), ..., (name_vertexV, name_vertex1)]
    """
    
    
    #step 1: obtain the number of sides of each obstacle
    length_obstacles = []
    for obstacle in list_vertices:
        length_obstacles.append(len(obstacle))
        
    #step 2: convert indexing of vertices from [0][0],[0][1],... into 1,2,3,...,N 
    #(0 and N+1 are start and goal respectively)
    
    #then enter every tuple (side.vertex1, side.vertex2) into sides_obstacle
    #then enter sides_obstacle into list_sides
    list_sides = []
    for obstacle in range(len(list_vertices)):
        sides_obstacle = []                             #list of sides of current obstacle
        
        shift = sum(length_obstacles[0:obstacle]) + 1   #to convert indexing
        nb_sides = length_obstacles[obstacle]
        for vertex in range(nb_sides):
            side = (shift + vertex,\
                    shift + ((vertex+1) % nb_sides))    #use of % to count 1,2,1 instead of 1,2,3
            sides_obstacle.append(side)
        
        list_sides.append(sides_obstacle)               #total list of sides, grouped by obstacle

    return list_sides



#%%
#test
# list_vertices = [[(10,10),(20,10),(15,18.66)],\
#                   [(30,25),(40,15),(53.66,18.66),(57.32,32.32),(47.32,42.32),(33.66,38.66)],\
#                       [(68.21,44.49),(68.31,61.98),(50.82,62.08),(50.72,44.58)]]
# start = (0,0)
# goal = (70,60)
# res = find_all_paths(list_vertices, start, goal)
# print(res)
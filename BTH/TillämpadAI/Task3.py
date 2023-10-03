# size of maze matrix
N = 4

# check is position is valid to move
def checkpos(maze, x, y ):
    if x >= 0 and x < N:
        if y >= 0 and y < N:
            if maze[x][y] == 1:
                return True
     
    return False
 

def Helper(maze):
    # solution matrix
    sol = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]
     
    if mazesolver(maze, 0, 0, sol) == False:
        return False
     
    for i in sol:
        for j in i:
            print(str(j) + " ", end ="")
        print("")
    return True
     
def mazesolver(maze, x, y, sol):
    # if destination reached
    if x == N - 1 and y == N - 1 and maze[x][y]== 1:
        sol[x][y] = 1
        return True
         
    # Check if position is valid
    if checkpos(maze, x, y) == True:
        if sol[x][y] == 1:
            return False
           
        sol[x][y] = 1
         
        # forward direction
        if mazesolver(maze, x + 1, y, sol) == True:
            return True
             
        # 
        # if above doesnt work, move in down direction
        if mazesolver(maze, x, y + 1, sol) == True:
            return True
           
        
        # if above two do not work, move back in left direction. Backtrack
        if mazesolver(maze, x - 1, y, sol) == True:
            return True
             
        # Else, move upwards
        if mazesolver(maze, x, y - 1, sol) == True:
            return True
         
        # if nothing works, backtrack and set the pos to 0 as we
        # will not be using the path. 
        sol[x][y] = 0
        return False
 

maze = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 1]
    ]
            
Helper(maze)
 
import random


def game(shape=""):
    choice = game_menu()  # Main Menu
    if choice == 1:  # Start a New Game
        path, shape = the_path() 
        grid = read_grid(path) 
        score = 0 
        lets_play(grid, shape, score) 
    elif choice == 2:  # Reload the most recent game
        grid = read_grid("board/current_board.txt") 
        with open("score.txt", "r") as f_score: 
            score = ord(f_score.read())
        lets_play(grid, shape, score)  # If there is a game saved continue the last game
    elif choice == 3:
        rules()
    elif choice == 4:
        print("Bye !")
    return""


# Start a game
def lets_play(grid, shape, score):
    stop = False
    # Stop the game if the user want to stop playing or if the user make a mistake about the coordinate three times
    while stop is False:
        print_grid(grid, score)
        bloc = select_bloc(shape)
        attempts = 0
        i, j, attempts = enter_coordinates(attempts, grid) 

        while valid_position(grid, bloc, i, j) is False: 
            if attempts == 3: 
                print("You loose !")
                print()
                with open("board/current_board.txt", "w") as board:
                    board.write("")  # Reset the grid
                # Game stop
                return game(shape)  # Return to the Game Menu
            else:
                print("Your coordinates are not valid. Please try again : remaining attempts", 3 - attempts, ".")
                i, j, attempts = enter_coordinates(attempts, grid)
        grid = emplace_bloc(grid, bloc, i, j)  # Place the bloc chosen
        for x in range(5): 
            # If a column or a row is full, col_clear or row_clear will clear the entire line/column concerned
            score1, grid = col_clear(grid, j + x)
            score2, grid = row_clear(grid, i - 4 + x)
            score += score1 + score2  # Sum the score won by clearing the column and the row
        update_score(score)  # Save the score
        save_grid(grid)
        print("If you want to stop playing, enter 'stop', else enter another thing.")
        a = input()
        if a == "stop" or a == "'stop'":
            stop = True
    return game(shape)  # Return to the Menu


def enter_coordinates(attempts, grid):
    # Use try except if the user enter other things than a string here
    while True:
        try:
            print("On witch row do you want to place the bloc ? (letter of row)")
            i = str(input())
            break
        except NameError:
            print("Oops! That was not a valid string try again.")
    while i < "A" or i > chr(65 + len(grid) - 1):  # If the coordinate does not enter the grid
        while True:
            try:
                print("On witch row do you want to place the bloc ? (letter of row)")
                i = str(input())
                break
            except ValueError:
                print("Oops! That was not a valid string try again.")
    i = ord(i) - 65  # Convert the coordinate letter into a coordinate number

# Same logic for the column
    while True:
        try:
            print("On witch column do you want to place the bloc ? (letter of column)")
            j = str(input())
            break
        except NameError:
            print("Oops! That was not a valid string try again.")
    while j < "a" or j > chr(97 + len(grid[i]) - 1):
        while True:
            try:
                print("On witch column do you want to place the bloc ? (letter of column)")
                j = str(input())
                break
            except NameError:
                print("Oops! That was not a valid string try again.")
    j = ord(j) - 97
    return i, j, attempts + 1


def game_menu():
    # Heading of the game
    print("_"*30)
    print()
    print(" "*5+"A TETRIS LIKE GAME!"+" "*5)
    print()
    print("_"*30)
    print()

    # Verify if there exist a recent last game
    board = open("board/current_board.txt", "r")
    content = board.read()
    # If there is no recent last game
    if content == "":
        print("New game - press 1")
        print("Game rules - press 2")
        print("Quit game - press 3")
    else:  # If there exist a recent last game, it will propose a new option : reload the most recent game
        print("New game - press 1")
        print("Resume game - press 2")
        print("Game rules - press 3")
        print("Quit game - press 4")
        print()
    board.close()
    while True:
        try:
            choice = int(input())
            break
        except ValueError:
            print("Oops! That was not a valid value try again.")
    while choice < 1 or choice > 4:
        while True:
            try:
                choice = int(input("Please enter 1, 2 or 3 : "))
                break
            except ValueError:
                print("Oops! That was not a valid value try again.")
    if content == "" and choice > 1:
        choice += 1

    return choice


def rules():

    print()
    print("How to play :")
    print()
    print("  1. Choose a game board")
    print("  2. Choose a bloc to enter in the board among 3 blocs")
    print("  3. Enter bloc's coordinates")
    print("     Warning : the coordinates on the grid that you will enter will match the cell of the lower left corner of the bloc.")
    print("     You have 3 attempts to enter valid coordinate, else you loose")
    print("  4. Increase your score with clearing a max of row and columns by filling the entire line")
    print()
    print("If you want to return to the menu, write 'menu' :")
    while True:
        try:
            menu = str(input())
            break
        except NameError:
            print("Oops! That was not a valid string try again.")
    while menu != "menu" and menu != "'menu'":
        while True:
            try:
                menu = str(input())
                break
            except NameError:
                print("Oops! That was not a valid string try again.")
    return game()


# Game board functions

# Return the name of a file 'path' that correspond to the user choice for the grid
def the_path():
    # Heading of the choice of the shape board
    print("_" * 30)
    print(" " * 5 + "SHAPE OF THE BOARD" + " " * 5)
    print("_" * 30)
    print()
    
    print("Triangle - press 1")
    print("Diamond - press 2")
    print("Circle - press 3")
    print()

    path = ""
    while True:
        try:
            shape = int(input())
            break
        except ValueError:
            print("Oops! That was not a valid number try again.")
    while shape < 1 or shape > 3:
        while True:
            try:
                shape = int(input("Please enter 1, 2 or 3 : "))
                break
            except ValueError:
                print("Oops! That was not a valid number try again.")
    if shape == 1:
        shape = "triangle"
    elif shape == 2:
        shape = "diamond"
    elif shape == 3:
        shape = "circle"

    print()
    print("Basic size board - press 1")
    print("Personalized size  - press 2")
    print()
    while True:
        try:
            choice = int(input())
            break
        except ValueError:
            print("Oops! That was not a valid number try again.")
    while choice != 1 and choice != 2:
        while True:
            try:
                choice = int(input("Please enter 1 or 2 : "))
                break
            except ValueError:
                print("Oops! That was not a valid number try again.")

    if choice == 1:
        if shape == "diamond":
            path = "board/littleboard_diamond.txt"
        elif shape == "triangle":
            path = "board/littleboard_triangle.txt"
        else:
            path = "board/littleboard_circle.txt"

    elif choice == 2:
        print("Enter the number of columns that you want for the board :")
        while True:
            try:
                size = int(input(""))
                break
            except ValueError:
                print("Oops! That was not a valid number try again.")
        # Control if the personalized board can be created or not
        while size < 7 and shape != "diamond" or size < 9 and shape == "diamond" or size > 25 or size % 2 == 0:
            print("Enter the number of columns that you want for the board (only odd number greater than 7 are allowed):") 
            while True:
                try:
                    size = int(input(""))
                    break
                except ValueError:
                    print("Oops! That was not a valid number try again.")
        halfsize = int((size + 1) / 2)
        
    # Create the personalized board in Diamond based on the basic textfile of the diamond
        if shape == "diamond":
            f_diamond2 = open("board/diamondboard.txt", "w")

            for i in range(halfsize - 1):
                f_diamond2.write("0 " * (halfsize - i - 1))
                f_diamond2.write("1" + i * " 1 1")
                f_diamond2.write(" 0" * (halfsize - i - 1))
                f_diamond2.write("\n")
            for i in range(halfsize):
                f_diamond2.write("0 " * i)
                f_diamond2.write("1" + (halfsize - i - 1) * " 1 1")
                f_diamond2.write(" 0" * i)
                if i != halfsize - 1:
                    f_diamond2.write("\n")

            f_diamond2.close()

            path = "board/diamondboard.txt"

    # Create the personalized board in Circle based on the basic textfile of the circle
        elif shape == "circle":
            f_circle2 = open("board/circleboard.txt", "w")

            radius = (size / 2) - 0.5
            for i in range(size):
                for j in range(size):
                    x = i - radius
                    y = j - radius
                    if x ** 2 + y ** 2 <= radius ** 2 + 1:
                        f_circle2.write("1 ")
                    else:
                        f_circle2.write("0 ")
                f_circle2.write("\n")
            f_circle2.close()

            path = "board/circleboard.txt"

    # Create the personalized board in triangle based on the basic textfile of the diamond
        else:
            f_triangle2 = open("board/triangleboard.txt", "w")
            for i in range(halfsize):
                f_triangle2.write("0 " * (halfsize - i - 1))
                f_triangle2.write("1" + i * " 1 1")
                f_triangle2.write(" 0" * (halfsize - i - 1))
                if i != halfsize - 1:
                    f_triangle2.write("\n")
            f_triangle2.close()

            path = "board/triangleboard.txt"
    return path, shape


# Returns a valid grid read from the contents of the file specified by path.
# Transform the text file in a list
def read_grid(path):
    with open(path, "r") as f_board:
        board = f_board.read()

    list_grid = []
    l = []
    for e in board:
        if e == "0":
            l.append(0)
        elif e == "\n":
            list_grid.append(l)
            l = []
        elif e == "1":
            l.append(1)
        elif e == "2":
            l.append(2)
    list_grid.append(l)
    return list_grid


# Transform a list grid in text and save it in a file
def save_grid(grid):
    board = open("board/current_board.txt", "w")
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                board.write("0 ")
            if grid[i][j] == 1:
                board.write("1 ")
            if grid[i][j] == 2:
                board.write("2 ")
        if i != len(grid)-1:
            board.write("\n")
    board.close()
    with open("board/current_board.txt", "r") as board:
        text = board.read()
    return text


# Function that print the current grid and score
def print_grid(grid, score):
    # Print all the letters corresponding to the columns
    print(end="  ")
    for i in range(len(grid[0])):
        print(chr(97+i), end=" ")
    print()
    # Print a line below the letters
    print(end="  ")
    print("= "*len(grid[0]))

    for i in range(len(grid)):
        # Print the letter corresponding to the line and a vertical line on the left of the grid
        print(chr(65+i)+"║", end="")
        for j in range(len(grid[i])):
            # Print the grid and the blocs
            if grid[i][j] == 0:
                print("  ", end="")
            if grid[i][j] == 1:
                print(". ", end="")
            if grid[i][j] == 2:
                print("■ ", end="")
        print("║", end="")  # Print a vertical line on the right of the grid
        
        # Print the score between two lines on the right of the grid
        if i == int(len(grid)/2) - 2:
            print(" " * 12 + "SCORE")
        elif i == int(len(grid)/2) - 1:
            print(" " * 10 + "=" * 9)
        elif i == int(len(grid)/2):
            print(" " * 10, score)
        elif i == int(len(grid)/2) + 1:
            print(" " * 10 + "=" * 9)
        else:
            print()
            
    # Print a line below the grid
    print(end="  ")
    print("= " * len(grid[0]))
    return ""


# Blocs functions

# Open all the blocs files corresponding to the type of grid chosen and collect its content in a list
def open_bloc(grid):
    l = []
    # Transform the content of the blocs files in a 2D list with read_grid
    # Then, we add this 2D list in the list l

    # Blocks common to all grids
    l.append(read_grid("bloc/all/bloc1.txt"))

    l.append(read_grid("bloc/all/bloc2.txt"))

    l.append(read_grid("bloc/all/bloc3.txt"))

    l.append(read_grid("bloc/all/bloc4.txt"))

    l.append(read_grid("bloc/all/bloc5.txt"))

    l.append(read_grid("bloc/all/bloc6.txt"))

    l.append(read_grid("bloc/all/bloc7.txt"))

    l.append(read_grid("bloc/all/bloc8.txt"))

    l.append(read_grid("bloc/all/bloc9.txt"))

    l.append(read_grid("bloc/all/bloc10.txt"))

    l.append(read_grid("bloc/all/bloc11.txt"))

    l.append(read_grid("bloc/all/bloc12.txt"))

    l.append(read_grid("bloc/all/bloc13.txt"))

    l.append(read_grid("bloc/all/bloc14.txt"))

    l.append(read_grid("bloc/all/bloc15.txt"))

    l.append(read_grid("bloc/all/bloc16.txt"))

    l.append(read_grid("bloc/all/bloc17.txt"))

    l.append(read_grid("bloc/all/bloc18.txt"))

    l.append(read_grid("bloc/all/bloc19.txt"))

    l.append(read_grid("bloc/all/bloc20.txt"))

    # Same logic applied to the "triangle" shape
    if grid == "triangle":

        l.append(read_grid("bloc/triangle/triangle1.txt"))

        l.append(read_grid("bloc/triangle/triangle2.txt"))

        l.append(read_grid("bloc/triangle/triangle3.txt"))

        l.append(read_grid("bloc/triangle/triangle4.txt"))

        l.append(read_grid("bloc/triangle/triangle5.txt"))

        l.append(read_grid("bloc/triangle/triangle6.txt"))

        l.append(read_grid("bloc/triangle/triangle7.txt"))

        l.append(read_grid("bloc/triangle/triangle8.txt"))

        l.append(read_grid("bloc/triangle/triangle9.txt"))

        l.append(read_grid("bloc/triangle/triangle10.txt"))

        l.append(read_grid("bloc/triangle/triangle11.txt"))

    # Same logic applied to the "diamond" shape
    elif grid == "diamond":

        l.append(read_grid("bloc/diamond/diamond1.txt"))

        l.append(read_grid("bloc/diamond/diamond2.txt"))

        l.append(read_grid("bloc/diamond/diamond3.txt"))

        l.append(read_grid("bloc/diamond/diamond4.txt"))

        l.append(read_grid("bloc/diamond/diamond5.txt"))

        l.append(read_grid("bloc/diamond/diamond6.txt"))

        l.append(read_grid("bloc/diamond/diamond7.txt"))

        l.append(read_grid("bloc/diamond/diamond8.txt"))

        l.append(read_grid("bloc/diamond/diamond9.txt"))

        l.append(read_grid("bloc/diamond/diamond10.txt"))

        l.append(read_grid("bloc/diamond/diamond11.txt"))

        l.append(read_grid("bloc/diamond/diamond12.txt"))

        l.append(read_grid("bloc/diamond/diamond13.txt"))

        l.append(read_grid("bloc/diamond/diamond14.txt"))

    # Same logic applied to the "circle" shape
    elif grid == "circle":

        l.append(read_grid("bloc/circle/circle1.txt"))

        l.append(read_grid("bloc/circle/circle2.txt"))

        l.append(read_grid("bloc/circle/circle3.txt"))

        l.append(read_grid("bloc/circle/circle4.txt"))

        l.append(read_grid("bloc/circle/circle5.txt"))

        l.append(read_grid("bloc/circle/circle6.txt"))

        l.append(read_grid("bloc/circle/circle7.txt"))

        l.append(read_grid("bloc/circle/circle8.txt"))

        l.append(read_grid("bloc/circle/circle9.txt"))

        l.append(read_grid("bloc/circle/circle10.txt"))

        l.append(read_grid("bloc/circle/circle11.txt"))

        l.append(read_grid("bloc/circle/circle12.txt"))

    return l


# Displays 3 random blocs associated to the grid.
def print_blocs(grid):
    l = open_bloc(grid)  # Collect all the blocs corresponding to the shape of the board
    m = []  # Initialise the list of the blocs randomly chosen
    nb_bloc = 0  # Initialise the number of blocs that are already chosen
    # 3 blocs are randomly chosen among those in the list l
    while nb_bloc < 3:
        bloc = random.choice(l)
        if bloc not in m:
            m.append(bloc)
            nb_bloc += 1

    # Print the three blocs
    for blocs in m:
        for row in blocs:
            if row != [0, 0, 0, 0, 0]:
                for col in row:
                    if col == 0:
                        print("  ", end="")
                    elif col == 1:
                        print("■ ", end="")
                print()
        print()
    return m  # Return the list containing the three blocs


# Allow the user to choose a block within the 3 blocs that are displayed
def select_bloc(grid):
    list = print_blocs(grid)  # Show 3 random blocs and save them in a list
    # Ask the user to choose a bloc 
    print("Select a bloc :(1, 2 or 3)")
    i = int(input())
    while i < 1 or i > 3:
        print("Select a bloc :(1, 2 or 3)")
        i = int(input())
    # Return the bloc chosen among the 3 blocs
    return list[i-1]


# Positioning

# It checks if the coordinate entered are valid or not
def valid_position(grid, bloc, i, j):
    valid_coordinate = []
    y_max = len(grid)
    x_max = len(grid[i])
    is_valid = False

    if i < y_max and j + 4 < x_max:  # The coordinates must be in the board and not outside
    
        # We try to define if the bloc chosen can enter the board
        for x in range(5):
            l = [False] * 5
            for y in range(5):
                # We test if the coordinate of bloc can enter the board
                if bloc[x][y] == 0:
                    l[y] = True
                elif bloc[x][y] == 1 and grid[x + i - 4][y + j] == 1:
                    l[y] = True
            valid_coordinate.append(l)
        # We are going to verify if all the coordinate of the bloc match with the board
        is_valid = True
        for i in range(len(valid_coordinate)):
            for j in range(len(valid_coordinate[i])):
                if valid_coordinate[i][j] is False:
                    is_valid = False
    return is_valid


# Place the bloc
def emplace_bloc(grid, bloc, i, j):
    if valid_position(grid, bloc, i, j) is True:  # Test if the coordinate are valid or not
        # Browse the dimensions of the bloc file
        for x in range(5):
            for y in range(5):
                if bloc[x][y] != 0 and bloc[x][y] == grid[x + i - 4][y + j] == 1:
                    grid[x + i - 4][y + j] = 2  # Place the bloc
    return grid


# Clear rows/columns and update the score

# It verifies if the line i in a grid is full.
def row_state(grid, i):

    L = []
    for y in range(len(grid[i])):
        full_line = False
        if grid[i][y] == 2 or grid[i][y] == 0:
            full_line = True
        L.append(full_line)
    if False in L:
        full_line = False
    else:
        full_line = True
    return full_line


# It verifies if the column j in a grid is full.
def col_state(grid, j):

    L = []
    for x in range(len(grid)):
        full_line = False
        if grid[x][j] == 2 or grid[x][j] == 0:
            full_line = True
        L.append(full_line)
    if False in L:
        full_line = False
    else:
        full_line = True
    return full_line


# It cancels the row i in a grid by shifting all lines from the top of a unit down.
def row_clear(grid, i):
    count = 0
    if row_state(grid, i) is True:
        for y in range(len(grid[i])):
            if grid[i][y] == 2:
                grid[i][y] = 1
                count += 1
        for x in range(i, 0, -1):
            for y in range(len(grid[x])):
                if grid[x][y] == 1 and grid[x-1][y] == 2:
                    grid[x-1][y] = 1
                    grid[x][y] = 2
    return count, grid


# It cancels the column j in a grid.
def col_clear(grid, j):
    count = 0
    if col_state(grid, j) is True:
        for x in range(len(grid)):
            if grid[x][j] == 2:
                grid[x][j] = 1
                count += 1
    return count, grid


# The number of cancelled squares corresponding to the score
def update_score(score):
    f_score = open("score.txt", "w")
    f_score.write(chr(score))
    f_score.close()
    return ""

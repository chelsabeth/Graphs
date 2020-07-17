from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt" 
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
rooms = {}
oldRoomValue = 0
lastDirection = None

# Ideas

# dfs until dead end then bfs



###

def calculateOpposite(direction):
    if direction == 'n':
        return 's'
    if direction == 'e':
        return 'w'
    if direction == 's':
        return 'n'
    if direction == 'w':
        return 'e'



def traverseWhileQuestionMark():
    # While there is a '?' in a direction for the room that you are in
        # If the room is a '?'
            # Go from the starting room which is zero to a unexlored room which is a '?' using player.travel()
    pass

def rebuildDictionaryForRoomWithNewDirection(direction):
    # After we move to new room
    rooms[oldRoomValue][direction] = player.current_room.id
    rooms[player.current_room.id][calculateOpposite(direction)] = oldRoomValue

def roomsFilled():
    # if rooms[player.current_room.id]['n'] is not '?' and rooms[player.current_room.id]['s'] is not '?' and rooms[player.current_room.id]['e'] is not '?' and rooms[player.current_room.id]['w']:
    #     return True
    validDirection = player.current_room.get_exists()

    for each in validDirection:
        if rooms[player.current_room.id][each] is '?':
            return False

    return True
    
def setNewRoom():

    # Get room player is currently in
    room = player.current_room

    # Make an empty dictionary that we can fill with the possible directions, and room values which start at '?'
    exitsDict = {}
    exits = room.get_exits()

    # Fill each possible direction with '?'
    for each in exits:
        exitsDict[each] = '?'

    # Add that dictionary we just created to the main rooms dictionary using the value from the room
    rooms[room.id] = exitsDict

while len(rooms) < 7:
    # Which of these directions have already been explored? We know this because the numbers would already be there instead of the ?
    # TraverseWhileQuestionMark()
    # Go back until there is a '?'

    # If the room has not already been added to rooms dict add it
    if player.current_room.id not in traversal_path:
        setNewRoom()
    
    # Set the rooms value in the dictionary for the previous rooms ID based on what direction we previously moved

    # Set old rooms value in the dictionary for the new rooms ID
    rebuildDictionaryForRoomWithNewDirection(lastDirection)
    
    # Do magical thing loading from previous info

    # If there are no more '?' in directions then go back the way we came
    while roomsFilled():
        # move back to where I came from 
        player.travel(lastDirection)

    # What directions are avaiable from current room using room.get_exits()
    directions = player.current_room.get_exits()

    # Get random direction
    randomDirection = random.choice(directions)

    # while randomDirection == calculateOpposite(lastDirection):
    #     randomDirection = random.choice(directions)

    # Save old room
    oldRoomValue = player.current_room.id

    # Move into random direction if the direction has not already been explored
    player.travel(randomDirection)
    lastDirection = randomDirection
    # print(player.current_room.id)
        
    

print(rooms)

###

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
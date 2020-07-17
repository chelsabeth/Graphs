from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt" 
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
room = player.current_room

# gets the opposite direction - helps with checking which direction I have already been 
def calculate_opposite(direction):
    if direction == 'n':
        return 's'
    if direction == 'e':
        return 'w'
    if direction == 's':
        return 'n'
    if direction == 'w':
        return 'e'

def room_from_path(starting_room, path):
    room = starting_room
    for direction in path:
        room = room.get_room_in_direction(direction)
        # take the player and put them in the new room, set the room to be the new room
    return room

# finds the path to the nearest unexplored room
def to_nearest_unexplored(starting_room):
    explored = set()
    queue = Queue()
    queue.enqueue([])

    # while we still have items in the queue
    while queue.size() != 0:
        # adding the item you just dequeued to the path
        path = queue.dequeue()
        # getting the path to the nearest unexplored room
        room = room_from_path(starting_room, path)
        # options for which directions we can move 
        exits = room.get_exits()

        # for all the valid ways that the player can go 
        for direction in exits:
            # makes a copy of path from up there ☝️
            new_path = path.copy()
            # adds the direction that is valid to that path 
            new_path.append(direction)
            # see if the direction player wants to go is unexplored and if so, returns that path 
            if rooms[room.id][direction] == '?':
                return new_path
            # if direction has not already been explored, add the new_path+direction to the queue
            if (room, direction) not in explored:
                queue.enqueue(new_path)
            # adds room, direction to explored set    
            explored.add((room, direction))

def add_new_room(room):
    # adds room to rooms graph if room has not already been added
    adjacent_rooms = rooms.get(room.id)
    if adjacent_rooms is None:
        adjacent_rooms = {direction:'?' for direction in room.get_exits()}
        rooms[room.id] = adjacent_rooms

# where the traversal starts, add the first room to the rooms dict
add_new_room(room)

while True:
    exits = room.get_exits()
    path_to_unexplored = to_nearest_unexplored(room)
    # if every room is explored, this should be 0 
    if path_to_unexplored is None or len(path_to_unexplored) == 0:
        # once we have visited every room stop the loop
        break
    for direction in path_to_unexplored:
        # moving to new room, gets a room in a certain direction
        new_room = room.get_room_in_direction(direction)
        # adds direction to traversal_path array 
        traversal_path.append(direction)
        # takes the new rooms id and adds it to the chosen direction - this is making the connections between two rooms
        rooms[room.id][direction] = new_room.id
        # if the room is not in rooms,then add it to the rooms dict/graph
        add_new_room(new_room)
        # take the old rooms id and adds it to the opposite of the chosendirection - this is making the connections between two rooms
        rooms[new_room.id][calculate_opposite(direction)] = room.id

        # take the player and put them in the new room, set the room to be the new room
        player.travel(direction)
        room = player.current_room

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

import random
import numpy as np


map_width = 60 # number of squares wide
map_height = 60 # number of squares tall

min_room_size = 8
max_room_size = 12
max_rooms = 12
min_rooms = 8
corridor_width = 4
corridor_height = 4
rooms = []


def init_map():
    """Initializes the map of key/value pairs."""
    game_map = np.zeros((map_width, map_height), dtype=int)
    return game_map


class Room:
    """Defines a room of the dungeon."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f"A room at ({self.x},{self.y})"


def init_rooms(game_map):
    """Initializes the rooms in the dungeon."""
    total_rooms = random.randint(min_rooms, max_rooms)
    while len(rooms) < total_rooms:
        width = random.randint(min_room_size, max_room_size)
        height = random.randint(min_room_size, max_room_size)
        x = random.randint(0, map_width - width - 2)
        y = random.randint(0, map_height - height - 2)
        room = Room(x, y, width, height)
        if not check_for_overlap(room, rooms):
            rooms.append(room)
    for room in rooms:
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                game_map[x, y] = 1

    return game_map

def check_for_overlap(room, rooms):
    """Return false if the room overlaps any other room."""
    for current_room in rooms:
        xmin1 = room.x
        xmax1 = room.x + room.width
        xmin2 = current_room.x
        xmax2 = current_room.x + current_room.width
        ymin1 = room.y
        ymax1 = room.y + room.height
        ymin2 = current_room.y
        ymax2 = current_room.y + current_room.height
        if (xmin1 <= xmax2 and xmax1 >= xmin2) and \
           (ymin1 <= ymax2 and ymax1 >= ymin2):
            return True
    return False


def connect_rooms(game_map):
    """Draws passages randomly between the rooms."""
    random.shuffle(rooms)
    for i in range(len(rooms) - 1):
        A: Room = rooms[i]
        B: Room = rooms[i + 1]

        if A.x <= B.x and A.x + A.width >= B.x + B.width:
            for x in range(B.x, B.x + corridor_width):
                if A.y < B.y:
                    start, stop = A.y + A.height, B.y + 2
                else:
                    start, stop = B.y + B.height, A.y + 2
                for y in range(start, stop):
                    game_map[x, y] = 1
        elif A.y <= B.y and A.y + A.height >= B.y + B.height:
            for y in range(B.y, B.y + corridor_height):
                if A.x < B.x:
                    start, stop = A.x + A.width, B.x + 2
                else:
                    start, stop = B.x + B.width, A.x
                for x in range(start, stop):
                    game_map[x, y] = 1

        elif A.x >= B.x + B.width and A.y >= B.y + B.height:
            for x in range(B.x + B.width - 2, A.x + 1):
                for y in range(B.y + B.height - 2, A.y + 1):
                    game_map[x, y] = 1
        elif A.x + A.width <= B.x and A.y >= B.y + B.height:
            for x in range(A.x + A.width - 2, B.x + 1):
                for y in range(B.y + B.height - 2, A.y + 1):
                    game_map[x, y] = 1
        elif A.x >= B.x + B.width and A.y + A.height <= B.y:
            for x in range(B.x + B.width - 2, A.x + 1):
                for y in range(A.y + A.height - 1, B.y + 1):
                    game_map[x, y] = 1
        elif A.x + A.width <= B.x and A.y + A.height <= B.y:
            for x in range(A.x + A.width - 2, B.x + 1):
                for y in range(A.y + A.height - 2, B.y + 1):
                    game_map[x, y] = 1

        elif A.x >= B.x and A.x <= B.x + B.width:
            for x in range (A.x, A.x + corridor_width):
                if A.y > B.y + B.height:
                    start, stop = B.y + B.height, A.y + 2
                else:
                    start, stop = A.y, B.y + B.height + 2
                for y in range(start, stop):
                    game_map[x, y] = 1

        elif A.x + A.width >= B.x and A.x + A.width <= B.x + B.width:
            for x in range(A.x + A.width, A.x + A.width + corridor_width):
                if A.y > B.y + B.height:
                    start, stop = B.y + B.height, A.y + 2
                else:
                    start, stop = A.y, B.y + B.height + 2
                for y in range(start, stop):
                    game_map[x, y] = 1

        elif A.y >= B.y and A.y + A.height >= B.y + B.height:
            for y in range(B.y + B.height, A.y + corridor_height):
                if A.x > B.x + B.width:
                    start, stop = B.x + B.width, A.x + 2
                else:
                    start, stop = A.x + A.width, B.x + 2
                for x in range(start, stop):
                    game_map[x, y] = 1

        elif A.y <= B.y and A.y + A.height <= B.y + B.height:
            for y in range(A.y + A.height, B.y + corridor_height):
                if A.x > B.x + B.width:
                    start, stop = B.x + B.width, A.x + 2
                else:
                    start, stop = A.x + A.width, B.x + 2
                for x in range(start, stop):
                    game_map[x, y] = 1

        else:
            print('Unsuccessful connection')

    return game_map

        


def locate_mobs(game_map: np.array) -> np.array:
    for i in range(len(rooms)):
        room: Room = rooms[i]
        x: int = room.x + room.width // 2
        y : int = room.y + room.height // 2
        if i == 0:
            game_map[x, y] = 5 # value of character
        elif 1 <= i <= 2:
            game_map[x, y] = 3 # value of holem
        else:
            game_map[x, y] = random.choice((7, 2))
    return game_map

def generate_dungeon():
    game_map = init_map()
    game_map = init_rooms(game_map)
    game_map = connect_rooms(game_map)
    game_map[0, :] = game_map[map_width - 1, :] = game_map[:, 0] = game_map[:, map_height - 1] = 0
    game_map = locate_mobs(game_map)
    return game_map


if __name__ == "__main__":
    game_map = [''.join([str(i) for i in line]).replace('0', 'x').replace('1', '.').replace('5', 'p').replace('7', '1') for line in generate_dungeon().tolist()]
    with open('map.txt', 'w') as ouf:
        for line in game_map:
            print(line, file=ouf)

import pandas as pd
import pprint
import numpy as np
import copy

def is_nan(x):
    return (x is np.nan or x != x)

def clean_courses_seats_data(courses_seats_data):
    new_data = []
    for l in courses_seats_data:
        if is_nan(l[0]) is False:
            if l[0][0].isalpha:
                new_data.append(l)
    half = 1
    courses_seats = {}
    for courses in new_data:
        day = courses[0]
        current = {}
        if day[0] is '2':
            half = half + 1
            continue
        i = 2
        while i<len(courses) and is_nan(courses[i]) is False:
            current[courses[i]] = (courses[i + 1], half)
            i = i + 2
        if half is 1:
            courses_seats[day] = current
        else:
            courses_seats[day].update(current)
    return courses_seats

def clean_seat_arrangement_data(rooms_capacity_data):
    new_data = {}
    for l in rooms_capacity_data:
        new_data[l[0]] = l[-1]
    return new_data

def num_of_floors(rooms_capacity_data):
    floors = set()
    for rooms in rooms_capacity_data:
        floors.add(str(rooms)[0])
    return floors

def get_seating_arrangement(rooms_capacity_data, courses_seats_data, days, half):
    half_courses = []
    courses_rooms = {}
    arrangement = {}
    floor_wise_seats = {}

    for courses in courses_seats_data[days]:
        if courses_seats_data[days][courses][1] is half:
            half_courses.append((courses_seats_data[days][courses][0], courses))

    half_courses.sort()
    half_courses.reverse()

    for rooms in rooms_capacity_data:
        floor_wise_seats[str(rooms)[0]] = []

    for rooms in rooms_capacity_data:
        floor_wise_seats[str(rooms)[0]].append((int(rooms_capacity_data[rooms]/2), rooms))
        floor_wise_seats[str(rooms)[0]].append((rooms_capacity_data[rooms]-int(rooms_capacity_data[rooms]/2), rooms))

    for courses in half_courses:
        num_of_students = courses[0]
        courses_name = courses[1]
        allocated = False
        for floors in floor_wise_seats:
            current = []
            courses_rooms[courses_name] = set()
            temp_floor_wise_seats = copy.deepcopy(floor_wise_seats[floors])
            remaining_students = num_of_students
            rooms = floor_wise_seats[floors]
            floor_wise_seats[floors].sort()
            floor_wise_seats[floors].reverse()
            for i, room in enumerate(floor_wise_seats[floors]):
                if allocated is False:
                    room_capacity = room[0]
                    room_num = room[1]
                    if room_num not in courses_rooms[courses_name]:
                        if remaining_students > room_capacity:
                            current.append((room_num, room_capacity))
                            remaining_students = remaining_students - room_capacity
                            room_capacity = 0
                        else:
                            current.append((room_num, remaining_students))
                            room_capacity = room_capacity - remaining_students
                            remaining_students = 0
                            allocated = True
                        courses_rooms[courses_name].add(room_num)
                    floor_wise_seats[floors][i] = (room_capacity, room_num)
            if allocated is True:
                break
            else:
                floor_wise_seats[floors] = copy.deepcopy(temp_floor_wise_seats)
        if allocated is False:
            courses_rooms[courses_name] = set()
            remaining_students = num_of_students
            current = []
            for floors in floor_wise_seats:
                rooms = floor_wise_seats[floors]
                floor_wise_seats[floors].sort()
                floor_wise_seats[floors].reverse()
                for i, room in enumerate(floor_wise_seats[floors]):
                    if allocated is False:
                        room_capacity = room[0]
                        room_num = room[1]
                        if room_num not in courses_rooms[courses_name] and room_capacity > 0:
                            if remaining_students > room_capacity:
                                current.append((room_num, room_capacity))
                                remaining_students = remaining_students - room_capacity
                                room_capacity = 0
                            else:
                                current.append((room_num, remaining_students))
                                room_capacity = room_capacity - remaining_students
                                remaining_students = 0
                                allocated = True
                            courses_rooms[courses_name].add(room_num)
                        floor_wise_seats[floors][i] = (room_capacity, room_num)

        if allocated is True:
            arrangement[courses_name] = current
        else:
            print("ERROR")

    print(days, half, "half")
    print(arrangement)

df = pd.read_excel('tt full.xlsx', header=0, sheetname='Courses Seats') #, sheetname='<your sheet>'
df.to_csv('courses_seats_data.csv', index=False, quotechar="'")
df = pd.read_excel('tt full.xlsx', header=0, sheetname='ClassRoom Capacity') #, sheetname='<your sheet>'
df.to_csv('rooms_capacity_data.csv', index=False, quotechar="'")
courses_seats_data = pd.read_csv('courses_seats_data.csv').values
rooms_capacity_data = pd.read_csv('rooms_capacity_data.csv').values
_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

courses_seats_data = clean_courses_seats_data(courses_seats_data)
rooms_capacity_data = clean_seat_arrangement_data(rooms_capacity_data)

#print(courses_seats_data)
#print(rooms_capacity_data)

for days in courses_seats_data:
    if days in _days:
        get_seating_arrangement(rooms_capacity_data, courses_seats_data, days, 1)
        get_seating_arrangement(rooms_capacity_data, courses_seats_data, days, 2)

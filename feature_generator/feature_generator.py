import math
import csv
import os
import json
import threading

class TPoint:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

class Session:
    def __init__(self, id, input_data_file_path):
        self.id = id
        self.input_data_file_path = input_data_file_path
        self.features = {}

class Feature:
    def __init__(self):
        self.records = []

    def add_record(self, value):
        self.records.append(value)

def get_t_point(csv_line):
    record = csv_line.split(',')
    x = int(record[1])
    y = int(record[2])
    time = float(record[0])
    return TPoint(x, y, time)

def get_theta(point_a, point_b):
    delta_x = abs(point_a.x - point_b.x)
    delta_y = abs(point_a.y - point_b.y)
    return math.atan2(delta_y, delta_x)

def get_velocity(axis, tpoint_a, tpoint_b):
    if axis not in ['x', 'y', 'xy']:
        return -1

    if axis == 'xy':
        x_velocity = get_velocity('x', tpoint_a, tpoint_b)
        y_velocity = get_velocity('y', tpoint_a, tpoint_b)
        return math.sqrt(x_velocity**2 + y_velocity**2)

    delta_axis = 0.0
    if axis == 'x':
        delta_axis = abs(tpoint_a.x - tpoint_b.x)
    elif axis == 'y':
        delta_axis = abs(tpoint_a.y - tpoint_b.y)

    delta_t = abs(tpoint_a.time - tpoint_b.time)
    if delta_t == 0:
        return 0.0

    return delta_axis / delta_t

def get_feature_val(feature_name, tpoints):
    if 'velocity' in feature_name:
        if feature_name == 'velocity':
            return get_velocity('xy', tpoints[0], tpoints[1])
        return get_velocity(feature_name[0], tpoints[0], tpoints[1])

    if feature_name == 'acceleration':
        velocity_a = get_velocity('xy', tpoints[0], tpoints[1])
        velocity_b = get_velocity('xy', tpoints[2], tpoints[3])
        delta_t = abs(tpoints[0].time - tpoints[3].time)
        if delta_t == 0:
            return 0
        return abs(velocity_a - velocity_b) / delta_t

    if feature_name == 'jerk':
        acceleration_a = get_feature_val('acceleration', tpoints[:4])
        acceleration_b = get_feature_val('acceleration', tpoints[4:])
        delta_t = abs(tpoints[0].time - tpoints[7].time)
        if delta_t == 0:
            return 0
        return abs(acceleration_a - acceleration_b) / delta_t

    if feature_name == 'theta':
        return get_theta(tpoints[0], tpoints[1])

    return -1

def initialize_tpoints_buffer(file_path, n):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        tpoints = [get_t_point(','.join(next(reader))) for _ in range(n)]
    return tpoints

def append_tpoint(tpoints, num_tpoints, new_tpoint):
    for i in range(1, num_tpoints):
        tpoints[i - 1] = tpoints[i]
    tpoints[num_tpoints - 1] = new_tpoint
    return tpoints

def record_feature(feature_name, session):
    tpoints = initialize_tpoints_buffer(session.input_data_file_path, 8)
    feature = Feature()
    feature_value = get_feature_val(feature_name, tpoints)
    feature.add_record(feature_value)

    with open(f"{session.id}_{feature_name}.json", 'w') as output_file:
        json.dump([feature_value], output_file)

    with open(session.input_data_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            new_tpoint = get_t_point(','.join(row))
            tpoints = append_tpoint(tpoints, 8, new_tpoint)
            feature.add_record(get_feature_val(feature_name, tpoints))

    with open(f"{session.id}_{feature_name}.json", 'a') as output_file:
        json.dump(feature.records, output_file)

def record_features(session):
    threads = []
    for feature_name in get_features_names():
        thread = threading.Thread(target=record_feature, args=(feature_name, session))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def get_features_names():
    return ["velocity", "acceleration", "jerk", "theta"]

session = Session("session_1", "mouse_movement_data.txt")
record_features(session)

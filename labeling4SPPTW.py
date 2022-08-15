#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 11:28
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : labeling4SPPTW.py
# @Statement : The labeling algorithm for the shortest path problem with time windows
# @Reference : Desrochers M, Soumis F. A generalized permanent labelling algorithm for the shortest path problem with time windows[J]. INFOR: Information Systems and Operational Research, 1988, 26(3): 191-212.
import copy
import heapq


def find_neighbor(network):
    """
    find the neighbor of each node
    :param network:
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def dominated(obj1, obj2):
    """
    judgment whether objective 1 is dominated by objective 2
    :param obj1: the objective value 1
    :param obj2: the objective value 2
    :return:
    """
    if (obj1[0] > obj2[0] and obj1[1] >= obj2[1]) or (obj1[0] >= obj2[0] and obj1[1] > obj2[1]):
        return True
    return False


def add_labels(omega, obj_list, destination, temp_node, temp_obj):
    """

    :param omega:
    :param obj_list:
    :param destination:
    :param temp_node:
    :param temp_obj:
    :return:
    """
    for index in omega[temp_node]:
        if dominated(temp_obj, obj_list[index]):
            return False
    for index in omega[destination]:
        if temp_obj[0] >= obj_list[index][0]:
            return False
    return True


def main(network, source, destination, time_window):
    """
    the main function
    :param network: {node1: {node2: [cost1, time1], node3: [cost2, time2] ...}, ...}
    :param source: the source node
    :param destination:
    :param time_window:
    :return:
    """
    # Step 1. Initialization
    neighbor = find_neighbor(network)
    nn = len(network)  # node number
    nw = len(network[source][neighbor[source][0]])  # objective number
    obj_list = []
    path_list = []
    ni = 0
    omega = {}
    for node in range(nn):
        omega[node] = []
    queue = []
    ind = 0
    heapq.heappush(queue, (0, ind, {
        'path': [source],
        'obj': [0 for n in range(nw)],
    }))
    ind += 1

    # Step 2. The main loop
    while queue:
        length, temp_ind, info = heapq.heappop(queue)
        path = info['path']
        obj = info['obj']
        epicenter = path[-1]
        if add_labels(omega, obj_list, destination, epicenter, obj):
            omega[epicenter].append(ni)
            obj_list.append(obj)
            path_list.append(path)
            ni += 1
            for node in neighbor[epicenter]:
                if node not in path and obj[1] + network[epicenter][node][1] <= time_window[node][1]:
                    temp_obj = [
                        obj[0] + network[epicenter][node][0],
                        max(time_window[node][0], obj[1] + network[epicenter][node][1]),
                    ]
                    temp_path = copy.deepcopy(path)
                    temp_path.append(node)
                    heapq.heappush(queue, (sum(temp_obj), ind, {
                        'path': temp_path,
                        'obj': temp_obj,
                    }))
                    ind += 1

    # Step 3. Sort the results
    best_length = 1e10
    best_index = -1
    for index in omega[destination]:
        if best_length > obj_list[index][0]:
            best_length = obj_list[index][0]
            best_index = index
    if best_index == -1:
        return {}
    else:
        return {'cost': obj_list[best_index][0], 'time': obj_list[best_index][1], 'path': path_list[best_index]}


if __name__ == '__main__':
    test_network = {
        0: {1: [62, 50], 2: [44, 90], 3: [67, 10]},
        1: {0: [62, 50], 2: [33, 25], 4: [52, 90]},
        2: {0: [44, 90], 1: [33, 25], 3: [32, 10], 4: [52, 40]},
        3: {0: [67, 10], 2: [32, 10], 4: [54, 100]},
        4: {1: [52, 90], 2: [52, 40], 3: [54, 100]},
    }
    tw = {0: [113, 119], 1: [68, 131], 2: [77, 89], 3: [70, 79], 4: [39, 125]}
    source_node = 0
    destination_node = 4
    print(main(test_network, source_node, destination_node, tw))

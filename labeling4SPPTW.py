#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 11:28
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : labeling4SPPTW.py
# @Statement : The labeling algorithm for the shortest path problem with time windows
# @Reference : Desrochers M, Soumis F. A generalized permanent labelling algorithm for the shortest path problem with time windows[J]. INFOR: Information Systems and Operational Research, 1988, 26(3): 191-212.


def extract(label_set):
    # Dijkstra rule: extract the label with the minimum cost
    pop_lab = min(label_set, key=lambda x: x['cost'])
    label_set.remove(pop_lab)
    return pop_lab, label_set


def dominate(label1, label2):
    # label1 dominates label2, return 0; label2 dominates label1, return 1; else, return -1.
    cost1, time1, cost2, time2 = label1['cost'], label1['time'], label2['cost'], label2['time']
    if (cost1 <= cost2 and time1 < time2) or (cost1 < cost2 and time1 <= time2):
        return 0
    elif cost1 >= cost2 and time1 >= time2:
        return 1
    return -1


def add_label(label_set, labels, new_label, vertex2):
    # if new label is not dominated by existing labels, add the new label to the label set and remove dominated labels
    flag = True
    remove_dominated = []
    for temp_label in labels[vertex2]:
        flag_domination = dominate(new_label, temp_label)
        if flag_domination == 1:
            flag = False
            break
        elif flag_domination == 0:
            remove_dominated.append(temp_label)
    if flag:
        for item in remove_dominated:
            if item in label_set:
                label_set.remove(item)
            labels[vertex2].remove(item)
        label_set.append(new_label)
        labels[vertex2].append(new_label)
    return label_set, labels


def main(graph, s, d, tw):
    """
    The main function.
    :param graph: a directed graph {node1: {node2: [cost1, time1], node3: [cost2, time2], ...}, ...}
    :param s: the source node
    :param d: the destination node
    :param tw: time windows
    :return:
    """
    # Step 1. Initialization
    label_set = []
    labels = {}
    for vertex in graph:
        labels[vertex] = []
    first_label = {'path': [s], 'cost': 0, 'time': 0}
    labels[s].append(first_label)
    label_set.append(first_label)

    # Step 2. The main loop
    while label_set:
        temp_label, label_set = extract(label_set)
        temp_path, temp_cost, temp_time = temp_label['path'], temp_label['cost'], temp_label['time']
        vertex1 = temp_path[-1]
        for vertex2 in graph[vertex1]:
            if vertex2 not in temp_path and temp_time + graph[vertex1][vertex2][1] <= tw[vertex2][1]:
                new_path = temp_path.copy()
                new_path.append(vertex2)
                new_cost = temp_cost + graph[vertex1][vertex2][0]
                new_time = max(tw[vertex2][0], temp_time + graph[vertex1][vertex2][1])
                new_label = {'path': new_path, 'cost': new_cost, 'time': new_time}
                label_set, labels = add_label(label_set, labels, new_label, vertex2)

    # Step 3. Output
    if not labels[d]:
        print('No feasible solution!')
    else:
        best_label = min(labels[d], key=lambda x: x['cost'])
        print('cost = ' + str(best_label['cost']) + ', time = ' + str(best_label['time']) + ', path = ' + str(best_label['path']))


if __name__ == '__main__':
    test_graph = {
        0: {1: [62, 50], 2: [44, 90], 3: [67, 10]},
        1: {0: [62, 50], 2: [33, 25], 4: [52, 90]},
        2: {0: [44, 90], 1: [33, 25], 3: [32, 10], 4: [52, 40]},
        3: {0: [67, 10], 2: [32, 10], 4: [54, 100]},
        4: {1: [52, 90], 2: [52, 40], 3: [54, 100]},
    }
    time_window = {0: [113, 119], 1: [68, 131], 2: [77, 89], 3: [70, 79], 4: [39, 125]}
    main(test_graph, 0, 4, time_window)

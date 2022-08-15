### The Labeling Algorithm for the Shortest Path Problem with Time Windows

##### Reference: Desrochers M, Soumis F. A generalized permanent labelling algorithm for the shortest path problem with time windows[J]. INFOR: Information Systems and Operational Research, 1988, 26(3): 191-212.

The shortest path problem with time windows aims to determine the shortest path on a network with time windows.

| Variables   | Meaning                                                      |
| ----------- | ------------------------------------------------------------ |
| network     | Dictionary, {node1: {node2: [cost1, time1], node3: [cost2, time2] ...}, ...} |
| source      | The source node                                              |
| destination | The destination node                                         |
| nn          | The number of nodes                                          |
| nw          | The number of objectives                                     |
| neighbor    | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| ind         | The index of each label added to the priority queue          |
| ni          | The index of each label that is assessed as the Pareto-optimal subpath |
| omega       | List, omega[n] contains all the indexes of labels that are assessed as the Pareto-optimal subpath from the source node to node n (Pareto-optimal labels) |
| obj_list    | List, the objective value of the each Pareto-optimal label   |
| path_list   | List, the path of each Pareto-optimal label                  |
| queue       | The priority queue, which outputs the label that has the minimum value of the summation of objectives at each iteration |

#### Example

![SPPTW](C:\Users\dell\Desktop\研究生\个人算法主页\The labeling algorithm for the shortest path problem with time windows\SPPTW.png)

The red number associated with each arc is the cost, and the green number is the transit time. The time windows associated with each node are listed in the right.

```python
if __name__ == '__main__':
    test_network = {
        0: {1: [62, 50], 2: [44, 90], 3: [67, 10]},
        1: {0: [62, 50], 2: [33, 25], 4: [52, 90]},
        2: {0: [44, 90], 1: [33, 25], 3: [32, 10], 4: [52, 40]},
        3: {0: [67, 10], 2: [32, 10], 4: [54, 100]},
        4: {1: [52, 90], 2: [52, 40], 3: [54, 100]},
    }
    tw = {0: [0, 1e6], 1: [68, 131], 2: [77, 89], 3: [70, 79], 4: [39, 125]}
    source_node = 0
    destination_node = 4
    print(main(test_network, source_node, destination_node, tw))
```

##### Output:

```python
{
    'cost': 151, 
    'time': 120, 
    'path': [0, 3, 2, 4]，
}
```


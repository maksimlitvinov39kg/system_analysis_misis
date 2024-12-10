from math import log2
import json

def make_node(parent, children):
    return {"parent": parent, "children": children}

def rec_parse_input(parent, data, graph):
    desc = []
    for key, value in data.items():
        desc.append(key)
        if value:
            graph[key] = make_node(parent, rec_parse_input(key, value, graph))
        else:
            graph[key] = make_node(parent, [])
    return desc

def json_to_tree(json_string):
    graph = {}
    data = json.loads(json_string)
    rec_parse_input(None, data, graph)
    return graph

def siblings_list(graph, curr_key):
    parent = graph[curr_key]["parent"]
    return [key for key in graph if graph[key]["parent"] == parent and key != curr_key]

def calculate_parents(key, graph):
    count = 0
    while graph[key]["parent"] is not None:
        count += 1
        key = graph[key]["parent"]
    return count

def calculate_indirect_children(graph, children, counter):
    for child in children:
        counter[0] += 1
        calculate_indirect_children(graph, graph[child]["children"], counter)

def calculate_relations(graph):
    size = len(graph)
    result = [[0] * size for _ in range(5)]

    for curr_key, value in graph.items():
        idx = int(curr_key) - 1
        result[0][idx] = 1 if value["parent"] else 0
        result[1][idx] = len(value["children"])
        result[2][idx] = calculate_parents(curr_key, graph) - 1 if value["parent"] else 0

        counter = [0]
        calculate_indirect_children(graph, value["children"], counter)
        result[3][idx] = counter[0]

        result[4][idx] = len(siblings_list(graph, curr_key))

    return result

def calculate_entropy(matrix):
    n = len(matrix[0])
    total_entropy = 0

    for column in zip(*matrix):
        column_entropy = 0
        for value in column:
            if value > 0:
                probability = value / (n - 1)
                column_entropy -= probability * log2(probability)

        total_entropy += column_entropy

    return total_entropy

def parse_graph(data):
    graph = {}
    rec_parse_input(None, data, graph)
    return graph

def main(json_string):
    data = json.loads(json_string)
    graph = parse_graph(data)
    relations = calculate_relations(graph)
    entropy = calculate_entropy(relations)
    print(f"Calculated Entropy: {entropy:.2f}")

test_data = {
    "1": {
        "2": {
            "3": {
                "5": {},
                "6": {}
            },
            "4": {
                "7": {},
                "8": {}
            }
        }
    }
}
json_string = json.dumps(test_data)
main(json_string)

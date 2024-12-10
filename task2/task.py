import json

def parse_graph(data, parent=None):
    graph = {}
    for key, value in data.items():
        graph[key] = {"parent": parent, "children": list(value.keys())}
        graph.update(parse_graph(value, key))
    return graph

def calculate_relations(graph):
    keys = sorted(graph.keys(), key=int)
    n = len(keys)
    key_index = {key: i for i, key in enumerate(keys)}

    matrix = [[0] * n for _ in range(5)]

    for key, value in graph.items():
        idx = key_index[key]

        if value["parent"] is not None:
            parent_idx = key_index[value["parent"]]
            matrix[0][parent_idx] += 1

        matrix[1][idx] = len(value["children"])

        parent = value["parent"]
        depth = 0
        while parent is not None:
            depth += 1
            parent = graph[parent]["parent"]
        matrix[2][idx] = depth - 1 if value["parent"] is not None else 0
        
        def count_indirect_children(children):
            count = 0
            for child in children:
                count += 1 + count_indirect_children(graph[child]["children"])
            return count

        matrix[3][idx] = count_indirect_children(value["children"])

        if value["parent"] is not None:
            siblings = graph[value["parent"]]["children"]
            matrix[4][idx] = len(siblings) - 1

    return matrix

def main(json_string):
    data = json.loads(json_string)
    graph = parse_graph(data)
    relations = calculate_relations(graph)

    for row in relations:
        print(row)

test_input = '''{
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
}'''

main(test_input)

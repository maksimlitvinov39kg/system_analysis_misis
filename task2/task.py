import json
from collections import defaultdict

def extract_vertices(graph):
    vertices = set()

    def dfs(node):
        vertices.add(node)
        for child in graph.get(node, {}):
            dfs(child)

    for root in graph:
        dfs(root)

    return sorted(vertices)

def build_relation_matrix(graph):
    vertices = extract_vertices(graph)
    n = len(vertices)

    vertex_index = {v: i for i, v in enumerate(vertices)}
    
    r1 = [[0] * n for _ in range(5)]

    def dfs(node, parent=None):
        node_idx = vertex_index[node]
        if parent is not None:
            parent_idx = vertex_index[parent]
            r1[0][parent_idx] += 1
            r1[1][node_idx] += 1
            for sibling in graph[parent]:
                if sibling != node:
                    sibling_idx = vertex_index[sibling]
                    r1[4][node_idx] += 1
                    r1[4][sibling_idx] += 1
                    
        for child in graph.get(node, {}):
            dfs(child, node)

    def dfs_indirect(node, parent=None, depth=0):
        node_idx = vertex_index[node]
        if parent is not None and depth > 1:
            parent_idx = vertex_index[parent]
            r1[2][parent_idx] += 1
            r1[3][node_idx] += 1

        for child in graph.get(node, {}):
            dfs_indirect(child, node, depth + 1)

    for root in graph:
        dfs(root)
        dfs_indirect(root)

    return r1

input_data = '''
{
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
'''
def main(json_string):
    
    graph = json.loads(json_string)

    matrix = build_relation_matrix(graph)

    for row in matrix:
        print(row)

main(input_data)
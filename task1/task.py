import json

def build_graph(graph, parent=None, result=None):
    if result is None:
        result = {}
    
    for node, children in graph.items():
        result[node] = {
            'parent': parent,
            'children': list(children.keys())
        }
        build_graph(children, node, result)
    
    return result

def print_graph_info(graph_info):
    for node, info in graph_info.items():
        parent = info['parent']
        children = info['children']
        
        if parent is not None:
            siblings = [s for s in graph_info[parent]['children'] if s != node]
        else:
            siblings = []
        
        print(f"Вершина: {node}")
        print(f"        Братья: {siblings}")
        print(f"        Дети: {children}")

json_input = '''
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

graph = json.loads(json_input)

graph_info = build_graph(graph)

print_graph_info(graph_info)
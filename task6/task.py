import json
import typing as tp

class LinearFunction:
    def __init__(self, slope: float, intercept: float, left: float, right: float):
        self.slope = slope
        self.intercept = intercept
        self.left = left
        self.right = right

    def evaluate(self, x: float) -> float:
        return self.slope * x + self.intercept

    def __contains__(self, x: float) -> bool:
        return self.left <= x <= self.right


def calculate_linear_params(point1: tp.Tuple[float, float], point2: tp.Tuple[float, float]) -> LinearFunction:
    if point1[0] == point2[0]:
        return LinearFunction(0, point1[1], point1[0], point2[0])
    slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
    intercept = point1[1] - slope * point1[0]
    return LinearFunction(slope, intercept, point1[0], point2[0])


def generate_functions(data: tp.List[tp.List[float]]) -> tp.List[LinearFunction]:
    return [
        calculate_linear_params(data[i - 1], data[i])
        for i in range(1, len(data))
    ]


def prepare_data(input_data: tp.Dict[str, tp.List[tp.List[float]]]) -> tp.Dict[str, tp.List[LinearFunction]]:
    return {key: generate_functions(value) for key, value in input_data.items()}


def fuzzify(rule: str, value: float, functions: tp.Dict[str, tp.List[LinearFunction]]) -> float:
    for func in functions[rule]:
        if value in func:
            return max(0.0, func.evaluate(value))
    return 0.0


def activate(rule: str, value: float, functions: tp.Dict[str, tp.List[LinearFunction]]) -> float:
    for func in functions[rule]:
        if func.slope == 0:
            continue
        activation_point = (value - func.intercept) / func.slope
        if activation_point in func:
            return activation_point
    return 0.0


def main(input_value: float) -> float:
    temp_data = json.loads(INPUT)
    temp_functions = prepare_data(temp_data)

    regulator_data = json.loads(REGULATOR)
    regulator_functions = prepare_data(regulator_data)

    rules = json.loads(REGULATOR_RULES)
    fuzzified = {rule: fuzzify(rule, input_value, temp_functions) for rule in rules}
    activated = {
        rules[rule]: activate(rules[rule], fuzzified[rule], regulator_functions)
        for rule in rules
    }
    rule_strengths = [min(fuzzified[rule], activated[rules[rule]]) for rule in rules]

    best_rule_index = rule_strengths.index(max(rule_strengths))
    best_rule = list(activated.keys())[best_rule_index]

    for point in regulator_data[best_rule]:
        if point[1] == 1 and point[0] > activated[best_rule]:
            return point[0]
    return 0.0


INPUT = """{
    "холодно": [
        [0, 1],
        [16, 1],
        [20, 0],
        [50, 0]
    ],
    "комфортно": [
        [16, 0],
        [20, 1],
        [22, 1],
        [26, 0]
    ],
    "жарко": [
        [0,0],
        [22,0],
        [26,1],
        [50,1]
    ]
}"""

REGULATOR = """{
    "слабо":[[0,1],[6,1],[10,0],[20,0]],
    "умеренно":[[6,0],[10,1],[12,1],[16,0]],
    "интенсивно":[[0,0],[12,0],[16,1],[20,1]]
}"""

REGULATOR_RULES = """{
    "холодно":"интенсивно",
    "комфортно":"умеренно",
    "жарко":"слабо"
}"""

result = main(11)
print(result)

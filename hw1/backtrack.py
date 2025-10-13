def dfparse(s: str) -> list[int]:
    def parse(i: int):

        # Base case: Try rule (3): S -> ε
        yield True, i, [3]

        # Try rule (2): S -> b S a S
        if i < len(s) and s[i] == 'b':
            for success1, j, prod1 in parse(i + 1):
                if j < len(s) and s[j] == 'a':
                    for success2, k, prod2 in parse(j + 1):
                        yield True, k, [2] + prod1 + prod2

        # Try rule (1): S -> a S b S
        if i < len(s) and s[i] == 'a':
            for success1, j, prod1 in parse(i + 1):
                if j < len(s) and s[j] == 'b':
                    for success2, k, prod2 in parse(j + 1):
                        yield True, k, [1] + prod1 + prod2

    for success, pos, productions in parse(0):
        if success and pos == len(s): 
            return productions

    return []  # parsing failed
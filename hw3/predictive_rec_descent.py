
from typing import List, Tuple

precedences = {'or': 1, 'and': 2, 'not': 3, 'id': 4}

def is_id(tok: str) -> bool:
    return isinstance(tok, str) and len(tok) == 1 and 'a' <= tok <= 'z'

# Helper Functions

# paren_L(E = child_tokens, E.prec = child_prec, p = p)
def paren_L(child_tokens: List[str], child_prec: int, p: int) -> List[str]:
    if child_prec < p:
        return ['('] + child_tokens + [')']
    return child_tokens

# paren_R(E = child_tokens, E.prec = child_prec, p = p)
def paren_R(child_tokens: List[str], child_prec: int, p: int) -> List[str]:
    if child_prec <= p:
        return ['('] + child_tokens + [')']
    return child_tokens

# paren_unary(E = child_tokens, E.prec = child_prec, p = p)
def paren_unary(child_tokens: List[str], child_prec: int, p: int) -> List[str]:
    if child_prec < p:
        return ['('] + child_tokens + [')']
    return child_tokens

# Parser Class 
class Parser:
    def __init__(self, tokens: List[str]):
        self.toks = tokens
        self.i = 0

    # Lookahead function: looks at the next token without consuming it
    def lookahead(self):
        if self.i >= len(self.toks):
            return None
        else:
            return self.toks[self.i]

    # Match function: consumes the expected token if it matches the lookahead
    def match(self, expected: str):
        if self.lookahead() == expected:
            self.i += 1
        else:
            raise ValueError(f"PARSE_ERROR: expected {expected}, saw {self.lookahead()}")

    # Check if at the end of the token list
    def at_end(self) -> bool:
        return self.i >= len(self.toks)

    # Start function: entry point for parsing
    def start(self) -> List[str]:
        result_tokens, _prec = self.expr()
        if self.lookahead() == '$$':
            self.match('$$')
        if not self.at_end():
            raise ValueError("PARSE_ERROR: extra tokens at end")
        return result_tokens

    # Expr function: handles the grammar rules
    def expr(self) -> Tuple[List[str], int]:
        t = self.lookahead() # lookahead token
        # Based on the lookahead token, decide which production to use
        if t == 'or': 
            self.match('or')
            L_toks, L_p = self.expr() # parse left expr
            R_toks, R_p = self.expr() # parse right expr
            p = precedences['or'] 
            L = paren_L(L_toks, L_p, p) # add parentheses to left if needed
            R = paren_R(R_toks, R_p, p) # add parentheses to right if needed
            return (L + ['or'] + R, p)

        elif t == 'and': 
            self.match('and')
            L_toks, L_p = self.expr() # parse left expr
            R_toks, R_p = self.expr() # parse right expr
            p = precedences['and']
            L = paren_L(L_toks, L_p, p) # add parentheses to left if needed
            R = paren_R(R_toks, R_p, p) # add parentheses to right if needed
            return (L + ['and'] + R, p)

        elif t == 'not':
            self.match('not') 
            S_toks, S_p = self.expr() # parse sub expr
            p = precedences['not']
            S = paren_unary(S_toks, S_p, p) # add parentheses to sub expr if needed
            return (['not'] + S, p)

        elif is_id(t):
            self.match(t)  # consume the id
            return ([t], precedences['id'])

        else:
            raise ValueError("PARSE_ERROR: expected 'or' | 'and' | 'not' | id")
    
def parse(tokens: List[str]) -> str:
    toks = tokens
    try:
        p = Parser(toks)
        result_tokens = p.start()
        print(' '.join(result_tokens))
    except Exception:
        print('')


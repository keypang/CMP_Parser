from typing import List, Tuple, Union

# You may define ParseTree and ErrorReport in any way that fits your implementation.
# The below is a placeholder and should be modified.

class ParseTree:
    def __init__(self, symbol: str, children: List['ParseTree'] = None):
        self.symbol = symbol
        self.children = children if children else []

    def __str__(self):
        return self._build_tree()

    def __repr__(self):
        return self.__str__()

    def _build_tree(self, prefix="", is_tail=True):
        lines = []
        lines.append(f"{prefix}{'└── ' if is_tail else '├── '}{self.symbol}")
        for i, child in enumerate(self.children):
            is_last = i == (len(self.children) - 1)
            child_prefix = prefix + ("    " if is_tail else "│   ")
            lines.append(child._build_tree(child_prefix, is_last))
        return "\n".join(lines)

class ErrorReport:
    def __init__(self, position: int, message: str):
        self.position = position
        self.message = message


def parser(tokens: List[str]) -> Tuple[bool, Union[ParseTree, ErrorReport]]:
    tokens.append("$")  # end marker
    stack = [0]         # 상태 스택
    tree_stack = []     # 파스트리 스택
    index = 0

    while True:
        state = stack[-1]
        token = tokens[index]
        action = ACTION.get((state, token))

        if action is None:
            return False, ErrorReport(index, f"unexpected token '{token}'")

        if action[0] == "shift":
            stack.append(action[1])
            tree_stack.append(ParseTree(token))
            index += 1

        elif action[0] == "reduce":
            lhs, rhs = productions[action[1]]
            rhs_len = 0 if rhs == ['ε'] else len(rhs)
            children = tree_stack[-rhs_len:] if rhs_len > 0 else []
            del tree_stack[-rhs_len:]
            del stack[-rhs_len:]
            tree_stack.append(ParseTree(lhs, children))

            goto_state = GOTO.get((stack[-1], lhs))
            if goto_state is None:
                return False, ErrorReport(index, f"no GOTO for ({stack[-1]}, {lhs})")
            stack.append(goto_state)

        elif action[0] == "accept":
            return True, tree_stack[0]

ACTION = {
    (0, 'type'): ('shift', 5), (0, '$'): ('reduce', 2), 

    (1, '$'): ('accept', None),

    (2, 'type'): ('shift', 5), (2, '$'): ('reduce', 2), 

    (3, 'type'): ('reduce', 3), (3, 'id'): ('reduce', 3), 

    (4, 'type'): ('reduce', 4), (4, '$'): ('reduce', 4),

    (5, 'id'): ('shift', 7), 

    (6, '$'): ('reduce', 1), 

    (7, ';'): ('shift', 8), (7, '='): ('shift', 9), (4, '('): ('shift', 10), 

    (8, 'type'): ('reduce', 5), (8, 'id'): ('reduce', 5), (8, '{'): ('reduce', 5), (8, '}'): ('reduce', 5), (8, 'if'): ('reduce', 5),
    (8, 'else'): ('reduce', 5), (8, 'while'): ('reduce', 5), (8, 'for'): ('reduce', 5), (8, 'return'): ('reduce', 5), (8, '$'): ('reduce', 5),

    (9, 'id'): ('shift', 18), (9, '('): ('shift', 21), (9, '-'): ('shift', 16), (9, 'num'): ('shift', 20),

    (10, 'type'): ('shift', 24), (10, ')'): ('reduce', 10),
    
    (11, ';'): ('shift', 25), 

    (12, ';'): ('reduce', 29), (12, ')'): ('reduce', 29), (12, ','): ('reduce', 29), 

    (13, ';'): ('reduce', 30), (13, ')'): ('reduce', 30), (13, ','): ('reduce', 30), (13, '=='): ('shift', 26), (13, '+'): ('shift', 27), 

    (14, ';'): ('reduce', 32), (14, ')'): ('reduce', 32), (14, ','): ('reduce', 32), (13, '=='): ('reduce', 32), (13, '+'): ('reduce', 32), 
    (14, '*'): ('shift', 28), 

    (15, ';'): ('reduce', 34), (15, ')'): ('reduce', 34), (15, ','): ('reduce', 34), (15, '=='): ('reduce', 34), (15, '+'): ('reduce', 34), 
    (15, '*'): ('shift', 34),

    (16, 'id'): ('shift', 18), (16, '('): ('shift', 21), (16, '-'): ('shift', 16), (16, 'num'): ('shift', 20), 

    (17, 'id'): ('reduce', 37), (17, ')'): ('reduce', 37), (17, ','): ('reduce', 37), (17, '=='): ('reduce', 37), (17, '+'): ('reduce', 37),
    (17, '*'): ('reduce', 37),

    (18, 'id'): ('reduce', 40), (18, '('): ('shift', 30), (18, ')'): ('reduce', 40), (18, ','): ('reduce', 40), (18, '=='): ('reduce', 40),
    (18, '+'): ('reduce', 40), (18, '*'): ('reduce', 40),

    (19, 'id'): ('reduce', 39), (19, ')'): ('reduce', 39), (19, ','): ('reduce', 39), (19, '=='): ('reduce', 39), (19, '+'): ('reduce', 39),
    (19, '*'): ('reduce', 39),
    
    (20, 'id'): ('reduce', 41), (20, ')'): ('reduce', 41), (20, ','): ('reduce', 41), (20, '=='): ('reduce', 41), (20, '+'): ('reduce', 41),
    (20, '*'): ('reduce', 41),

    (21, 'id'): ('shift', 18), (21, '('): ('shift', 21), (21, '-'): ('shift', 16), (21, 'num'): ('shift', 20),

    (22, ')'): ('shift', 32),

    (23, ')'): ('reduce', 9), (23, ','): ('shift', 33),

    (24, 'id'): ('shift', 34),

    (25, 'type'): ('reduce', 6), (25, 'id'): ('reduce', 6), (25, '{'): ('reduce', 6), (25, '}'): ('reduce', 6), (25, 'if'): ('reduce', 6),
    (25, 'else'): ('reduce', 6), (25, 'while'): ('reduce', 6), (25, 'for'): ('reduce', 6), (25, 'return'): ('reduce', 6), (25, '$'): ('reduce', 6),

    (26, 'id'): ('shift', 18), (26, '('): ('shift', 21), (26, '-'): ('shift', 16), (26, 'num'): ('shift', 20),

    (27, 'id'): ('shift', 18), (27, '('): ('shift', 21), (27, '-'): ('shift', 16), (27, 'num'): ('shift', 20),

    (28, 'id'): ('shift', 18), (28, '('): ('shift', 21), (28, '-'): ('shift', 16), (28, 'num'): ('shift', 20),

    (29, ';'): ('reduce', 36), (29, ')'): ('reduce', 36), (29, ','): ('reduce', 36), (29, '=='): ('reduce', 36), (29, '+'): ('reduce', 36),
    (29, '*'): ('reduce', 36),

    (30, ';'): ('shift', 18), (30, ')'): ('shift', 21), (30, ','): ('reduce', 45), (30, '-'): ('shift', 16), (30, 'num'): ('shift', 20),

    (31, ')'): ('shift', 40),

    (32, '}'): ('shift', 42),

    (33, 'type'): ('shift', 24), (34, ')'): ('reduce', 10),

    (34, ')'): ('reduce', 11), (34, ','): ('reduce', 11),

    (35, ';'): ('reduce', 31), (35, ')'): ('reduce', 31), (35, ','): ('reduce', 31), (35, '+'): ('shift', 27),

    (36, ';'): ('reduce', 33), (36, ')'): ('reduce', 33), (36, ','): ('reduce', 33), (36, '=='): ('reduce', 33), (36, '+'): ('reduce', 33),
    (36, '*'): ('shift', 28),

    (37, ';'): ('reduce', 35), (37, ')'): ('reduce', 35), (37, ','): ('reduce', 35), (37, '=='): ('reduce', 35), (37, '+'): ('reduce', 35),
    (37, '*'): ('reduce', 35),

    (38, ')'): ('shift', 44),

    (39, ')'): ('reduce', 44), (39, ';'): ('shift', 45),

    (40, ';'): ('reduce', 42), (40, ')'): ('reduce', 42), (40, ','): ('reduce', 42), (40, '=='): ('reduce', 42), (40, '+'): ('reduce', 42),
    (40, '*'): ('reduce', 42),

    (41, ';'): ('reduce', 7), (41, '$'): ('reduce', 7),

    (42, 'type'): ('shift', 57), (42, 'id'): ('shift', 58), (42, '{'): ('shift', 42), (42, '}'): ('reduce', 14), (42, 'if'): ('shift', 50),
    (42, 'while'): ('shift', 51), (42, 'for'): ('shift', 52), (42, 'return'): ('shift', 53),

    (43, ')'): ('reduce', 8),

    (44, ';'): ('reduce', 38), (44, ')'): ('reduce', 38), (44, ','): ('reduce', 38), (44, '=='): ('reduce', 38), (44, '+'): ('reduce', 38),
    (44, '*'): ('reduce', 38),

    (45, 'id'): ('shift', 18), (45, '('): ('shift', 21), (45, ')'): ('reduce', 45), (45, '-'): ('shift', 16), (45, 'num'): ('shift', 20),

    (46, '}'): ('shift', 60),

    (47, 'type'): ('shift', 57), (47, 'id'): ('shift', 58), (47, '{'): ('shift', 42), (47, '}'): ('reduce', 14), (47, 'if'): ('shift', 50),
    (47, 'while'): ('shift', 51), (47, 'for'): ('shift', 52), (47, 'return'): ('shift', 53),

    (48, 'type'): ('reduce', 15), (48, 'id'): ('reduce', 15), (48, '{'): ('reduce', 15), (48, '}'): ('reduce', 15), (48, 'if'): ('reduce', 15),
    (48, 'while'): ('reduce', 15), (48, 'for'): ('reduce', 15), (48, 'return'): ('reduce', 15),

    (49, 'type'): ('reduce', 16), (49, 'id'): ('reduce', 16), (49, '{'): ('reduce', 16), (49, '}'): ('reduce', 16), (49, 'if'): ('reduce', 16),
    (49, 'while'): ('reduce', 16), (49, 'for'): ('reduce', 16), (49, 'return'): ('reduce', 16),

    (50, '('): ('shift', 62),

    (51, '('): ('shift', 63),

    (52, '('): ('shift', 64),

    (53, 'id'): ('shift', 18), (53, '('): ('shift', 21), (53, '-'): ('shift', 16), (53, 'num'): ('shift', 20),

    (54, 'type'): ('reduce', 21), (54, 'id'): ('reduce', 21), (54, '{'): ('reduce', 21), (54, '}'): ('reduce', 21), (54, 'if'): ('reduce', 21),
    (54, 'else'): ('reduce', 21), (54, 'while'): ('reduce', 21), (54, 'for'): ('reduce', 21), (54, 'return'): ('reduce', 21),

    (55, 'type'): ('reduce', 22), (55, 'id'): ('reduce', 22), (55, '{'): ('reduce', 22), (55, '}'): ('reduce', 22), (55, 'if'): ('reduce', 22),
    (55, 'else'): ('reduce', 22), (55, 'while'): ('reduce', 22), (55, 'for'): ('reduce', 22), (55, 'return'): ('reduce', 22),

    (56, 'type'): ('reduce', 23), (56, 'id'): ('reduce', 23), (56, '{'): ('reduce', 23), (56, '}'): ('reduce', 23), (56, 'if'): ('reduce', 23),
    (56, 'else'): ('reduce', 23), (56, 'while'): ('reduce', 23), (56, 'for'): ('reduce', 23), (56, 'return'): ('reduce', 23),

    (57, 'id'): ('shift', 66),

    (58, '='): ('shift', 67),

    (59, ')'): ('reduce', 43),

    (60, 'type'): ('reduce', 12), (60, 'id'): ('reduce', 12), (60, '{'): ('reduce', 12), (60, '}'): ('reduce', 12), (60, 'if'): ('reduce', 12),
    (60, 'else'): ('reduce', 12), (60, 'while'): ('reduce', 12), (60, 'for'): ('reduce', 12), (60, 'return'): ('reduce', 12), (60, '$'): ('reduce', 12),

    (61, '}'): ('reduce', 13),

    (62, 'id'): ('shift', 18), (62, '('): ('shift', 21), (62, '-'): ('shift', 20), (62, 'num'): ('shift', 16),

    (63, 'id'): ('shift', 18), (63, '('): ('shift', 21), (63, '-'): ('shift', 20), (63, 'num'): ('shift', 16),

    (64, 'id'): ('shift', 18), (64, '('): ('shift', 21), (64, '-'): ('shift', 20), (64, 'num'): ('shift', 20),
    
    (65, ';'): ('reduce', 71),
    
    (66, ';'): ('shift', 8), (66, '='): ('shift', 9),
    
    (67, 'id'): ('shift', 18), (67, '('): ('shift', 21), (67, '-'): ('shift', 20), (67, 'num'): ('shift', 20),
    
    (68, ')'): ('shift', 73),
    
    (69, ')'): ('shift', 74),
    
    (70, ';'): ('shift', 75),
    
    (71, 'type'): ('reduce', 20), (71, 'id'): ('reduce', 20), (71, '{'): ('reduce', 20), (71, '}'): ('reduce', 20), (71, 'if'): ('reduce', 20),
    (71, 'else'): ('reduce', 20), (71, 'while'): ('reduce', 20), (71, 'for'): ('reduce', 20), (71, 'return'): ('reduce', 20),
    
    (72, ';'): ('shift', 76),
    
    (73, 'type'): ('shift', 57), (73, 'id'): ('shift', 58), (73, '{'): ('shift', 42), (73, 'if'): ('shift', 50), (73, 'while'): ('shift', 51),
    (73, 'for'): ('shift', 52), (73, 'return'): ('shift', 53),
    
    (74, 'type'): ('shift', 57), (74, 'id'): ('shift', 58), (74, '{'): ('shift', 42), (74, 'if'): ('shift', 50), (74, 'while'): ('shift', 51),
    (74, 'for'): ('shift', 52), (74, 'return'): ('shift', 53),
    
    (75, '=='): ('reduce', 18), (75, '+'): ('reduce', 21), (75, '*'): ('reduce', 16), (75, '-'): ('reduce', 20),
    
    (76, 'type'): ('reduce', 28), (76, 'id'): ('reduce', 28), (76, '{'): ('reduce', 28), (76, '}'): ('reduce', 28), (76, 'if'): ('reduce', 28),
    (76, 'else'): ('reduce', 28), (76, 'while'): ('reduce', 28), (76, 'for'): ('reduce', 28), (76, 'return'): ('reduce', 28),
    
    (77, 'type'): ('reduce', 15), (77, 'id'): ('reduce', 15), (77, '{'): ('reduce', 15), (77, '}'): ('reduce', 15), (77, 'if'): ('reduce', 15),
    (77, 'else'): ('reduce', 82), (77, 'while'): ('reduce', 15), (77, 'for'): ('reduce', 15), (77, 'return'): ('reduce', 15),
    
    (78, 'type'): ('reduce', 24), (78, 'id'): ('reduce', 24), (78, '{'): ('reduce', 24), (78, '}'): ('reduce', 24), (78, 'if'): ('reduce', 24),
    (78, 'while'): ('reduce', 24), (78, 'for'): ('reduce', 24), (78, 'return'): ('reduce', 24),
    
    (79, 'type'): ('reduce', 18), (79, 'id'): ('reduce', 18), (79, '{'): ('reduce', 18), (79, '}'): ('reduce', 18), (79, 'if'): ('reduce', 18),
    (79, 'else'): ('reduce', 18), (79, 'while'): ('reduce', 18), (79, 'for'): ('reduce', 18), (79, 'return'): ('reduce', 18),
    
    (80, 'type'): ('reduce', 26), (80, 'id'): ('reduce', 26), (80, '{'): ('reduce', 26), (80, '}'): ('reduce', 26), (80, 'if'): ('reduce', 26),
    (80, 'while'): ('reduce', 26), (80, 'for'): ('reduce', 26), (80, 'return'): ('reduce', 26),
    
    (81, ';'): ('shift', 83),
    
    (82, 'type'): ('shift', 57), (82, 'id'): ('shift', 58), (82, '{'): ('shift', 42), (82, 'if'): ('shift', 50), (82, 'while'): ('shift', 51),
    (82, 'for'): ('shift', 52), (82, 'return'): ('shift', 53),
    
    (83, 'id'): ('shift', 18), (83, '('): ('shift', 21), (83, '-'): ('shift', 16), (83, 'num'): ('shift', 20),
    
    (84, 'type'): ('reduce', 17), (84, 'id'): ('reduce', 17), (84, '{'): ('reduce', 17), (84, '}'): ('reduce', 17), (84, 'if'): ('reduce', 17),
    (84, 'else'): ('reduce', 17), (84, 'while'): ('reduce', 17), (84, 'for'): ('reduce', 17), (84, 'return'): ('reduce', 17),
    
    (85, 'type'): ('reduce', 25), (85, 'id'): ('reduce', 25), (85, '{'): ('reduce', 25), (85, '}'): ('reduce', 25), (85, 'if'): ('reduce', 25),
    (85, 'while'): ('reduce', 25), (85, 'for'): ('reduce', 25), (85, 'return'): ('reduce', 25),
    
    (86, ')'): ('shift', 87),

    (87, 'type'): ('shift', 57), (87, 'id'): ('shift', 58), (87, '{'): ('shift', 42), (87, 'if'): ('shift', 50), (87, 'while'): ('shift', 51),
    (87, 'for'): ('shift', 52), (87, 'return'): ('shift', 53),
    
    (88, 'type'): ('reduce', 19), (88, 'id'): ('reduce', 19), (88, '{'): ('reduce', 19), (88, '}'): ('reduce', 19), (88, 'if'): ('reduce', 19),
    (88, 'else'): ('reduce', 19), (88, 'while'): ('reduce', 19), (88, 'for'): ('reduce', 19), (88, 'return'): ('reduce', 19),
    
    (89, 'type'): ('reduce', 27), (89, 'id'): ('reduce', 27), (89, '{'): ('reduce', 27), (89, '}'): ('reduce', 27), (89, 'if'): ('reduce', 27),
    (89, 'while'): ('reduce', 27), (89, 'for'): ('reduce', 27), (89, 'return'): ('reduce', 27),
}

GOTO = {
    (0, "DeclList"): 1, (0, "Decl"): 2, (0, "VarDecl"): 3, (0, "FunDecl"): 4,

    (2, "DeclList"): 6, (2, "Decl"): 2, (2, "VarDecl"): 3, (2, "FunDecl"): 4,

    (9, "Expr"): 11, (9, "EqualityExpr"): 12, (9, "AddExpr"): 13, (9, "MulExpr"): 14, (9, "UnaryExpr"): 15,
    (9, "PostfixExpr"): 17, (9, "PrimaryExpr"): 19,

    (10, "ParamList"): 22, (10, "Param"): 23,

    (16, "UnaryExpr"): 29, (16, "PostfixExpr"): 17, (16, "PrimaryExpr"): 19,
    
    (21, 'Expr'): 31, (21, 'EqualityExpr'): 12, (21, 'AddExpr'): 13, (21, 'MulExpr'): 14, (21, 'UnaryExpr'): 15,
    (21, 'PostfixExpr'): 17, (21, 'PrimaryExpr'): 19,

    (26, 'AddExpr'): 35, (26, 'MulExpr'): 14, (26, 'UnaryExpr'): 15, (26, 'PostfixExpr'): 17, (26, 'PrimaryExpr'): 19,

    (27, 'MulExpr'): 36, (27, 'UnaryExpr'): 15, (27, 'PostfixExpr'): 17, (27, 'PrimaryExpr'): 19,

    (28, 'UnaryExpr'): 37, (28, 'PostfixExpr'): 17, (28, 'PrimaryExpr'): 19,

    (30, 'Expr'): 39, (30, 'EqualityExpr'): 12, (30, 'AddExpr'): 13, (30, 'MulExpr'): 14, (30, 'UnaryExpr'): 15,
    (30, 'PostfixExpr'): 17, (30, 'PrimaryExpr'): 19, (30, 'ArgList'): 38,

    (32, 'Block'): 41,
    
    (33, "ParamList"): 43, (33, "Param"): 23,

    (42, 'VarDecl'): 54, (42, 'Block'): 56, (42, 'StmtList'): 46, (42, 'Stmt'): 47, (42, 'MatchedStmt'): 48,
    (42, 'UnmatchedStmt'): 49, (42, 'ExprStmt'): 55,

    (45, "Expr"): 39, (45, "EqualityExpr"): 12, (45, "AddExpr"): 13, (45, "MulExpr"): 14, (45, "UnaryExpr"): 15,
    (45, "PostfixExpr"): 17, (45, "PrimaryExpr"): 19, (45, "ArgList"): 59,

    (47, 'VarDecl'): 54, (47, 'Block'): 56, (47, 'StmtList'): 61, (47, 'Stmt'): 47, (47, 'MatchedStmt'): 48,
    (47, 'UnmatchedStmt'): 49, (47, 'ExprStmt'): 55,

    (53, "Expr"): 65, (53, "EqualityExpr"): 12, (53, "AddExpr"): 13, (53, "MulExpr"): 14, (53, "UnaryExpr"): 15,
    (53, "PostfixExpr"): 17, (53, "PrimaryExpr"): 19,

    (62, "Expr"): 68, (62, "EqualityExpr"): 12, (62, "AddExpr"): 13, (62, "MulExpr"): 14, (62, "UnaryExpr"): 15,
    (62, "PostfixExpr"): 17, (62, "PrimaryExpr"): 19,

    (63, "Expr"): 69, (63, "EqualityExpr"): 12, (63, "AddExpr"): 13, (63, "MulExpr"): 14, (63, "UnaryExpr"): 15,
    (63, "PostfixExpr"): 17, (63, "PrimaryExpr"): 19,

    (64, "Expr"): 70, (64, "EqualityExpr"): 12, (64, "AddExpr"): 13, (64, "MulExpr"): 14, (64, "UnaryExpr"): 15,
    (64, "PostfixExpr"): 17, (64, "PrimaryExpr"): 19,

    (67, "Expr"): 72, (67, "EqualityExpr"): 12, (67, "AddExpr"): 13, (67, "MulExpr"): 14, (67, "UnaryExpr"): 15,
    (67, "PostfixExpr"): 17, (67, "PrimaryExpr"): 19,

    (73, 'VarDecl'): 54, (73, 'Block'): 56, (73, 'Stmt'): 78, (73, 'MatchedStmt'): 77, (73, 'UnmatchedStmt'): 49,
    (73, 'ExprStmt'): 55,

    (74, 'VarDecl'): 54, (74, 'Block'): 56, (74, 'MatchedStmt'): 79, (74, 'UnmatchedStmt'): 80, (74, 'ExprStmt'): 55,

    (75, "Expr"): 81, (75, "EqualityExpr"): 12, (75, "AddExpr"): 13, (75, "MulExpr"): 14, (75, "UnaryExpr"): 15,
    (75, "PostfixExpr"): 17, (75, "PrimaryExpr"): 19,

    (82, 'VarDecl'): 54, (82, 'Block'): 56, (82, 'MatchedStmt'): 84, (82, 'UnmatchedStmt'): 85, (82, 'ExprStmt'): 55,

    (83, "Expr"): 86, (83, "EqualityExpr"): 12, (83, "AddExpr"): 13, (83, "MulExpr"): 14, (83, "UnaryExpr"): 15,
    (83, "PostfixExpr"): 17, (83, "PrimaryExpr"): 19,

    (87, 'VarDecl'): 54, (87, 'Block'): 56, (87, 'MatchedStmt'): 88, (87, 'UnmatchedStmt'): 89, (87, 'ExprStmt'): 55,
}

productions = [
    ("Program", ["DeclList"]),
    ("DeclList", ["Decl", "DeclList"]),
    ("DeclList", []),
    ("Decl", ["VarDecl"]),
    ("Decl", ["FuncDecl"]),
    ("VarDecl", ["type", "id", ";"]),
    ("VarDecl", ["type", "id", "=", "Expr", ";"]),
    ("FuncDecl", ["type", "id", "(", "ParamList", ")", "Block"]),
    ("ParamList", ["Param", ",", "ParamList"]),
    ("ParamList", ["Param"]),
    ("ParamList", []),
    ("Param", ["type", "id"]),
    ("Block", ["{", "StmtList", "}"]),
    ("StmtList", ["Stmt", "StmtList"]),
    ("StmtList", []),
    ("Stmt", ["MatchedStmt"]),
    ("Stmt", ["UnmatchedStmt"]),
    ("MatchedStmt", ["if", "(", "Expr", ")", "MatchedStmt", "else", "MatchedStmt"]),
    ("MatchedStmt", ["while", "(", "Expr", ")", "MatchedStmt"]),
    ("MatchedStmt", ["for", "(", "Expr", ";", "Expr", ";", "Expr", ")", "MatchedStmt"]),
    ("MatchedStmt", ["return", "Expr", ";"]),
    ("MatchedStmt", ["VarDecl"]),
    ("MatchedStmt", ["ExprStmt"]),
    ("MatchedStmt", ["Block"]),
    ("UnmatchedStmt", ["if", "(", "Expr", ")", "Stmt"]),
    ("UnmatchedStmt", ["if", "(", "Expr", ")", "MatchedStmt", "else", "UnmatchedStmt"]),
    ("UnmatchedStmt", ["while", "(", "Expr", ")", "UnmatchedStmt"]),
    ("UnmatchedStmt", ["for", "(", "Expr", ";", "Expr", ";", "Expr", ")", "UnmatchedStmt"]),
    ("ExprStmt", ["id", "=", "Expr", ";"]),
    ("Expr", ["EqualityExpr"]),
    ("EqualityExpr", ["AddExpr"]),
    ("EqualityExpr", ["AddExpr", "==", "AddExpr"]),
    ("AddExpr", ["MulExpr"]),
    ("AddExpr", ["AddExpr", "+", "MulExpr"]),
    ("MulExpr", ["UnaryExpr"]),
    ("MulExpr", ["MulExpr", "*", "UnaryExpr"]),
    ("UnaryExpr", ["-", "UnaryExpr"]),
    ("UnaryExpr", ["PostfixExpr"]),
    ("PostfixExpr", ["id", "(", "ArgList", ")"]),
    ("PostfixExpr", ["PrimaryExpr"]),
    ("PrimaryExpr", ["id"]),
    ("PrimaryExpr", ["num"]),
    ("PrimaryExpr", ["(", "Expr", ")"]),
    ("ArgList", ["Expr", ",", "ArgList"]),
    ("ArgList", ["Expr"]),
    ("ArgList", []),
]
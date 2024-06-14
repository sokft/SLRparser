import sys

class ParseNode:
    '''
    parse tree의 각 node(non-terminal & terminal) 표현
    '''
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children if children else []

class SLRParser:
    '''
    SLR parser 기능

    parameter
    ---------
    SLR_parsing_table : dict
        state 및 symbol에 따른 action을 정의한 SLR parsing table
    SLR_grammar : list
        SLR grammar

    attribute
    ---------
    stack : list
        파싱 state 및 symbol을 저장하는 스택
    input_buffer : list
        파싱할 input token 리스트
    error_message : str
        파싱 중 발생한 오류 메시지
    parse_tree : ParseNode
        parse tree의 root node
    '''
    def __init__(self, parsing_table, SLR_grammar):
        self.SLR_parsing_table = SLR_parsing_table  # SLR parsing table
        self.SLR_grammar = SLR_grammar  # SLR grammar
        self.stack = []  # 스택
        self.input_buffer = []  # 입력 버퍼
        self.error_message = None  # 오류 메시지
        self.parse_tree = None  # parse tree의 root node(start symbol)

    def initialize(self, input_tokens):
        '''
        input token 초기화
        
        parameter
        ---------
        input_tokens : list
            파싱할 input token 리스트
        
        action
        ---------
        스택을 초기 상태로 설정하고, 입력 버퍼에 end marker를 추가
        '''
        self.stack = [0]  # 초기 상태는 0
        self.input_buffer = input_tokens + ['$']  # end marker 추가

    def parse(self):
        '''
        입력을 파싱하여 syntax analyze를 수행하는 함수
        
        return
        ---------
        bool
            파싱 성공 시 True, 실패 시 False를 반환
        '''
        while True:
            state = self.stack[-1]  # 스택의 top에 있는 state를 가져옴
            symbol = self.input_buffer[0]  # 입력 버퍼의 첫 번째 symbol을 가져옴
            action = self.SLR_parsing_table[state].get(symbol)  # 현재 state와 symbol로 action 조회

            # action이 None인 경우 error 처리
            if action is None:
                self.error_message = f"Syntax Error: state {state}에서 symbol '{symbol}'에 대한 action 없음"
                return False

            # Shift인 경우
            if action.startswith('s'):
                self.shift(action[1:])
            # Reduce인 경우
            elif action.startswith('r'):
                if not self.reduce(action[1:], state, symbol):
                    return False
            # Accept인 경우
            elif action == 'acc':
                print("Accept!")
                self.parse_tree = self.stack[1]  # parse tree의 root node(start symbol) 설정
                return True
            # 기타 예외 처리
            else:
                return False

    def shift(self, state):
        '''
        Shift를 수행하는 함수
        
        parameter
        ---------
        state : str
            이동할 state 번호
        
        action
        ---------
        입력 버퍼에서 symbol을 제거하고, 스택에 새로운 node(non-terminal)와 state push
        '''
        symbol = self.input_buffer.pop(0)  # 입력 버퍼에서 symbol 제거
        node = ParseNode(symbol)  # 새로운 node 생성
        self.stack.append(node)  # node(non-terminal)를 스택에 푸시
        self.stack.append(int(state))  # 새로운 state를 스택에 푸시

    def reduce(self, rule_number, current_state, current_symbol):
        '''
        Reduce를 수행하는 함수
        
        parameter
        ---------
        rule_number : str
            적용할 grammar 번호
        current_state : int
            현재 state
        current_symbol : str
            현재 symbol
        
        return
        ---------
        bool
            Reduce 성공 시 True, 실패 시 False를 반환
        
        action
        ---------
        grammar 규칙에 따라 스택에서 state와 symbol를 제거하고 새로운 node(non-terminal)를 생성하여 push
        '''
        rule_number = int(rule_number)
        lhs, rhs = self.SLR_grammar[rule_number]  # reduce 번호에 해당하는 rule을 가져옴

        children = []
        if rhs != ['epsilon']:
            for _ in range(len(rhs)):
                self.stack.pop()  # state pop
                children.insert(0, self.stack.pop())  # symbol 제거 및 자식 리스트에 추가

        node = ParseNode(lhs, children)  # 새로운 node 생성
        self.stack.append(node)  # node를 스택에 푸시

        state = self.stack[-2]  # 스택의 새로운 최상위 state를 가져옴
        new_state = self.SLR_parsing_table[state].get(lhs)  # 새로운 state 조회

        if new_state is None:
            return False

        self.stack.append(new_state)  # 새로운 state를 스택에 푸시
        return True
    
    def get_error_message(self):
        return self.error_message

    def print_parse_tree(self, node, level=0):
        '''
        parse tree를 출력하는 함수
        
        parameter
        ---------
        node : ParseNode
            출력할 parse tree의 root node(start symbol)
        level : int
            현재 출력 중인 tree의 깊이 (기본값: 0)
        
        action
        ---------
        parse tree의 각 node를 재귀적으로 출력합니다.
        '''
        print(' ' * (level * 2) + str(node.symbol))  # 현재 node 출력
        for child in node.children:  # 자식 node에 대해 재귀적으로 출력
            self.print_parse_tree(child, level + 1)

# SLR parsing table
SLR_parsing_table = {
    0: {'vtype': 's4', '$': 'r3', 'CODE': 1, 'VDECL': 2, 'FDECL': 3},
    1: {'$': 'acc'},
    2: {'vtype': 's4', '$': 'r3', 'CODE': 5, 'VDECL': 2, 'FDECL': 3},
    3: {'vtype': 's4', '$': 'r3', 'CODE': 6, 'VDECL': 2, 'FDECL': 3},
    4: {'id': 's7', 'ASSIGN': 8},
    5: {'$': 'r1'},
    6: {'$': 'r2'},
    7: {'semi': 's9', 'assign': 's11', 'lparen': 's10'},
    8: {'semi': 's12'},
    9: {'vtype': 'r4', 'id': 'r4', 'rbrace': 'r4', 'if': 'r4', 'while': 'r4', 'return': 'r4', '$': 'r4'},
    10: {'vtype': 's14', 'rparen': 'r20', 'ARG': 13},
    11: {'id': 's23', 'literal': 's17', 'character': 's18', 'boolstr': 's19', 'lparen': 's22', 'num': 's24', 'RHS': 15, 'EXPR': 16, 'EXPR’': 20, 'EXPR’’': 21},
    12: {'vtype': 'r5', 'id': 'r5', 'rbrace': 'r5', 'if': 'r5', 'while': 'r5', 'return': 'r5', '$': 'r5'},
    13: {'rparen': 's25'},
    14: {'id': 's26'},
    15: {'semi': 'r6'},
    16: {'semi': 'r7', 'addsub': 's27'},
    17: {'semi': 'r8'},
    18: {'semi': 'r9'},
    19: {'semi': 'r10'},
    20: {'semi': 'r12', 'addsub': 'r12', 'multdiv': 's28', 'rparen': 'r12'},
    21: {'semi': 'r14', 'addsub': 'r14', 'multdiv': 'r14', 'rparen': 'r14'},
    22: {'id': 's23', 'lparen': 's22', 'num': 's24', 'EXPR': 29, 'EXPR’': 20, 'EXPR’’': 21},
    23: {'semi': 'r16', 'addsub': 'r16', 'multdiv': 'r16', 'rparen': 'r16'},
    24: {'semi': 'r17', 'addsub': 'r17', 'multdiv': 'r17', 'rparen': 'r17'},
    25: {'lbrace': 's30'},
    26: {'rparen': 'r22', 'comma': 's32', 'MOREARGS': 31},
    27: {'id': 's23', 'lparen': 's22', 'num': 's24', 'EXPR’': 33, 'EXPR’’': 21},
    28: {'id': 's23', 'lparen': 's22', 'num': 's24', 'EXPR’’': 34},
    29: {'addsub': 's27', 'rparen': 's35'},
    30: {'vtype': 's42', 'id': 's43', 'rbrace': 'r24', 'if': 's40', 'while': 's41', 'return': 'r24', 'VDECL': 38, 'ASSIGN': 39, 'BLOCK': 36, 'STMT': 37},
    31: {'rparen': 'r19'},
    32: {'vtype': 's44'},
    33: {'semi': 'r11', 'addsub': 'r11', 'multdiv': 's28', 'rparen': 'r11'},
    34: {'semi': 'r13', 'addsub': 'r13', 'multdiv': 'r13', 'rparen': 'r13'},
    35: {'semi': 'r15', 'addsub': 'r15', 'multdiv': 'r15', 'rparen': 'r15'},
    36: {'return': 's46', 'RETURN': 45},
    37: {'vtype': 's42', 'id': 's43', 'rbrace': 'r24', 'if': 's40', 'while': 's41', 'return': 'r24', 'VDECL': 38, 'ASSIGN': 39, 'BLOCK': 47, 'STMT': 37},
    38: {'vtype': 'r25', 'id': 'r25', 'rbrace': 'r25', 'if': 'r25', 'while': 'r25', 'return': 'r25'},
    39: {'semi': 's48'},
    40: {'lparen': 's49'},
    41: {'lparen': 's50'},
    42: {'id': 's51', 'ASSIGN': 8},
    43: {'assign': 's11'},
    44: {'id': 's52'},
    45: {'rbrace': 's53'},
    46: {'id': 's23', 'literal': 's17', 'character': 's18', 'boolstr': 's19', 'lparen': 's22', 'num': 's24', 'RHS': 54, 'EXPR': 16, 'EXPR’': 20, 'EXPR’’': 21},
    47: {'rbrace': 'r23', 'return': 'r23'},
    48: {'vtype': 'r26', 'id': 'r26', 'rbrace': 'r26', 'if': 'r26', 'while': 'r26', 'return': 'r26'},
    49: {'boolstr': 's57', 'COND': 55, 'COND’': 56},
    50: {'boolstr': 's57', 'COND': 58, 'COND’': 56},
    51: {'semi': 's9', 'assign': 's11'},
    52: {'rparen': 'r22', 'comma': 's32', 'MOREARGS': 59},
    53: {'vtype': 'r18', '$': 'r18'},
    54: {'semi': 's60'},
    55: {'rparen': 's61', 'comp': 's62', 'COND': 62, 'COND’': 57},
    56: {'rparen': 'r30', 'comp': 'r30'},
    57: {'rparen': 'r31', 'comp': 'r31'},
    58: {'rparen': 's63', 'comp': 's62', 'COND': 62, 'COND’': 57},
    59: {'rparen': 'r21'},
    60: {'rbrace': 'r34'},
    61: {'lbrace': 's64'},
    62: {'boolstr': 's57', 'COND’': 65},
    63: {'lbrace': 's66'},
    64: {'vtype': 's42', 'id': 's43', 'rbrace': 'r24', 'if': 's40', 'while': 's41', 'return': 'r24', 'VDECL': 38, 'ASSIGN': 39, 'BLOCK': 67, 'STMT': 37},
    65: {'rparen': 'r29', 'return': 'r29'},
    66: {'vtype': 's42', 'id': 's43', 'rbrace': 'r24', 'if': 's40', 'while': 's41', 'return': 'r24', 'VDECL': 38, 'ASSIGN': 39, 'BLOCK': 68, 'STMT': 37},
    67: {'rbrace': 's69'},
    68: {'rbrace': 's70'},
    69: {'vtype': 'r33', 'id': 'r33', 'rbrace': 'r33', 'if': 'r33', 'while': 'r33', 'else': 's72', 'return': 'r33', 'ELSE': 71},
    70: {'vtype': 'r28', 'id': 'r28', 'rbrace': 'r28', 'if': 'r28', 'while': 'r28', 'return': 'r28'},
    71: {'vtype': 'r27', 'id': 'r27', 'rbrace': 'r27', 'if': 'r27', 'while': 'r27', 'return': 'r27'},
    72: {'lbrace': 's73'},
    73: {'vtype': 's42', 'id': 's43', 'rbrace': 'r24', 'if': 's40', 'while': 's41', 'return': 'r24', 'VDECL': 38, 'ASSIGN': 39, 'BLOCK': 74, 'STMT': 37},
    74: {'rbrace': 's75'},
    75: {'vtype': 'r32', 'id': 'r32', 'rbrace': 'r32', 'if': 'r32', 'while': 'r32', 'return': 'r32'}
}

# SLR grammar
SLR_grammar = [
    ("S'", ["CODE"]),
    ("CODE", ["VDECL", "CODE"]),
    ("CODE", ["FDECL", "CODE"]),
    ("CODE", ["epsilon"]),
    ("VDECL", ["vtype", "id", "semi"]),
    ("VDECL", ["vtype", "ASSIGN", "semi"]),
    ("ASSIGN", ["id", "assign", "RHS"]),
    ("RHS", ["EXPR"]),
    ("RHS", ["literal"]),
    ("RHS", ["character"]),
    ("RHS", ["boolstr"]),
    ("EXPR", ["EXPR", "addsub", "EXPR’"]),
    ("EXPR", ["EXPR’"]),
    ("EXPR’", ["EXPR’", "multdiv", "EXPR’’"]),
    ("EXPR’", ["EXPR’’"]),
    ("EXPR’’", ["lparen", "EXPR", "rparen"]),
    ("EXPR’’", ["id"]),
    ("EXPR’’", ["num"]),
    ("FDECL", ["vtype", "id", "lparen", "ARG", "rparen", "lbrace", "BLOCK", "RETURN", "rbrace"]),
    ("ARG", ["vtype", "id", "MOREARGS"]),
    ("ARG", ["epsilon"]),
    ("MOREARGS", ["comma", "vtype", "id", "MOREARGS"]),
    ("MOREARGS", ["epsilon"]),
    ("BLOCK", ["STMT", "BLOCK"]),
    ("BLOCK", ["epsilon"]),
    ("STMT", ["VDECL"]),
    ("STMT", ["ASSIGN", "semi"]),
    ("STMT", ["if", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace", "ELSE"]),
    ("STMT", ["while", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace"]),
    ("COND", ["COND", "comp", "COND’"]),
    ("COND", ["COND’"]),
    ("COND’", ["boolstr"]),
    ("ELSE", ["else", "lbrace", "BLOCK", "rbrace"]),
    ("ELSE", ["epsilon"]),
    ("RETURN", ["return", "RHS", "semi"])
]

# input file 입력으로 받아서 처리
input_file = sys.argv[1]
with open(input_file, 'r') as file:
    input = file.read()

# parser 초기화
parser = SLRParser(SLR_parsing_table, SLR_grammar)
input_tokens = input.split()
parser.initialize(input_tokens)

# parser 실행 및 결과 출력
if parser.parse():
    print("\n-----Generate Parse Tree-----")
    parser.print_parse_tree(parser.parse_tree)
else:
    print("Reject!\n")
    print(parser.get_error_message())


"""
NarayanganjScript - A programming language in Narayanganj dialect
Simple and easy to explain version
"""

# ========== PART 1: TOKENIZER ==========
class Tokenizer:
    """Breaks code into small pieces (tokens)"""
    
    keywords = {
        'jodi': 'IF', 'naile': 'ELSE', 'jotokhon': 'WHILE',
        'a': 'IS', 'rakho': 'STORE', 'dekha': 'SHOW',
        'er_sathe': 'PLUS', 'gun': 'TIMES', 'vag': 'DIVIDE',
        'shoman': 'EQUAL', 'beshi': 'GREATER', 'kom': 'LESS'
    }
    
    def tokenize(self, code):
        """Convert Narayanganj code to tokens"""
        tokens = []
        current = ""
        
        for char in code:
            if char in ' \n\t;(){}':
                if current:
                    tokens.append(self.get_token(current))
                    current = ""
                if char == ';':
                    tokens.append(('SEMI', ';'))
                elif char == '(':
                    tokens.append(('LPAREN', '('))
                elif char == ')':
                    tokens.append(('RPAREN', ')'))
                elif char == '{':
                    tokens.append(('LBRACE', '{'))
                elif char == '}':
                    tokens.append(('RBRACE', '}'))
            elif char.isdigit():
                if current and not current.isdigit():
                    tokens.append(self.get_token(current))
                    current = char
                else:
                    current += char
            elif char == '"':
                tokens.append(('STRING', current))
                current = ""
            else:
                current += char
        
        if current:
            tokens.append(self.get_token(current))
        
        return tokens
    
    def get_token(self, word):
        """Identify what type of token this is"""
        if word in self.keywords:
            return (self.keywords[word], word)
        elif word.isdigit():
            return ('NUMBER', int(word))
        elif word.startswith('"'):
            return ('STRING', word.strip('"'))
        else:
            return ('NAME', word)

# ========== PART 2: PARSER ==========
class Parser:
    """Builds a tree structure from tokens"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        """Parse all statements"""
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements
    
    def parse_statement(self):
        """Parse one statement at a time"""
        
        # Assignment: x a 5 rakho;
        if self.current()[0] == 'NAME' and self.peek()[0] == 'IS':
            name = self.eat('NAME')[1]
            self.eat('IS')  # 'a'
            
            # Get value (number or expression)
            if self.current()[0] == 'NUMBER':
                value = ('NUMBER', self.eat('NUMBER')[1])
            else:
                value = self.parse_expression()
            
            # Optional 'rakho'
            if self.current()[0] == 'STORE':
                self.eat('STORE')
            
            self.eat('SEMI')
            return ('ASSIGN', name, value)
        
        # Print: "Hello" dekha; or x dekha;
        elif self.current()[0] == 'STRING' or (self.current()[0] == 'NAME' and self.peek()[0] == 'SHOW'):
            if self.current()[0] == 'STRING':
                value = self.eat('STRING')
            else:
                value = self.parse_expression()
            
            self.eat('SHOW')  # 'dekha'
            self.eat('SEMI')
            return ('PRINT', value)
        
        # If statement: jodi (condition) { ... } naile { ... }
        elif self.current()[0] == 'IF':
            self.eat('IF')  # 'jodi'
            self.eat('LPAREN')
            
            # Parse condition: x shoman 5
            left = self.parse_expression()
            op = self.eat()[0]  # 'EQUAL', 'GREATER', 'LESS'
            right = self.parse_expression()
            condition = ('COMPARE', op, left, right)
            
            self.eat('RPAREN')
            self.eat('LBRACE')
            
            # Parse then block
            then_block = []
            while self.current()[0] != 'RBRACE':
                then_block.append(self.parse_statement())
            self.eat('RBRACE')
            
            # Parse else block (optional)
            else_block = []
            if self.current()[0] == 'ELSE':
                self.eat('ELSE')  # 'naile'
                self.eat('LBRACE')
                while self.current()[0] != 'RBRACE':
                    else_block.append(self.parse_statement())
                self.eat('RBRACE')
            
            return ('IF', condition, then_block, else_block)
        
        # While loop: jotokhon (condition) { ... }
        elif self.current()[0] == 'WHILE':
            self.eat('WHILE')  # 'jotokhon'
            self.eat('LPAREN')
            
            # Parse condition
            left = self.parse_expression()
            op = self.eat()[0]
            right = self.parse_expression()
            condition = ('COMPARE', op, left, right)
            
            self.eat('RPAREN')
            self.eat('LBRACE')
            
            # Parse loop body
            body = []
            while self.current()[0] != 'RBRACE':
                body.append(self.parse_statement())
            self.eat('RBRACE')
            
            return ('WHILE', condition, body)
        
        self.pos += 1
        return None
    
    def parse_expression(self):
        """Parse mathematical expressions"""
        if self.current()[0] == 'NUMBER':
            return self.eat('NUMBER')
        elif self.current()[0] == 'NAME':
            return self.eat('NAME')
        elif self.current()[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr
    
    def current(self):
        """Get current token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')
    
    def peek(self):
        """Look at next token without eating it"""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return ('EOF', '')
    
    def eat(self, expected=None):
        """Consume current token"""
        token = self.current()
        if expected and token[0] != expected:
            raise SyntaxError(f"Expected {expected}, got {token[0]}")
        self.pos += 1
        return token

# ========== PART 3: INTERPRETER ==========
class Interpreter:
    """Executes the parsed code"""
    
    def __init__(self):
        self.variables = {}
    
    def execute(self, ast):
        """Execute all statements"""
        for stmt in ast:
            self.execute_statement(stmt)
    
    def execute_statement(self, stmt):
        """Execute one statement"""
        
        # Assignment
        if stmt[0] == 'ASSIGN':
            _, name, value = stmt
            self.variables[name] = self.get_value(value)
        
        # Print
        elif stmt[0] == 'PRINT':
            _, value = stmt
            print(self.get_value(value))
        
        # If statement
        elif stmt[0] == 'IF':
            _, condition, then_block, else_block = stmt
            
            if self.evaluate_condition(condition):
                for s in then_block:
                    self.execute_statement(s)
            else:
                for s in else_block:
                    self.execute_statement(s)
        
        # While loop
        elif stmt[0] == 'WHILE':
            _, condition, body = stmt
            
            while self.evaluate_condition(condition):
                for s in body:
                    self.execute_statement(s)
    
    def get_value(self, value):
        """Get actual value from token"""
        if value[0] == 'NUMBER':
            return value[1]
        elif value[0] == 'STRING':
            return value[1]
        elif value[0] == 'NAME':
            if value[1] in self.variables:
                return self.variables[value[1]]
            raise NameError(f"Variable '{value[1]}' not defined")
    
    def evaluate_condition(self, condition):
        """Evaluate comparison"""
        _, op, left, right = condition
        
        left_val = self.get_value(left)
        right_val = self.get_value(right)
        
        if op == 'EQUAL':
            return left_val == right_val
        elif op == 'GREATER':
            return left_val > right_val
        elif op == 'LESS':
            return left_val < right_val

# ========== PART 4: MAIN COMPILER ==========
class NarayanganjScript:
    """Main compiler class - puts everything together"""
    
    @staticmethod
    def run(code):
        print("=" * 40)
        print(" NARAYANGANJSCRIPT ")
        print("=" * 40)
        print(f"Code:\n{code}")
        print("-" * 40)
        
        # Step 1: Tokenize
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(code)
        print("Tokens:", tokens)
        
        # Step 2: Parse
        parser = Parser(tokens)
        ast = parser.parse()
        print("\nAST (Tree Structure):", ast)
        
        # Step 3: Execute
        interpreter = Interpreter()
        print("\nOutput:")
        interpreter.execute(ast)
        print(f"\nFinal Variables: {interpreter.variables}")

# ========== EXAMPLE USAGE ==========
if __name__ == "__main__":
    # Example 1: Simple calculation
    code1 = """
    x a 10 rakho
    y a 5 rakho
    jog a x er_sathe y rakho
    "Jogfol:" dekha
    jog dekha
    """
    
    # Example 2: If statement
    code2 = """
    x a 15 rakho
    jodi (x beshi 10) {
        "x 10 er beshi" dekha
    } naile {
        "x 10 er kom" dekha
    }
    """
    
    # Example 3: While loop
    code3 = """
    count a 1 rakho
    jotokhon (count kom 5) {
        count dekha
        count a count er_sathe 1 rakha
    }
    """
    
    print("\n" + "="*40)
    print("EXAMPLE 1 - SIMPLE CALCULATION")
    print("="*40)
    NarayanganjScript.run(code1)
    
    print("\n" + "="*40)
    print("EXAMPLE 2 - IF STATEMENT")
    print("="*40)
    NarayanganjScript.run(code2)
    
    print("\n" + "="*40)
    print("EXAMPLE 3 - WHILE LOOP")
    print("="*40)
    NarayanganjScript.run(code3)
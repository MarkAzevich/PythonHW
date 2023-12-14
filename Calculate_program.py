import flask

class Calculator:
    def __init__(self):
        self.operators = {'+': 1, '-': 1, '*': 2, '/': 2}
        self.unary_operators = {'-'}
        self.parentheses = {'(', ')'}

    def tokenize(self, expression):
        tokens = []
        current_token = ''
        open_parentheses_count = 0
        error_message = ""
        for i, char in enumerate(expression):
            if char.isdigit() or char == '.':
                current_token += char
            elif char in self.operators or char in self.parentheses:
                if current_token:
                    tokens.append(float(current_token))
                    current_token = ''
                if char in self.unary_operators and (i == 0 or expression[i-1] in self.operators or expression[i-1] in self.parentheses):
                    current_token += char
                else:
                    tokens.append(char)
                    if char == '(':
                        open_parentheses_count += 1
                    elif char == ')':
                        open_parentheses_count -= 1
            elif char != ' ':
                error_message = "Incorrect input: invalid character"
        if open_parentheses_count < 0:
            error_message = "Invalid expression: mismatched parentheses"
        if current_token:
            tokens.append(float(current_token))
        if open_parentheses_count != 0:
            error_message = "Invalid expression: mismatched parentheses"
        if error_message:
            return error_message
        return tokens

    
    def to_rpn(self, tokens):
        output = []
        operators_stack = []
        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self.operators:
                while operators_stack and operators_stack[-1] in self.operators and self.operators[token] <= self.operators[operators_stack[-1]]:
                    output.append(operators_stack.pop())
                operators_stack.append(token)
            elif token == '(':
                operators_stack.append(token)
            elif token == ')':
                while operators_stack and operators_stack[-1] != '(':
                    output.append(operators_stack.pop())
                if operators_stack and operators_stack[-1] == '(':
                    operators_stack.pop()
        while operators_stack:
            output.append(operators_stack.pop())
        return output

    def calculate(self, expression):
        tokens = self.tokenize(expression)
        if isinstance(tokens, str):
            return tokens
        rpn = self.to_rpn(tokens)
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.operators:
                if len(stack) < 2:
                    return 'Invalid expression'
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == '*':
                    result = operand1 * operand2
                elif token == '/':
                    if operand2 == 0:
                        return 'Division by zero'
                    result = operand1 / operand2
                stack.append(result)
        if len(stack) != 1:
            return 'Invalid expression'
        return stack[0]


app = flask.Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = flask.request.form.get('expression')
    try:
        result = Calculator().calculate(expression)
        return flask.jsonify({'result': result})
    except Exception as e:
        return flask.jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

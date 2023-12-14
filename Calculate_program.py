import flask

class Calculator:
    def calculate(self, expression):
        # Удаляем пробелы из выражения
        expression = expression.replace(" ", "")
        
        # Проверяем наличие скобок в выражении
        if "(" in expression or ")" in expression:
            # Рекурсивно вычисляем значение выражения внутри скобок
            return self.calculate_with_brackets(expression)
        
        # Разделяем выражение на числа и операции
        numbers = []
        operators = []
        number = ""
        
        for i, char in enumerate(expression):
            if char.isdigit() or char == ".":
                number += char
            elif (char == "-" or char == "+") and (i == 0 or expression[i-1] in ["+", "-", "*", "/"]):
                # Учитываем унарный минус
                number += char
            else:
                if number:
                    numbers.append(float(number))
                    number = ""
                
                if char in ["+", "-", "*", "/"]:
                    operators.append(char)
        
        if number:
            numbers.append(float(number))
        
        # Вычисляем умножение и деление слева направо
        i = 0
        while i < len(operators):
            if operators[i] == "*":
                numbers[i] *= numbers[i+1]
                del numbers[i+1]
                del operators[i]
            elif operators[i] == "/":
                if numbers[i+1] != 0:
                    numbers[i] /= numbers[i+1]
                    del numbers[i+1]
                    del operators[i]
                else:
                    return "Ошибка: деление на ноль"
            else:
                i += 1
        
        # Вычисляем сложение и вычитание слева направо
        result = numbers[0]
        
        for i in range(len(operators)):
            if operators[i] == "+":
                result += numbers[i+1]
            elif operators[i] == "-":
                result -= numbers[i+1]
        
        return result


    def calculate_with_brackets(self, expression):
        # Находим самую внутреннюю пару скобок
        start = expression.rfind("(")
        end = expression.find(")", start)
        
        # Вычисляем значение выражения внутри скобок
        value = self.calculate(expression[start+1:end])
        
        # Заменяем выражение внутри скобок на его значение
        expression = expression[:start] + str(value) + expression[end+1:]
        
        # Если в выражении остались скобки, рекурсивно вычисляем их значения
        if "(" in expression or ")" in expression:
            return self.calculate_with_brackets(expression)
        else:
            return self.calculate(expression)




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




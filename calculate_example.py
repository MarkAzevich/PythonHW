import requests

expression = "50*0.999 - 1"

# Создаем JSON-объект с математическим выражением
data = {'expression': expression}

# Отправляем POST-запрос на API-точку `/calculate`
response = requests.post('http://localhost:5000/calculate', data=data)

# Получаем результат вычисления выражения из ответа
result = response.json()['result']
#print(response.json())
print("Результат:", result)

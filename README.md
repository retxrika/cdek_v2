# Библиотека для работы со СДЭК'ом

Примеры использования:

- Авторизация.

```python
from cdek2 import CDEK2Client

cdek_client = CDEK2Client('your_client_id', 'your_client_secret')
```

- Получение всех пунктов выдачи.

```python
cities = cdek_client.get_delivery_points()

for city in cities:
  print(city)
```

- Расчет суммы доставки заказа.

```python
goods = [
    {
        'weight': 1000,
        'length': 10,
        'width': 10,
        'height': 10,
    },
]

cost = cdek_client.get_delivery_cost(sender_city_code=250, receiver_city_code=7, goods=goods)
print(cost['delivery_sum'])
```

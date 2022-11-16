# cdek_v2

## Оглавление
1. [Авторизация](#Авторизация)
2. [Получение всех пунктов выдачи](#Получение_всех_пунктов_выдачи)
3. [Расчет суммы доставки заказ](#Расчет_суммы_доставки_заказ)
4. [Цель](#Цель)

<a name="Авторизация"></a> 
- ### Авторизация.

```python
from cdek_v2 import CDEK2Client

cdek_client = CDEK2Client('your_client_id', 'your_client_secret')
```

<a name="Получение_всех_пунктов_выдачи"></a> 
- ### Получение всех пунктов выдачи.

```python
cities = cdek_client.get_delivery_points()

for city in cities:
  print(city)
```

<a name="Расчет_суммы_доставки_заказ"></a>
- ### Расчет суммы доставки заказа.

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

<a name="Цель"></a>
- ### Цель

Библиотека создана под вторую версию протокола API СДЭК'а и используется для расчета стоимости доставки для интернет-магазинов. 

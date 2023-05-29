import requests

from typing import Dict, Optional
from boltons.iterutils import remap

class CDEK2Client:
    __CDEK_URL = 'https://api.cdek.ru'
    __AUTH_URL = '/v2/oauth/token?parameters'
    __DELIVERY_POINTS_URL = '/v2/deliverypoints'
    __DELIVERY_COST_URL = '/v2/calculator/tariff'
    __HEADER_REQUEST = None

    def __init__(
            self, 
            client_id : str, 
            client_secret : str, 
            grant_type : str = 'client_credentials',
    ):
        # Генерация заголовка запроса.
        self.__HEADER_REQUEST = self.__get_header_request(
                                        grant_type=grant_type,
                                        client_id=client_id,
                                        client_secret=client_secret)

    def __exec_request(
            self, 
            url: str, 
            data: Dict = None, 
            method: str = 'GET',
    ) -> requests.Response:
        '''
        Возвращает ответ сервера на отправленный запрос.

        url - Путь к требуемому методу.
        data - Параметры запроса.
        method - POST/GET.
        '''

        if isinstance(data, dict):
            data = remap(data, lambda p, k, v: v is not None)

        url = self.__CDEK_URL + url

        if method == 'GET':
            response = requests.get(
                            url=url, 
                            headers=self.__HEADER_REQUEST, 
                            params=data)
        elif method == 'POST':
            if self.__HEADER_REQUEST == None:
                response = requests.post(
                                url=url, 
                                params=data)
            else:
                response = requests.post(
                                url=url, 
                                headers=self.__HEADER_REQUEST, 
                                json=data)
        else:
            raise NotImplementedError(f'Unknown method "{method}"')

        response.raise_for_status()

        return response

    def __get_header_request(
            self, 
            grant_type : str, 
            client_id : str,
            client_secret : str
    ) -> Dict[str, str]:
        '''
        Возвращает заголовок запроса с токеном авторизации 
        и форматом JSON (Content-Type: application/json).

        grant_type - Тип аутентификации, доступное значение.
        client_id - идентификатор клиента, равен Accoun.
        client_secret - секретный ключ клиента, равен Secure password.
        '''
        data = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        response = self.__exec_request(
                            url=self.__AUTH_URL, 
                            data=data, 
                            method='POST',
                    ).json()

        access_token = response['token_type'].capitalize() + \
                            ' ' + response['access_token']
        header = {
                    'Authorization': access_token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json', 
                }
        return header

    def get_delivery_points(
            self, 
            city_code: int = None,
            type: str = 'PVZ',
            country_code: str = 'RU',
    ) -> Optional[Dict]:
        '''
        Возвращает пункты выдачи заказов.

        city_code - Код населенного пункта СДЭК.
        type - Тип офиса, может принимать значения (PVZ/POSTAMAT/ALL).
        country_code - Код страны в формате ISO_3166-1_alpha-2.
        '''
            
        data = {
            'city_code': city_code,
            'type': type,
            'country_code': country_code,
        }
        response = self.__exec_request(
                        url=self.__DELIVERY_POINTS_URL, 
                        data=data,
                    ).json()
        return response

    def get_delivery_cost(
            self,
            sender_city_code : int,
            receiver_city_code : int,
            goods: Optional[Dict],
            tariff_code: int = 483, # Экспресс склад-склад.
    ) -> Dict:
        '''
        Возвращает стоимость доставки.

        sender_city_code - Код населенного пункта отправителя СДЭК.
        receiver_city_code - Код населенного пункта получателя СДЭК.
        goods - Товары в виде списка, пример:
        [
            {
                'weight': 1000,
                'length': 10,
                'width': 10,
                'height': 10,
            },
        ]
        tariff_code - Код тарифа СДЭК.
        '''
        data = {
            'tariff_code': tariff_code,
            'from_location': {
                'code': sender_city_code, 
            },
            'to_location': {
                'code': receiver_city_code,
            },
            'packages': goods,
        }
        response = self.__exec_request(
                        url=self.__DELIVERY_COST_URL, 
                        data=data, 
                        method='POST',
                    ).json()
        return response


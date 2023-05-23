import requests
import json
from progress.bar import ChargingBar
from urllib.parse import urlencode


class YA():


    def __init__(self, 
                url_photo, 
                name_photo, 
                size
                ):
        self.token = open('token_YA.txt').read()
        self.url_photo = url_photo
        self.headers = {
                        'Content-Type': 'application/json', 
                        'Authorization': self.token
                        }
        self.params = {'path':'disk:/'}
        self.name_folder = 'diplom_sorokin'
        self.name_photo = name_photo
        self.size = size


    def create_folder(self):
        bar_create_folder = ChargingBar(
            'Создание/Проверка папки для фото', 
            max = 100
            )
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        info_folder = requests.get(
                                url, 
                                headers={**self.headers}, 
                                params={**self.params}
                                )
        count_files = len(info_folder.json()['_embedded']['items'])
        bar_create_folder.next(25)
        for count in range(int(count_files)):
            bar_create_folder.next(25)
            type_files = info_folder.json()['_embedded']['items'][count]['type']
            count_name_folder = info_folder.json()['_embedded']['items'][count]['name']
            if (type_files == 'dir'):
                if (self.name_folder != count_name_folder):
                    params = dict(
                                path = 
                                self.params.get('path') 
                                + self.name_folder
                                  )  
                    requests.put(
                                url, 
                                headers={**self.headers}, 
                                params={**params}
                                )
        bar_create_folder.finish()
        return


    def loading_profile_picture(self):
        bar_loading_profile_picture = ChargingBar(
            'Загрузка файла на диски', 
            max = 100
            )
        bar_loading_profile_picture.next(25)
        url_loading = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        bar_loading_profile_picture.next(25)
        params = dict(path = 
                        self.params.get('path') 
                        + self.name_folder 
                        + '/' 
                        + self.name_photo 
                        + '.jpg', 
                     url = self.url_photo
                    )
        bar_loading_profile_picture.next(25)
        succsesful = requests.post( 
                                    url_loading, 
                                    params={**params}, 
                                    headers={**self.headers}
                                )
        bar_loading_profile_picture.next(25)
        info_file = {
                    'file_name':self.name_photo 
                    + '.jpg', 'size':self.size 
                    }
        bar_loading_profile_picture.finish()
        return succsesful, info_file
    
    def dowland_photo(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/download?'
        path = f'path=/{self.name_folder}/{self.name_photo}.jpg'
        response = requests.get(url+path,  headers={**self.headers})
        download_url = response.json()['href']
        return download_url

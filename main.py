import os
import random

import requests
from dotenv import load_dotenv


def get_request_random_xkcd():
    last_comics_url = 'https://xkcd.com/info.0.json'
    last_comics_response = requests.get(last_comics_url)
    last_comics_response.raise_for_status()
    total_comics_number = last_comics_response.json()['num']
    start_comics_number = 1
    comics_number = random.randint(start_comics_number, total_comics_number)
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    image_url = response.json()['img']
    comment = response.json()['alt']
    return image_url, comment


def download_picture(filename):
    image_url = get_request_random_xkcd()[0]
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_request_vk(vk_method, params):
    url = f'https://api.vk.com/method/{vk_method}'
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_upload_url_vk(vk_access_token, vk_api_version):
    vk_method = 'photos.getWallUploadServer'
    params = {
        'access_token': vk_access_token,
        'v': vk_api_version
        }
    vk_upload_url = get_request_vk(vk_method, params)['response']['upload_url']
    return vk_upload_url


def upload_photo_vk(vk_access_token, vk_api_version, filename):
    with open(filename, 'rb') as file:
        url = get_upload_url_vk(vk_access_token, vk_api_version)
        files = {'photo': file}
        response = requests.post(url, files=files)
        response.raise_for_status()
        upload_photo_response = response.json()
        vk_server = upload_photo_response['server']
        vk_photo = upload_photo_response['photo']
        vk_hash = upload_photo_response['hash']
        return vk_server, vk_photo, vk_hash


def saving_result_vk(vk_access_token, vk_api_version, filename):
    vk_method = 'photos.saveWallPhoto'
    vk_server, vk_photo, vk_hash = upload_photo_vk(
        vk_access_token, vk_api_version, filename
        )
    params = {'access_token': vk_access_token,
              'v': vk_api_version,
              'server': vk_server,
              'photo': vk_photo,
              'hash': vk_hash}
    response = get_request_vk(vk_method, params)
    owner_id = response['response'][0]['owner_id']
    photo_id = response['response'][0]['id']
    return owner_id, photo_id


def posting_photo_vk(vk_access_token, vk_api_version, filename):
    vk_method = 'wall.post'
    comment = get_request_random_xkcd()[1]
    owner_id, photo_id = saving_result_vk(
        vk_access_token, vk_api_version, filename
    )
    vk_group_id = -215288801
    params = {'access_token': vk_access_token,
              'v': vk_api_version,
              'owner_id': vk_group_id,
              'message': comment,
              'attachments': f'photo{owner_id}_{photo_id}'}
    response = get_request_vk(vk_method, params)
    return response


def deleted_local_file(filename):
    os.remove(filename)


if __name__ == '__main__':
    load_dotenv()
    filename = 'python.png'
    vk_api_version = 5.131
    vk_client_id = os.environ['VK_CLIENT_ID']
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    download_picture(filename)
    posting_photo_vk(vk_access_token, vk_api_version, filename)
    deleted_local_file(filename)

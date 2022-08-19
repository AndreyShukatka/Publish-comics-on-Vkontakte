import os
import random
import logging

import requests
from dotenv import load_dotenv


class VK_API_Error(Exception):
    pass


def find_vk_api_error(response):
    if 'error' in response:
        raise VK_API_Error(response['error']['error_msg'])


def request_random_xkcd():
    last_comics_url = 'https://xkcd.com/info.0.json'
    last_comics_response = requests.get(last_comics_url)
    last_comics_response.raise_for_status()
    total_comics_number = last_comics_response.json()['num']
    start_comics_number = 1
    comics_number = random.randint(start_comics_number, total_comics_number)
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response_data = response.json()
    image_url = response_data['img']
    comment = response_data['alt']
    return image_url, comment


def download_comic(filename, image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def request_vk(vk_method, params):
    url = f'https://api.vk.com/method/{vk_method}'
    response = requests.get(url, params=params)
    response_data = response.json()
    response.raise_for_status()
    find_vk_api_error(response_data)
    return response_data


def get_upload_vk_url(vk_access_token, vk_api_version):
    vk_method = 'photos.getWallUploadServer'
    params = {
        'access_token': vk_access_token,
        'v': vk_api_version
    }
    vk_upload_url = request_vk(vk_method, params)['response']['upload_url']
    return vk_upload_url


def upload_vk_photo(vk_access_token, vk_api_version, filename):
    with open(filename, 'rb') as file:
        url = get_upload_vk_url(vk_access_token, vk_api_version)
        files = {'photo': file}
        response = requests.post(url, files=files)
    response.raise_for_status()
    response_data = response.json()
    find_vk_api_error(response_data)
    upload_photo_response = response.json()
    vk_server = upload_photo_response['server']
    vk_photo = upload_photo_response['photo']
    vk_hash = upload_photo_response['hash']
    return vk_server, vk_photo, vk_hash


def save_vk_result(vk_access_token, vk_api_version, filename):
    vk_method = 'photos.saveWallPhoto'
    vk_server, vk_photo, vk_hash = upload_vk_photo(
        vk_access_token, vk_api_version, filename
    )
    params = {
        'access_token': vk_access_token,
        'v': vk_api_version,
        'server': vk_server,
        'photo': vk_photo,
        'hash': vk_hash
    }
    response = request_vk(vk_method, params)
    owner_id = response['response'][0]['owner_id']
    photo_id = response['response'][0]['id']
    return owner_id, photo_id


def post_vk_photo(
        vk_access_token,
        vk_api_version,
        filename,
        vk_group_id,
        comment
):
    vk_method = 'wall.post'
    owner_id, photo_id = save_vk_result(
        vk_access_token,
        vk_api_version,
        filename
    )
    vk_group_id = vk_group_id
    params = {
        'access_token': vk_access_token,
        'v': vk_api_version,
        'owner_id': vk_group_id,
        'message': comment,
        'attachments': f'photo{owner_id}_{photo_id}'
    }
    response = request_vk(vk_method, params)
    return response


if __name__ == '__main__':
    load_dotenv()
    filename = 'python.png'
    vk_api_version = 5.131
    vk_group_id = os.environ['VK_GROUP_ID']
    vk_client_id = os.environ['VK_CLIENT_ID']
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    try:
        image_url, comment = request_random_xkcd()
        download_comic(filename, image_url)
        post_vk_photo(
            vk_access_token,
            vk_api_version,
            filename,
            vk_group_id,
            comment
        )
    except VK_API_Error as VK_Error:
        logging.error(VK_Error)
    finally:
        os.remove(filename)

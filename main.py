import os
from random import randint

import requests
from dotenv import load_dotenv

from prepare_images import get_image, save_image, IMAGES_PATH


def check_errors_in_vk_response(vk_response):
    if 'error' in vk_response:
        raise requests.exceptions.HTTPError(vk_response['error'])


def get_random_xckd_comic_page_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()

    xckd_comic_pages_count = response.json()['num']

    random_xckd_comic_page_number = randint(1, xckd_comic_pages_count)

    return random_xckd_comic_page_number


def get_xckd_comic_page(page_number):
    url = 'https://xkcd.com/{}/info.0.json'.format(page_number)
    response = requests.get(url)
    response.raise_for_status()

    xckd_comic_page = response.json()

    return xckd_comic_page


def get_vk_wall_upload_address(vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': vk_group_id,
        'access_token': vk_access_token,
        'v': 5.103
    }

    response = requests.get(url, params=payload)
    vk_wall_upload_address = response.json()
    check_errors_in_vk_response(vk_wall_upload_address)

    return vk_wall_upload_address


def upload_image_to_vk_server(path_to_image, vk_wall_upload_url):
    with open(path_to_image, 'rb') as file:
        url = vk_wall_upload_url
        files = {
            'photo': file,
        }

        response = requests.post(url, files=files)
        vk_server_upload_image_response = response.json()
        check_errors_in_vk_response(vk_server_upload_image_response)

    return vk_server_upload_image_response


def save_image_on_vk_server(vk_access_token,
                            vk_group_id,
                            vk_uploaded_image,
                            vk_server,
                            vk_uploaded_image_hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'group_id': vk_group_id,
        'photo': vk_uploaded_image,
        'server': vk_server,
        'hash': vk_uploaded_image_hash,
        'access_token': vk_access_token,
        'v': 5.103
    }

    response = requests.post(url, data=payload)
    vk_server_save_image_response = response.json()
    check_errors_in_vk_response(vk_server_save_image_response)

    return vk_server_save_image_response


def post_image_to_vk_wall(vk_access_token,
                          vk_group_id,
                          vk_saved_image_owner_id,
                          vk_saved_image_media_id,
                          message):
    url = 'https://api.vk.com/method/wall.post'
    attachments = 'photo{}_{}'.format(
        vk_saved_image_owner_id,
        vk_saved_image_media_id,
    )
    payload = {
        'owner_id': '-{}'.format(vk_group_id),
        'from_group': 1,
        'message': message,
        'attachments': attachments,
        'access_token': vk_access_token,
        'v': 5.103
    }

    response = requests.post(url, data=payload)
    vk_server_post_image_to_wall_response = response.json()
    check_errors_in_vk_response(vk_server_post_image_to_wall_response)

    return vk_server_post_image_to_wall_response


def main():
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')

    page_number = get_random_xckd_comic_page_number()
    xckd_comic_page = get_xckd_comic_page(page_number)
    xckd_comic_page_img_link = xckd_comic_page['img']
    xckd_comic_page_text = xckd_comic_page['alt']

    xckd_comic_page_img = get_image(xckd_comic_page_img_link)
    image_name = 'xkcd_{}.png'.format(page_number)
    save_image(xckd_comic_page_img, image_name, IMAGES_PATH)

    vk_wall_upload_address = get_vk_wall_upload_address(
        vk_access_token,
        vk_group_id
    )

    vk_wall_upload_url = vk_wall_upload_address['response']['upload_url']

    path_to_image = os.path.join(IMAGES_PATH, image_name)
    vk_server_upload_image_response = upload_image_to_vk_server(
        path_to_image,
        vk_wall_upload_url
    )
    vk_server = vk_server_upload_image_response['server']
    vk_uploaded_image = vk_server_upload_image_response['photo']
    vk_uploaded_image_hash = vk_server_upload_image_response['hash']

    vk_server_save_image_response = save_image_on_vk_server(
        vk_access_token,
        vk_group_id,
        vk_uploaded_image,
        vk_server,
        vk_uploaded_image_hash
    )
    vk_saved_image_media_id = vk_server_save_image_response['response'][0]['id']
    vk_saved_image_owner_id = vk_server_save_image_response['response'][0]['owner_id']

    post_id = post_image_to_vk_wall(
        vk_access_token,
        vk_group_id,
        vk_saved_image_owner_id,
        vk_saved_image_media_id,
        xckd_comic_page_text
    )

    path_to_file = IMAGES_PATH + image_name
    os.remove(path_to_file)


if __name__ == '__main__':
    main()

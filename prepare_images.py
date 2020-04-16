import os
import argparse

import requests
from pathlib import Path
from PIL import Image


IMAGES_PATH = os.path.join("images",'')


def get_image(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    image = response.content

    return image


def save_image(image, filename, images_path):
    Path(images_path).mkdir(parents=True, exist_ok=True)

    image_path = images_path + filename
    with open(image_path, 'wb') as file:
        file.write(image)


def get_file_extension(filename):
    file_extension = filename.split('.')[-1]

    return file_extension


def resize_images(images_path, image_resolution):
    """Resize images for your resolution

    Some image extension, like .tif can't use .save method in Pillow,
    if it's format not RGB. Thats why this function convert all images to
    RGB format.
    """
    resized_images_folder_name = 'resized_images'
    resized_images_path = os.path.join(images_path, resized_images_folder_name, '')
    Path(resized_images_path).mkdir(parents=True, exist_ok=True)

    images_names = os.listdir(images_path)
    images_names.remove(resized_images_folder_name)

    for image_name in images_names:
        image = Image.open(images_path + image_name)
        image.thumbnail(image_resolution)
        resized_image_name = 'resized_{}.jpg'.format(image_name.split('.')[0])

        rgb_im = image.convert('RGB')
        rgb_im.save(resized_images_path + resized_image_name , format="JPEG")


def main():
    parser = argparse.ArgumentParser(
        description='This script resize downloads images. All images must be in the images folder of your script root directory.'
    )
    parser.add_argument('--width', help='Input required images width. Default width: 1080')
    parser.add_argument('--height', help='Input required images height. Default height: 1080')
    args = parser.parse_args()

    image_width = args.width if args.width else 1080
    image_height = args.height if args.height else 1080

    image_resolution = (image_width, image_height)
    resize_images(IMAGES_PATH, image_resolution)  #be carefull, this function convert image to RGB format.


if __name__ == '__main__':
    main()

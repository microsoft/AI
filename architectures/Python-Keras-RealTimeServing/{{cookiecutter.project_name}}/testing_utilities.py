import json
import logging
import random
import time
import urllib
from io import BytesIO

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import toolz
from PIL import Image, ImageOps
from azureml.core.authentication import AuthenticationException, AzureCliAuthentication, InteractiveLoginAuthentication


def read_image_from(url):
    return toolz.pipe(url, urllib.request.urlopen, lambda x: x.read(), BytesIO)


def to_rgb(img_bytes):
    return Image.open(img_bytes).convert("RGB")


@toolz.curry
def resize(img_file, new_size=(100, 100)):
    return ImageOps.fit(img_file, new_size, Image.ANTIALIAS)


def to_bytes(img, encoding="JPEG"):
    imgio = BytesIO()
    img.save(imgio, encoding)
    imgio.seek(0)
    return imgio.read()


def to_img(img_url):
    return toolz.pipe(img_url, read_image_from, to_rgb, resize(new_size=(224, 224)))


def _plot_image(ax, img):
    ax.imshow(to_img(img))
    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelleft=False,
        labelbottom=False,
    )
    return ax


def _plot_prediction_bar(ax, r):
    perf = [float(c[2]) for c in r.json()[0]["image"]]
    ax.barh(range(3, 0, -1), perf, align="center", color="#55DD55")
    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelbottom=False,
    )
    tick_labels = reversed([c[1] for c in r.json()[0]["image"]])
    ax.yaxis.set_ticks([1, 2, 3])
    ax.yaxis.set_ticklabels(
        tick_labels, position=(0.5, 0), minor=False, horizontalalignment="center"
    )


def plot_predictions(images, classification_results):
    if len(images) != 6:
        raise Exception("This method is only designed for 6 images")
    gs = gridspec.GridSpec(2, 3)
    fig = plt.figure(figsize=(12, 9))
    gs.update(hspace=0.1, wspace=0.001)

    for gg, r, img in zip(gs, classification_results, images):
        gg2 = gridspec.GridSpecFromSubplotSpec(4, 10, subplot_spec=gg)
        ax = fig.add_subplot(gg2[0:3, :])
        _plot_image(ax, img)
        ax = fig.add_subplot(gg2[3, 1:9])
        _plot_prediction_bar(ax, r)


def write_json_to_file(json_dict, filename, mode="w"):
    with open(filename, mode) as outfile:
        json.dump(json_dict, outfile, indent=4, sort_keys=True)
        outfile.write("\n\n")


def gen_variations_of_one_image(IMAGEURL, num):
    out_images = []
    img = to_img(IMAGEURL).convert("RGB")
    # Flip the colours for one-pixel
    # "Different Image"
    for i in range(num):
        diff_img = img.copy()
        rndm_pixel_x_y = (
            random.randint(0, diff_img.size[0] - 1),
            random.randint(0, diff_img.size[1] - 1),
        )
        current_color = diff_img.getpixel(rndm_pixel_x_y)
        diff_img.putpixel(rndm_pixel_x_y, current_color[::-1])
        out_images.append(to_bytes(diff_img))
    return out_images


def get_auth():
    logger = logging.getLogger(__name__)
    logger.debug("Trying to create Workspace with CLI Authentication")
    try:
        auth = AzureCliAuthentication()
        auth.get_authentication_header()
    except AuthenticationException:
        logger.debug("Trying to create Workspace with Interactive login")
        auth = InteractiveLoginAuthentication()
    return auth


def wait_until_ready(endpoint, max_attempts):
    code = 0
    attempts = 0
    while code != 200:
        attempts += 1
        if attempts == max_attempts:
            print("Unable to connect to endpoint, quitting")
            raise Exception(
                "Endpoint unavailable in " + str(max_attempts) + " attempts."
            )
            break
        try:
            code = urllib.request.urlopen(endpoint).getcode()
        except Exception as error:
            print(
                "Exception caught opening endpoint :" + str(endpoint) + " " + str(error)
            )

        if code != 200:
            print("Endpoint unavailable, waiting")
            time.sleep(10)

    output_str = "We are all done with code " + str(code)
    return output_str

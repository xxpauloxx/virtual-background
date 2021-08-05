import click
import cv2

import numpy
import time
import pyfakewebcam

from tf_bodypix.api import BodyPixModelPaths, download_model, load_model

KEY_ESC = 27

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

bodypixmodel = load_model(
    download_model(BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16)
)


def read_background_file(file):
    """Read background file using opencv and apply color and return image."""
    background_file = cv2.imread(file)
    background_file = background_file[:FRAME_HEIGHT , :FRAME_WIDTH , :]
    return cv2.cvtColor(background_file, cv2.COLOR_BGR2RGB)


def modify_frame_with_background_file(frame, background_image):
    """Detect body and return modified frame with background image file."""
    background_image = read_background_file(background_image)
    body_prediction = bodypixmodel.predict_single(frame)

    mask = body_prediction.get_mask(threshold=0.5).numpy().astype(numpy.uint8)
    masked_image = cv2.bitwise_and(frame, frame, mask=mask)

    negative = numpy.add(mask, -1)
    inverse = numpy.where(negative==-1, 1, negative).astype(numpy.uint8)

    masked_background = cv2.bitwise_and(
        background_image, background_image, mask=inverse)
    return cv2.add(masked_image, masked_background)


def start_virtual_webcam(webcam, virtual_webcam, background):
    """Start image proccess and virtual webcam with background image."""
    while True:
        _, frame = webcam.read()
        frame = cv2.convertScaleAbs(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), alpha=1.5, beta=0)

        virtual_webcam.schedule_frame(
            modify_frame_with_background_file(frame, background))

        keyboard_key = cv2.waitKey(30) & 0xff
        if keyboard_key == KEY_ESC:
            break
        time.sleep(0.01)

    webcam.release()


def get_webcam(webcam_device):
    """Get webcam instance of OpenCV."""
    webcam = cv2.VideoCapture(webcam_device)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    return webcam


@click.command()
@click.option('--virtual-webcam-device', default='/dev/video4', help='Virtual webcam device')
@click.option('--webcam-device', default=0, help='Webcam device')
@click.option('--background', default='./images/background.jpg', help='Background image')
def handle_parameters_app(virtual_webcam_device, webcam_device, background):
    """Handle parameters that will be used to start the application."""
    virtual_webcam = pyfakewebcam.FakeWebcam(
        video_device=virtual_webcam_device, width=FRAME_WIDTH, height=FRAME_HEIGHT)
    webcam = get_webcam(webcam_device)

    start_virtual_webcam(
        webcam=webcam, virtual_webcam=virtual_webcam, background=background)


if __name__ == '__main__':
    handle_parameters_app()
    cv2.destroyAllWindows()

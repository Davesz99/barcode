from pyzbar import pyzbar
from glob import glob
import cv2


def decode(image):
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
#        print("detected barcode:", obj)
        image = draw_barcode(obj, image)
        print("Type:", obj.type)
        print("Data:", obj.data)
        print()

    return image


def draw_barcode(decoded, image):
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                          (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                          color=(0, 255, 0),
                          thickness=2)
    return image


barcodes = glob("barcode*.jpg")

for barcode_file in barcodes:
    img = cv2.imread(barcode_file)
    img = decode(img)
    cv2.imshow("img", img)
    cv2.waitKey(0)

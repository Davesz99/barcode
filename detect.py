import cv2
import numpy as np


def detect(img):
    scale_percent = 640/img.shape[1]
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) #kép méretezés

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    ret, thresh =cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)#bináris
    kernel = np.ones((3, 10), np.uint8)
    thresh = cv2.dilate(thresh, kernel)# morfologiai szureessel noveljuk a kep feher tartomanyat
    # cv2.imshow("titlee", thresh);
    # cv2.waitKey(0);
    original_sized = cv2.resize(thresh, (img.shape[1],img.shape[0]), interpolation = cv2.INTER_LINEAR )# eredeti méretre vissza
    contours, hierarchy = cv2.findContours(original_sized,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)#kontur keresés

    # img_contours = np.zeros(img.shape)
    # cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 1)
    # cv2.imshow("title", original_sized);
    # cv2.imshow("titlee", img_contours);
    # cv2.waitKey(0);

    candidates = []
    index = 0
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)# minimális méretű téglalap, akár elforgatással
        box = cv2.boxPoints(rect)# a téglalap 4 sarka
        box = np.int0(box)#egész konvertálás

        cropped = crop_rect(rect,box,img)
        width = cropped.shape[1]
        #Az EAN13 minimális mérete 95 pixel
        if width>95:
                candidate = {"cropped": cropped, "rect": rect}#itt volt
                candidates.append(candidate)
        index = index + 1
    return candidates

def crop_rect(rect, box, img):
    W = rect[1][0]
    H = rect[1][1]
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)

    # a téglalap közepe
    center = ((x1+x2)/2,(y1+y2)/2)
    # Az elforgatott téglalapot határoló függőleges téglalap mérete
    size = (x2-x1, y2-y1)

    #kerekítés miatt újra kiszámoljuk
    #Egy képpontos téglalapot szubpixel pontossággal kér le a képről.
    cropped = cv2.getRectSubPix(img, size, center)
    angle = rect[2]
    if angle != 90:
        if angle > 45:
            angle = 0 - (90 - angle)
        else:
            angle = angle

        M = cv2.getRotationMatrix2D((size[0] / 2, size[1] / 2), angle, 1.0)

        cropped = cv2.warpAffine(cropped, M, size)
        croppedW = H if H > W else W
        croppedH = H if H < W else W
        # Final cropped & rotated rectangle
        croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW), int(croppedH)), (size[0] / 2, size[1] / 2))
        return croppedRotated
    return cropped

if __name__ == "__main__":
    image = cv2.imread("Dataset1/05102009210.jpg")
    candidates = detect(image)
    for i in range(len(candidates)):
        candidate = candidates[i]
        cv2.imshow(str(i), candidate["cropped"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

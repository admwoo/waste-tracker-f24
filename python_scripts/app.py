import requests
import json
import cv2
from pyzbar.pyzbar import decode


def take_photo(filename='photo.jpg'):
   """Takes a photo using the default camera and saves it to the specified filename."""

   # Initialize the camera
   cap = cv2.VideoCapture(0)

   if not cap.isOpened():
       print("Error: Could not open camera.")
       return

   while True:   
   # Capture a frame
       ret, frame = cap.read()
       if not ret:
           print("Failed to capture frame")
           break
       cv2.imshow("test", frame)

   cap.release()
   cv2.destroyAllWindows()

def get_barcode():
    take_photo()
    img = cv2.imread("barcode_imgs/photo.png")
    barcode = ""
    for code in decode(img):
        barcode = code.data.decode("utf-8")
        print(code.type)
        print(code.data.decode("utf-8"))
    
    return barcode

def get_packaging_info():
    URL = "https://world.openfoodfacts.org/api/v0/product/" + get_barcode() + ".json"

    #make api request
    r = requests.get(url=URL)

    data = r.json()

    if data and 'product' in data:
        product = data['product']
        packaging = product.get('packaging', None)  # Safely get 'packaging'

        if packaging:
            print(packaging)
        else:
            print("packaging key not found.")
            print(None)
    else:
        print("product data not available.")
        print(None)


def main():
    get_packaging_info()

if __name__ == "__main__":
    main()
    #app.run(debug=True)


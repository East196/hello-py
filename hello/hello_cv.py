import cv2


import cv2
print cv2.__file__
from  SimpleCV import Image, Color, time

img = cv2.imread('watch.jpg', cv2.COLOR_GRAY2RGB)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

car_in_lot = Image("parking-car.png")
car_not_in_lot = Image("parking-no-car.png")

car = car_in_lot.crop(470, 200, 200, 200)
car.show()

yellow_car = car.colorDistance(Color.YELLOW)
yellow_car.show()

only_car = car - yellow_car
only_car.show()

time.sleep(2)

car_not_in_lot = Image("parking-no-car.png")
no_car = car_not_in_lot.crop(470,200,200,200)

yellow_car = car.colorDistance(Color.YELLOW)
yellow_car.show()

time.sleep(2)

only_car = car - yellow_car
print only_car.meanColor()

import cv2

def play():
    # image = self.driver.get_screenshot_as_png()
    # data = np.fromstring(image, dtype=np.uint8)
    # image = cv2.imdecode(data, 1)
    image = cv2.imread("Testcases/green2.png")
    cv2.imshow("wi", image)
    cv2.waitKey(0)
    
play()
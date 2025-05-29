def resize_image(image, width, height):
    import cv2
    return cv2.resize(image, (width, height))

def convert_color_space(image, color_space):
    import cv2
    if color_space == 'gray':
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif color_space == 'hsv':
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return image

def apply_gaussian_blur(image, kernel_size=(5, 5)):
    import cv2
    return cv2.GaussianBlur(image, kernel_size, 0)

def threshold_image(image, threshold_value=127):
    import cv2
    _, thresh_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresh_image
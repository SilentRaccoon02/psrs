import cv2
import numpy as np


def save_and_show(name, image):
    cv2.imwrite(f"{name}.jpg", image)
    cv2.imshow(name, image)
    cv2.waitKey()


def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    kernel_size = int(np.sum(image.shape) / 80)
    eroded = cv2.erode(binary, np.ones((kernel_size, kernel_size)))
    gradient = cv2.morphologyEx(eroded, cv2.MORPH_GRADIENT, np.ones((2, 2)))

    return gradient


def find_angle(image):
    lines = cv2.HoughLines(image, 1, np.pi / 180, 100)

    if lines is None:
        return None, None

    thetas = np.sort(lines[:, 0, 1])
    middle = int((len(lines) / 2))
    angle = np.rad2deg(thetas[middle]) - 90

    return angle, lines


def display_lines(image, lines):
    lined = image.copy()

    for line in lines:
        rho = line[0][0]
        theta = line[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv2.line(lined, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

    return lined


def rotate_image(image, angle):
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)

    abs_cos = abs(rotation_matrix[0, 0])
    abs_sin = abs(rotation_matrix[0, 1])

    bound_width = int(height * abs_sin + width * abs_cos)
    bound_height = int(height * abs_cos + width * abs_sin)

    rotation_matrix[0, 2] += bound_width / 2 - image_center[0]
    rotation_matrix[1, 2] += bound_height / 2 - image_center[1]

    return cv2.warpAffine(image, rotation_matrix, (bound_width, bound_height))


def main():
    source = cv2.imread("source.jpg", cv2.IMREAD_COLOR)
    preprocessed = preprocess_image(source)
    save_and_show("preprocessed", preprocessed)

    angle, lines = find_angle(preprocessed)

    if angle is None:
        return

    print(f"angle = {angle:.2f}")
    lined = display_lines(source, lines)
    save_and_show("lined", lined)

    result = rotate_image(source, angle)
    save_and_show("result", result)


if __name__ == "__main__":
    main()

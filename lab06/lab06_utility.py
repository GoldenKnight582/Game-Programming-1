# Tyler Cobb
# ETGG1801-05 Lab 6

import math
import pygame
import random

# Functions


def get_relative_point(origin_x, origin_y, radians, hypotenuse, y_invert=True, int_conversion=True):
    """
    Find point (px, py) relative to a chosen point.
    :param origin_x: x-value of initial point
    :param origin_y: y-value of initial point
    :param radians: angle of the line between the initial point and second point
    :param hypotenuse: distance between the initial point and second point
    :param y_invert: boolean for whether the second point is above or below the initial point
    :param int_conversion: boolean for whether values should be converted to integers
    :return:
    """
    # Then second point is above initial point
    # Find the second point by taking the input of radians and hypotenuse and calculating the x and y distances
    opposite = math.sin(radians) * hypotenuse
    adjacent = math.cos(radians) * hypotenuse
    px = origin_x + adjacent
    if y_invert:
        py = origin_y - opposite
    else:
        py = origin_y + opposite
    if int_conversion:
        px = int(px)
        py = int(py)
        return px, py
    else:
        return px, py


def get_point(num_points, center_x, center_y, size, rotation, point_index):
    """
    Find a point in the shape
    :param num_points: the number of points in the shape
    :param center_x: x-value at the center of the shape
    :param center_y: y-value at the center of the shape
    :param size: size of the shape (Distance from center to corner point)
    :param rotation: rotation of the shape
    :param point_index:
    :return:
    """
    anglePoly = math.radians((360 / num_points) * point_index) + math.radians(rotation)
    px, py = get_relative_point(center_x, center_y, anglePoly, size)
    point = (px, py)
    return point


def draw_shape(num_points, center_x, center_y, size, rotation, surf, highlighted=False):
    """
    Use get_points to calculate the points in the shape, and draw it to the screen
    :param num_points: the number of points in the shape
    :param center_x: x-value at the center of the shape
    :param center_y: y-value at the center of the shape
    :param size: size of the shape (Distance from center to corner point)
    :param rotation: rotation of the shape
    :param surf: the surface that is being drawn to
    :param highlighted: boolean for whether the color should change
    :return:
    """
    line_counter = num_points
    x = 0
    point = get_point(num_points, center_x, center_y, size, rotation, x)
    x = 1
    while line_counter > 0:
        new_point = get_point(num_points, center_x, center_y, size, rotation, x)
        x += 1
        if not highlighted:
            pygame.draw.line(surf, (255, 255, 255), point, new_point, 1)
            pygame.draw.circle(surf, (255, 0, 0), point, 5)
            pygame.draw.circle(surf, (255, 0, 0), new_point, 5)
        else:
            pygame.draw.line(surf, (120, 255, 120), point, new_point, 1)
            pygame.draw.circle(surf, (0, 255, 0), point, 5)
            pygame.draw.circle(surf, (0, 255, 0), new_point, 5)
        line_counter -= 1
        point = new_point
    pygame.display.flip()


def create_shape(win_width, win_height):
    """
    Creates a randomly placed shape with a random (3-10) number of points with random rotation
    :param win_width:
    :param win_height:
    :return:
    """
    size = random.randint(40, 240)
    num_points = random.randint(3, 10)
    center_x = random.randint(0, win_width)
    if center_x > win_width - size:
        center_x = win_width - size
    elif center_x < size:
        center_x = size
    center_y = random.randint(0, win_height)
    if center_y > win_height - size:
        center_y = win_height - size
    elif center_y < size:
        center_y = size
    rotation = random.randint(0, 360)   # degrees
    return size, num_points, center_x, center_y, rotation


def determine_side(ax, ay, bx, by, px, py):
    """
    Determines if the point (px, py) is to the left of the line between (ax, ay) and (bx, by)
    :param ax: x-value of one corner point in the shape (starting point)
    :param ay: y-value of same corner point in the shape (starting point)
    :param bx: x-value of another corner point in the shape
    :param by: y-value of same point
    :param px: x-value of point within the window
    :param py: y-value of same point
    :return:
    """
    side_x = bx - ax
    side_y = by - ay
    to_point_x = px - ax
    to_point_y = py - ay
    if (side_x * to_point_y) - (side_y * to_point_x) > 0:
        side_result = True
    else:
        side_result = False
    return side_result


def inside(num_points, center_x, center_y, size, rotation, point_x, point_y):
    """
    Determines if the point (point_x, point_y) is inside the shape
    :param num_points: the number of points in the shape
    :param center_x: x-value at the center of the shape
    :param center_y: y-value at the center of the shape
    :param size: size of the shape (Distance from center to corner point)
    :param rotation: rotation of the shape
    :param point_x: x-value of a point
    :param point_y: y-value of same point
    :return:
    """
    vector_count = num_points
    answer_count = 0
    x = 0
    ax, ay = get_point(num_points, center_x, center_y, size, rotation, x)
    x = 1
    while vector_count > 0:
        bx, by = get_point(num_points, center_x, center_y, size, rotation, x)
        side_result = determine_side(ax, ay, bx, by, point_x, point_y)
        if side_result:
            answer_count += 1
        else:
            answer_count -= 1
        x += 1
        vector_count -= 1
        ax, ay = bx, by
    if answer_count == num_points:
        is_inside = True
    elif answer_count == -num_points:
        is_inside = True
    else:
        is_inside = False
    return is_inside

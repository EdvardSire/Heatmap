import os
from sys import maxsize
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageChops


def get_all_pixels(coordinates):
    """Get all pixel coordinates, given the top left and bottom right."""
    pixels = []
    x1, y1 = coordinates[0]
    x2, y2 = coordinates[1]
    for ix in range(x1, x2 + 1):
        for iy in range(y1, y2 + 1):
            pixels.append((ix, iy))
    return pixels


def get_coords(char):
    """Get the coordinate of a key from the key map."""
    left_shift = [
        (15, 1), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7),
        (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7)
    ]
    for key in (item for item in keys if char in item):
        pixels = get_all_pixels(char_map[key])
        if key.index(char) == 1:
            pixels += left_shift
        return pixels


def get_frequencies(filename):
    """Get the frequencies of certain keypresses."""
    print(f'Processing file {filename}...')
    pixels = []
    heatmap_data = np.asarray([[0] * 57] * 21)
    # Open the given file and read the contents
    with open(filename) as file:
        contents = file.read()
    # Get the pixels covered by each character, and append these to pixels
    for char in contents:
        coords = get_coords(char)
        if coords:
            for coord in coords:
                pixels.append(coord)
    # Increment the appropriate coordinate for each pixel covered
    for coordinate in pixels:
        x, y = coordinate
        heatmap_data[x][y] += 1
    # Get the sum of all data, and divide all values by that sum
    total = np.sum(heatmap_data)
    heatmap_data = heatmap_data / total
    # Get the values for the shift key, and scale them down by 70%
    for pixel in get_all_pixels(((18, 18), (19, 34))):
        x, y = pixel
        heatmap_data[x][y] *= 0.3
    print(f'Finished processing file {filename}.')

    return heatmap_data


def blend_and_save(heatmap_data, output_image, colormap, dots):
    """Plot a heatmap, upscale it to the keyboard and save a blended image."""
    print('Generating heatmap...')
    heatmap_path = './images/heatmap.png'
    keyboard = Image.open("./images/keyboard.png")

    # Clear the heatmap plot and axes
    plt.clf()
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.imshow(
        heatmap_data, interpolation='lanczos', zorder=1, cmap=colormap
    )

    plt.savefig(
        heatmap_path,
        dpi=dots,
        pad_inches=0,
        transparent=True,
        bbox_inches='tight'
    )
    print('Blending and saving image...')

    # Resize the heatmap to the keyboard's size, with antialiasing
    heatmap = Image.open(heatmap_path)
    heatmap = heatmap.resize(keyboard.size, Image.LANCZOS)
    heatmap.save(heatmap_path)

    # Blend the images, and save
    blended = ImageChops.darker(keyboard, heatmap)
    blended.save(output_image)

char_map = {
    ' ': ((18, 18), (19, 34)),
    '\t': ((8, 1), (9, 4)),
    '`¬': ((4, 1), (5, 2)),
    '1!': ((4, 5), (5, 6)),
    '2@': ((4, 9), (5, 10)),
    '3#': ((4, 13), (5, 14)),
    '4$': ((4, 17), (5, 18)),
    '5%': ((4, 20), (5, 21)),
    '6^': ((4, 24), (5, 25)),
    '7&': ((4, 28), (5, 29)),
    '8*': ((4, 32), (5, 33)),
    '9(': ((4, 36), (5, 37)),
    '0)': ((4, 40), (5, 41)),
    '-_': ((4, 44), (5, 45)),
    '=+': ((4, 48), (5, 49)),
    'qQ': ((8, 7), (9, 8)),
    'wW': ((8, 11), (9, 12)),
    'eE': ((8, 15), (9, 16)),
    'rR': ((8, 19), (9, 20)),
    'tT': ((8, 22), (9, 23)),
    'yY': ((8, 26), (9, 27)),
    'uU': ((8, 30), (9, 31)),
    'iI': ((8, 34), (9, 35)),
    'oO': ((8, 38), (9, 39)),
    'pP': ((8, 42), (9, 43)),
    '[{': ((8, 46), (9, 47)),
    ']}': ((8, 50), (9, 51)),
    '\\|': ((8, 54), (9, 55)),
    'aA': ((11, 8), (12, 9)),
    'sS': ((11, 12), (12, 13)),
    'dD': ((11, 16), (12, 17)),
    'fF': ((11, 20), (12, 21)),
    'gG': ((11, 23), (12, 24)),
    'hH': ((11, 27), (12, 28)),
    'jJ': ((11, 31), (12, 32)),
    'kK': ((11, 35), (12, 36)),
    'lL': ((11, 39), (12, 40)),
    ';:': ((11, 43), (12, 44)),
    'zZ': ((15, 10), (16, 11)),
    'xX': ((15, 14), (16, 15)),
    'cC': ((15, 18), (16, 19)),
    'vV': ((15, 22), (16, 23)),
    'bB': ((15, 25), (16, 26)),
    'nN': ((15, 29), (16, 30)),
    'mM': ((15, 33), (16, 34)),
    ',<': ((15, 37), (16, 38)),
    '.>': ((15, 41), (16, 42)),
    '/?': ((15, 45), (16, 46)),
    '\n': ((11, 51), (12, 55)),
    '\'"': ((11, 47), (12, 48))
}


if __name__ == '__main__':
    colormap = 'viridis'
    keys = char_map.keys()
    dpi = 600
    input = "file.txt"
    output_image= "./images/output.png"
    blend_and_save(
        get_frequencies(input), output_image, colormap, dpi
    )
    print(f'Image generated: {output_image}')


from PIL import Image

def split_grid_from_image(img, rows, cols):
    w, h = img.size

    piece_w = w // cols
    piece_h = h // rows

    images = []

    for i in range(rows):
        for j in range(cols):
            crop = img.crop((
                j * piece_w,
                i * piece_h,
                (j + 1) * piece_w,
                (i + 1) * piece_h
            ))
            images.append(crop)

    return images
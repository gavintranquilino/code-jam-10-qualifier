from PIL import Image
import numpy as np

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """

    image_w, image_h = image_size
    tile_w, tile_h = tile_size
    num_tiles_h = image_w // tile_w
    num_tiles_v = image_h // tile_h
    num_tiles = num_tiles_h * num_tiles_v

    # Check if tile size and image sizes are divisible
    if image_w % tile_w == 0 and image_h % tile_h == 0:
        used_tiles = set()
        for i in ordering:
            if i in used_tiles or i >= num_tiles:
                return False
            used_tiles.add(i)
    
    else:
        return False

    return True

def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """

    input_image = Image.open(image_path)
    tile_w, tile_h = tile_size
    image_w, image_h = input_image.size

    if not valid_input((image_w, image_h), tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

    num_tiles_h = image_w // tile_w
    num_tiles_w = image_h // tile_h
    num_tiles = num_tiles_h * num_tiles_w

    # Create empty canvas
    color_mode = input_image.mode
    new_image = Image.new(color_mode, (image_w, image_h))

    # Load image as numpy array
    input_array = np.array(input_image)

    for index, tile_index in enumerate(ordering):
        # Calculate row and column for the og file
        src_row = tile_index // num_tiles_h
        src_col = tile_index % num_tiles_h

        # Calculate coords in og image
        src_x1 = src_col * tile_w
        src_y1 = src_row * tile_h
        src_x2 = src_x1 + tile_w
        src_y2 = src_y1 + tile_h

        # Extract tile from array w numpy slicing
        tile = input_array[src_y1:src_y2, src_x1:src_x2]

        # Calculate row and column for new image
        dest_row = index // num_tiles_h
        dest_col = index % num_tiles_h

        # Calculate coords in new image
        dest_x1 = dest_col * tile_w
        dest_y1 = dest_row * tile_h
        dest_x2 = dest_x1 + tile_w
        dest_y2 = dest_y1 + tile_h

        # Paste the tile onto new image w Pillow
        new_image.paste(Image.fromarray(tile), (dest_x1, dest_y1, dest_x2, dest_y2))

    new_image.save(out_path)
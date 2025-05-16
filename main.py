from PIL import Image
import os

def load_and_resize_png():
    file_path = input("Enter the path to your source .png file: ").strip()
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: {file_path}")
    if not file_path.lower().endswith(".png"):
        raise ValueError("That doesn't look like a .png file.")
    img = Image.open(file_path).convert("RGBA")
    target_size = (72, 24)
    if img.size != target_size:
        img = img.resize(target_size, Image.Resampling.NEAREST)
    return img

def split_into_tiles(img, tile_size=(8, 8)):
    tile_w, tile_h = tile_size
    img_w, img_h = img.size

    cols = img_w // tile_w
    rows = img_h // tile_h

    tiles = []
    # row index 0 is top, so bottom row is rows-1
    for row in range(rows-1, -1, -1):        # bottom -> top
        for col in range(cols-1, -1, -1):    # right -> left
            left = col * tile_w
            upper = row * tile_h
            box = (left, upper, left + tile_w, upper + tile_h)
            tile = img.crop(box)
            tiles.append(tile)
    return tiles


if __name__ == "__main__":
    skin_path = "skin.png"
    if not os.path.isfile(skin_path):
        raise FileNotFoundError(f"Cannot find base skin: {skin_path}")
    base_skin = Image.open(skin_path).convert("RGBA")

    img = load_and_resize_png()
    tiles = split_into_tiles(img, (8, 8))
    print(f"Generated {len(tiles)} tiles.")

    # create an output directory
    out_dir = "skins"
    os.makedirs(out_dir, exist_ok=True)
    for idx, tile in enumerate(tiles, start=1):
        skin_copy = base_skin.copy()
        skin_copy.paste(tile, (8, 8))
        out_path = os.path.join(out_dir, f"skin_{idx:02d}.png")
        skin_copy.save(out_path)



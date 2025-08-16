import os

from PIL import Image, ImageFilter, ImageOps


# Image opening function
def open_img(imgPath: str) -> Image.Image | None:
    """Opens image from a given path

    Args:
        imgPath (str): Path of an image file

    Returns:
        Image or None: Returns image on success, else returns none on failure
    """
    try:
        return Image.open(imgPath).copy()
    except FileNotFoundError:
        print(f"Error: Image does not exist in {imgPath}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_img(img: Image.Image, savePath: str) -> None:
    """Save the image after modifications are made

    Args:
        im (Image): Image to be saved
        savePath (str): Path for the image to be saved to

    Returns:
        str: Returns an error if saving succeeds or fails
    """
    try:
        file_ext = os.path.splitext(savePath)[1].lower()
        if file_ext == ".jpg" or file_ext == ".jpeg":
            img.save(savePath, format="JPEG", quality=90)
        else:
            img.save(savePath)
    except Exception as e:
        print(f"Error saving image to {savePath}: {e}")


def rotate_img(img: Image.Image) -> Image.Image:
    """Rotates an image 90 degrees

    Args:
        img (Image.Image): The image to be rotated

    Returns:
        Image.Image: The rotated image
    """
    return img.rotate(90)


def resize_img(img: Image.Image, width: int, height: int) -> Image.Image:
    """Resizes a given image by width and height

    Args:
        img (Image.Image): The image to be resized
        width (int): Width to resize to (in pixels)
        height (int): Height to resize to (in pixels)

    Returns:
        Image.Image: Resized image
    """
    return img.resize((width, height), resample=5)


def apply_effect(img: Image.Image, effect: str) -> Image.Image | ValueError:
    """Applies a given effect to an image.

    Args:
        img (Image.Image): Image to apply effect to
        effect (str): Type of effect to apply to the image

    Returns:
        Image.Image | ValueError: Effected image
    """
    if effect == "blur":
        return img.filter(ImageFilter.BLUR)
    elif effect == "contour":
        return img.filter(ImageFilter.CONTOUR)
    elif effect == "detail":
        return img.filter(ImageFilter.DETAIL)
    elif effect == "edge enhance":
        return img.filter(ImageFilter.EDGE_ENHANCE)
    elif effect == "emboss":
        return img.filter(ImageFilter.EMBOSS)
    elif effect == "find edges":
        return img.filter(ImageFilter.FIND_EDGES)
    elif effect == "sharpen":
        return img.filter(ImageFilter.SHARPEN)
    elif effect == "smooth":
        return img.filter(ImageFilter.SMOOTH)
    else:
        return ValueError("Error: Filter not available")


def flip_image(img: Image.Image) -> Image.Image:
    """Flips an image from top to bottom

    Args:
        img (Image.Image): Image to be flipped

    Returns:
        Image.Image: Flipped image
    """
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def mirror_image(img: Image.Image) -> Image.Image:
    """Mirrors image from left to right

    Args:
        img (Image.Image): Image to mirror

    Returns:
        Image.Image: Mirrored image
    """
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def grayscale_image(img: Image.Image) -> Image.Image:
    """Applies a grayscale filter to the image

    Args:
        img (Image.Image): Image to apply grayscale to

    Returns:
        Image.Image: Grayscaled image
    """
    return ImageOps.grayscale(img)

def invert_image(img: Image.Image) -> Image.Image:
    """Applies an inverted filter to the image

    Args:
        img (Image.Image): Image to apply invert to

    Returns:
        Image.Image: Inverted image
    """
    return ImageOps.invert(img)

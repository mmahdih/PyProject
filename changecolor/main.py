import os

from PIL import Image


def changeColor(image_path):
    # Load the black icon
    image = Image.open(image_path)

    # Convert the image to RGBA (if not already in RGBA)
    image = image.convert("RGBA")

    # Get the data of the image
    data = image.getdata()

    # Create a new list to store the modified pixel values
    new_data = []

    # Iterate through each pixel
    for item in data:
        # If the pixel is black (0, 0, 0), change it to white (255, 255, 255)
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((255, 255, 255, item[3]))  # Keep the alpha value (transparency)
        else:
            # Keep non-black pixels unchanged
            new_data.append(item)

    # Update the image with the new data
    image.putdata(new_data)


    # Save or show the modified image
    image.save(f"{image_path}_white.png")
    # image.show()

png_list = os.listdir()

for images in png_list:
    if images.endswith(".png"):
        changeColor(images)

print(png_list)


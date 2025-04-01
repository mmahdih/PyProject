from PIL import Image
import numpy as np
import os


dir = os.listdir("images")
print(dir)

# os.mkdir("images\\white")


for file in dir:
	im = Image.open(f"images\\{file}")
	im = im.convert('RGBA')

	data = np.array(im)  # "data" is a height x width x 4 numpy array
	red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

	# Replace white with red... (leaves alpha values alone...)
	white_areas = (red == 0) & (blue == 0) & (green == 0)
	data[..., :-1][white_areas.T] = (255, 255, 255)  # Transpose back needed

	im2 = Image.fromarray(data)
	# im2.show()
	im2.save(f'images\\white\\{file}')

#
#

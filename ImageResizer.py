# Image Re-sizer application
# Written by AN on 2022-01-28
# Part of capstone effort from Udemy Intro to python course
# Uses Pillow library to manipulate photos, not doing anything very smart
# Allows image scaling, crop, and rotate

# note need to install pillow library to use this. Type "pip install pillow"
# if not done already

import os
from PIL import Image, ImageOps

def crop_image(path):

	# loads image, queries user on crop parameters and returns cropped image
	image = Image.open(path)
	print(f"Image has pixel size {image.size} ")
	print("Enter start and end coordinates as per example: 20, 50, 1020, 865")
	print("First two coords are x, y of top left corner")
	print("Last two coords are x, y of the bottom right corner")
	# (x, y, width, height)
	while True:
		try:
			data = list(map(int,input("Enter here: ").split(", ")))
		except:
			print("Error: enter data as 'x1, y1, x2, y2'. Try again...")
		else:
			break

	width = data[2]-data[0]
	height = data[3] - data[1]

	new_image = image.crop((data[0],data[1],width,height))

	return new_image

def resize_image(path):
	# loads image, queries user on scaling parameters and returns scaled image
	image = Image.open(path)
	print(f"Image has pixel size {image.size} ")
	answer = ""
	while answer not in ["Y","N"]:
		answer = input("Keep current aspect ratio? (Y/N)").upper()

	if answer == "Y":
		ratio = 0
		while ratio < 0.01 or ratio > 20:
			ratio = float(input("Enter the desired scaling factor between 0.01 and 20.0 \n"
						  "(Example: to make img half as wide and tall use 0.50): "))

		h, w = image.size

		new_h = int(h*ratio)
		new_w = int(w*ratio)

	else:
		new_h = 0
		while new_h < 1 or new_h > 1000000:
			new_h = int(input("Enter your desired height (min 1 and max 1E6): "))

		new_w = 0
		while new_w < 1 or new_w > 1000000:
			new_w = int(input("Enter your desired width (min 1 and max 1E6): "))

	new_image = image.resize((new_h,new_w))
	return new_image


def rotate_image(path):
	# loads image, queries user on rotate parameter and returns rotated image
	image = Image.open(path)
	print("Enter a number of degrees to rotate image. (0-360)")

	degrees = -1
	while degrees < 0 or degrees > 360:
		try:
			degrees = int(input("Enter here: "))
		except:
			print("Enter number of degrees between 0 and 360. Try again...")
		else:
			break

	new_image = image.rotate(degrees, expand = True)
	return new_image


def get_path():
	# Queries user on path of image, checks that this is valid
	successful_execution = True
	answer = ""
	while answer not in ["Y","N"]:
		answer = input("Is the image in the same folder as this program? (Y/N)").upper()

	if answer == "N":
		print(f"For reference, current path is: {os.getcwd()+'/'}")
		full_path = input("Please enter full path of image file including filename and extension: ")

	else:
		image_filename = input("Please enter image filename including extension: ")
		folder_path = os.getcwd()+'/'
		full_path = folder_path + image_filename

	file_exists = os.path.isfile(full_path)

	if file_exists == False:
		print(f"File at {full_path} does not exist. Please try again.")
		successful_execution = False

	return full_path, successful_execution

def myfunc():
	# Main script. Collects info, mods image, and provides option to save it
	# Opening information
	print("\n \n----------------- \n \nWelcome to ImageResizer!")
	print("This program can resize and perform other mods on your image file.")

	# Get image path and name
	full_path, success = get_path()
	if success == False:
		quit()
	
	# get folder path and filename from full path
	folder_path = full_path[:len(full_path)-full_path[::-1].find("/")]
	image_filename = full_path[len(full_path)-full_path[::-1].find("/")::]

	# Ask which function they want (crop, resize, rotate, make transparent)
	answer = ""
	while answer not in ["crop","resize","rotate"]:
		answer = input("Which operation do you want to do? (crop, resize, rotate) ").lower()

	# Do it
	if answer == "crop":
		new_image = crop_image(full_path)
	elif answer == "resize":
		new_image = resize_image(full_path)
	elif answer == "rotate":
		new_image = rotate_image(full_path)

	# Show user and ask if they want to save it, and get new filename
	new_image.show()

	answer = ""
	while answer not in ["Y","N"]:
		answer = input("Want to save image? (Y/N): ")

	if answer == "Y":
		new_filename = input("New file will be in same folder as old one. \n"
						 "Please enter new filename including extension: ")
		new_path = folder_path + new_filename
		new_image = ImageOps.exif_transpose(new_image)
		new_image.save(new_path)
		print("Thanks for using ImageResizer!")
	else:
		print("Thank you!")

	# End

if __name__ == "__main__":
	myfunc()

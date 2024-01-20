#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 02:23:23 2024

@author: kaanuslu
"""


import ecc
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.image as ImageMatplot
import tqdm
from tqdm.gui import tqdm_gui
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
from threading import Thread





#ecc parameters
finalpoints, p, a, b, order, generator = ecc.curveGenerator()
# Assign public and secret key
publicKey, secretKey = ecc.keyGenerator(a, b, p, order, generator)
# pixel to point and point to pixel dictionaries
pixelToPoint = {}
pointToPixel = {}
generatorLookup = {}
# images length width height
length, width, height = 0,0,0
oneDShape = 0

def download_display_latex():
    baseURL = "https://latex.codecogs.com/png.image?"
    baseURL += "\\bg_white "
    
    #elliptic curve equation
    endPoint = "y^2 = x^3 + {}x + {}".format(a,b)
    endPoint += " \\"
    endPoint += "\\"
    
    #finite field
    endPoint += " \mathbb{}_{{{}}}".format("{F}",p)
    endPoint += " \\"
    endPoint += "\\"
    
    #generator point
    endPoint += " generator = {}".format(str(generator))
    endPoint += " \\"
    endPoint += "\\"
    
    #order
    endPoint += " order = {}".format(str(order))
    endPoint += " \\"
    endPoint += "\\"
    
    endPoint2 = endPoint
    
    #public key
    endPoint += " \\textit{} {}".format("{public key is }",str(publicKey))
    
    #secretKey
    endPoint2 += " \\textit{} {}".format("{secret key is }",str(secretKey))


    
    url = baseURL + endPoint
    print(url)
    
    file_path = "latex_encrypt.png"
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open file in binary write mode and save the content
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image. Status code:", response.status_code)
    
    # Get the path from the text entry widget
    image_path = file_path
    
    # Load the image
    image = Image.open(image_path)
    
    # Resize the image to fit the display area
    image.thumbnail((250, 250))
    
    # Convert the image to PhotoImage format
    photo = ImageTk.PhotoImage(image)
    
    # Display the image
    latex_label_encrypt.config(image=photo)
    latex_label_encrypt.image = photo  # Keep a reference to avoid garbage collection
    
    
    
    url = baseURL + endPoint2
    print(url)
    
    file_path = "latex_decrypt.png"
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open file in binary write mode and save the content
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image. Status code:", response.status_code)
    
    # Get the path from the text entry widget
    image_path = file_path
    
    # Load the image
    image = Image.open(image_path)
    
    # Resize the image to fit the display area
    image.thumbnail((250, 250))
    
    # Convert the image to PhotoImage format
    photo = ImageTk.PhotoImage(image)
    
    # Display the image
    latex_label_decrypt.config(image=photo)
    latex_label_decrypt.image = photo  # Keep a reference to avoid garbage collection



def generate_curve_and_display():
    # Call your ECC curve generator function
    global finalpoints, p, a, b, order, generator, pixelToPoint, pointToPixel, generatorLookup
    finalpoints, p, a, b, order, generator = ecc.curveGenerator()
    
    pixelToPoint = {}
    pointToPixel = {}
    for i in range (0,len(finalpoints)):
        pixelToPoint[i]=finalpoints[i]
        pointToPixel[finalpoints[i]]=i
        
    generatorLookup = {}
    for i in range(order):
        generator_x, generator_y = ecc.pointMultiplication(generator[0],generator[1],a,b,p,i)
        generatorLookup[i] = (generator_x,generator_y)
        



    
    get_publicKey_and_secretKey()
    
    download_display_latex()

    
def get_publicKey_and_secretKey():
    global publicKey, secretKey
    # Assign public and secret key
    publicKey, secretKey = ecc.keyGenerator(a, b, p, order, generator)
    


def load_and_display_image():
    # Get the path from the text entry widget
    image_path = path_entry_encrypt.get()
    
    # Load the image
    image = Image.open(image_path)
    
    # Resize the image to fit the display area
    image.thumbnail((250, 250))
    
    # Convert the image to PhotoImage format
    photo = ImageTk.PhotoImage(image)
    
    # Display the image
    image_label_encrypt.config(image=photo)
    image_label_encrypt.image = photo  # Keep a reference to avoid garbage collection
    

def imageToArray(image):
    img=ImageMatplot.imread(image)
    img=img.reshape(-1,)
    return img

def arrayToImage(array,l,w,h):
    newimg=array.reshape(l,w,h)
    return newimg


def encrypt_image():
    global pixelToPoint, pointToPixel, generatorLookup, length, width, height, oneDShape
    image_path = path_entry_encrypt.get()
    print(image_path)
    img1D= imageToArray(image_path)
    print(img1D)
    img3D=ImageMatplot.imread(image_path)
    length,width,height=img3D.shape

    #newimg1D=[]
    oneDShape = img1D.shape[0]
    
    encryptedImage = []
    encryptedImagePixels = []
    
    for i in tqdm.tqdm(range (0, oneDShape)):
        pixel=img1D[i]

        px, py = publicKey
        
        c1, c2 = ecc.encrypt(pixel,a,b,p,order,generator,px,py,pixelToPoint,generatorLookup)
        encryptedImage.append((c1,c2))
        
        encryptedImagePixels.append(pointToPixel[c1])
        
    with open('encrypted_data.txt', 'w') as file:
    # Writing each item on a new line
        for item in encryptedImage:
            file.write(f"{item}\n")
    
    encryptedImagePixels=np.array(encryptedImagePixels)
    newimg3D=arrayToImage(encryptedImagePixels,length,width,height)
    plt.title("Encrypted image")
    plt.imshow(newimg3D)
    plt.axis('off')  # Optional: Turn off the axis
    plt.savefig('encrypted_image.png', bbox_inches='tight', pad_inches=0)
    plt.close()  # Close the plot to prevent it from showing in another interface

    # Get the path from the text entry widget
    image_path = 'encrypted_image.png'
        
    # Load the image
    image = Image.open(image_path)
        
    # Resize the image to fit the display area
    image.thumbnail((250, 250))
        
    # Convert the image to PhotoImage format
    photo = ImageTk.PhotoImage(image)
        
    # Display the image
    encrypted_image_label_encrypt.config(image=photo)
    encrypted_image_label_encrypt.image = photo  # Keep a reference to avoid garbage collection

    
    

def show_decrypted_image():
    # Get the path from the text entry widget
    image_path = 'decrypted_image.png'
    
    # Load the image
    image = Image.open(image_path)
    
    # Resize the image to fit the display area
    image.thumbnail((250, 250))
    
    # Convert the image to PhotoImage format
    photo = ImageTk.PhotoImage(image)
    
    # Display the image
    image_label_decrypt.config(image=photo)
    image_label_decrypt.image = photo  # Keep a reference to avoid garbage collection
    
def decrypt_image():
    global pixelToPoint, pointToPixel, generatorLookup, length, width, height, oneDShape
    cipher_path = path_entry_decrypt.get()
    cipher_path = 'encrypted_data.txt'
    print(cipher_path)
    
    encryptedImage = []

    with open(cipher_path, 'r') as file:
        # Read each line in the file
        for line in file:
            # Strip newline characters and any surrounding whitespace
            line = line.strip()
    
            # Convert the string to a tuple of tuples using eval (be cautious with eval)
            tuple_data = eval(line)
    
            # Append the tuple to the list
            encryptedImage.append(tuple_data)
    
    #print(encryptedImage[-1])
    newimg1D=[]
    for i in tqdm.tqdm(range (0, oneDShape)):
        c1, c2 = encryptedImage[i]

        nx = secretKey
        

        decryptedPixel = ecc.decrypt(c1,c2 ,p,a,b,order,nx, pointToPixel)
        newimg1D.append(decryptedPixel)
        
    newimg1D=np.array(newimg1D)
    newimg3D=arrayToImage(newimg1D,length,width,height)
    plt.title("Decrypted image")
    plt.imshow(newimg3D)
    plt.axis('off')  # Optional: Turn off the axis
    plt.savefig('decrypted_image.png', bbox_inches='tight', pad_inches=0)
    plt.close()  # Close the plot to prevent it from showing in another interface
    #print(newimg1D)
    show_decrypted_image()
    
    
    

    

def browse_file_encrypt():
    filename = filedialog.askopenfilename()
    path_entry_encrypt.delete(0, tk.END)  # Clear the current text
    path_entry_encrypt.insert(0, filename)  # Insert the selected file path
    
    
def browse_file_decrypt():
    filename = filedialog.askopenfilename()
    path_entry_decrypt.delete(0, tk.END)  # Clear the current text
    path_entry_decrypt.insert(0, filename)  # Insert the selected file path







# Create the main window
root = tk.Tk()
root.configure(bg='blue')
root.title("Image Encryption Application")

notebook = ttk.Notebook(root)

# Create two frames, one for each tab
encrypt_tab = ttk.Frame(notebook)
decrypt_tab = ttk.Frame(notebook)

# Add tabs to the notebook with a name
notebook.add(encrypt_tab, text='Encrypt')
notebook.add(decrypt_tab, text='Decrypt')

# Place the notebook in the main window
notebook.pack(expand=True, fill='both')


# Create a button to generate and display curve parameters
generate_button_encrypt = ttk.Button(encrypt_tab, text="Generate ECC Curve", command=generate_curve_and_display)
generate_button_decrypt = ttk.Button(decrypt_tab, text="Generate ECC Curve", command=generate_curve_and_display)
generate_button_encrypt.pack()
generate_button_decrypt.pack()




# Create a label to display the image
latex_label_encrypt = ttk.Label(encrypt_tab)
latex_label_encrypt.pack()

# Create a label to display the image
latex_label_decrypt = ttk.Label(decrypt_tab)
latex_label_decrypt.pack()





## display first elliptic curve
generate_curve_and_display()

# Create a text entry widget for image path
path_entry_encrypt = ttk.Entry(encrypt_tab, width=50)
path_entry_encrypt.pack()

path_entry_decrypt = ttk.Entry(decrypt_tab, width=50)
path_entry_decrypt.pack()

# Create a browse button encrypt
browse_button_encrypt = ttk.Button(encrypt_tab, text="Browse", command=browse_file_encrypt)
browse_button_encrypt.pack()

# Create a browse button decrypt
browse_button_decrypt = ttk.Button(decrypt_tab, text="Browse", command=browse_file_decrypt)
browse_button_decrypt.pack()

# Create a button to load and display the image
load_button = ttk.Button(encrypt_tab, text="Load Image", command=load_and_display_image)
load_button.pack()

# Create a button to decrypt and display the image
encrypt_button = ttk.Button(encrypt_tab, text="Encrypt the Image", command=encrypt_image)
encrypt_button.pack()

#decrypt part
decrypt_button = ttk.Button(decrypt_tab, text="Decrypt the Image", command=decrypt_image)
decrypt_button.pack()

# Create a label to display the image
image_label_encrypt = ttk.Label(encrypt_tab)
image_label_encrypt.pack(side = "left")

encrypted_image_label_encrypt = ttk.Label(encrypt_tab)
encrypted_image_label_encrypt.pack(side = "left")

# Create a label to display the image
image_label_decrypt = ttk.Label(decrypt_tab)
image_label_decrypt.pack()






# Start the application's main loop
root.mainloop()

import cv2
import pytesseract
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import re
import os

# Get the current working directory
cwd = os.getcwd()

def sanitize_text(text):
    # Remove characters that are not allowed in worksheet names and cell values
    sanitized_text = re.sub(r'[\\/*?\[\]:;]', '', text)
    return sanitized_text

# Open file dialog to select the image
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])

# Read the image file
img = cv2.imread(file_path)

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply threshold to remove noise and make text clear
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Apply dilation to make text more visible
kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(thresh,kernel,iterations = 1)

# Extract text using Pytesseract
text = pytesseract.image_to_string(dilation)

# Clean text for excel use
cleaned_text = ''.join(e for e in text if e.isalnum() or e.isspace())
sanitized_text = sanitize_text(cleaned_text)

# Save sanitized text in Excel file
df = pd.DataFrame({'Note': [sanitized_text]})
df.to_excel('Note.xlsx', index=False)

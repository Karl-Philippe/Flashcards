import os
import re
import shutil
import cv2

# Path to the directory containing your original images
original_directory = r"data\Raw"

# Path to the directory where processed images will be saved
processed_directory = r"data\Processed"

# Create the processed directory if it doesn't exist
if not os.path.exists(processed_directory):
    os.makedirs(processed_directory)

# List all files in the original directory
files = os.listdir(original_directory)

# Function to extract numeric part from the filename
def extract_number(filename):
    return int(re.search(r'\d+', filename).group())

# Sort the files based on numeric and non-numeric parts using natural sorting
def natural_sort_key(filename):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', filename)]

files.sort(key=natural_sort_key)

# Iterate over the files in pairs
for i in range(0, len(files), 2):
    # Generate the new filenames
    recto_filename = f"{i//2 + 1}_recto.jpg"  # For the first image in the pair
    verso_filename = f"{i//2 + 1}_verso.jpg"  # For the second image in the pair
    
    # Copy the files to the processed directory
    shutil.copyfile(os.path.join(original_directory, files[i]), os.path.join(processed_directory, recto_filename))
    if i + 1 < len(files):  # Ensure there's a next file in the list
        shutil.copyfile(os.path.join(original_directory, files[i + 1]), os.path.join(processed_directory, verso_filename))



# List all files in the processed directory
files = os.listdir(processed_directory)

def sharpen_image(image):
    # Apply unsharp masking for sharpening
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    sharpened = cv2.addWeighted(image, 1.4, blurred, -0.5, 0)
    return sharpened

# Iterate over the files
for filename in files:
    # Load the image
    image = cv2.imread(os.path.join(processed_directory, filename))
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to segment the paper
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the contour with the maximum area (assuming it's the paper)
    max_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box of the contour
    x, y, w, h = cv2.boundingRect(max_contour)
    
    # Crop the image using the bounding box
    cropped_image = image[y:y+h, x:x+w]

    processed_image = sharpen_image(cropped_image)
    
    # Save the cropped image with the same filename
    cv2.imwrite(os.path.join(processed_directory, filename), processed_image)

import os
import sqlite3

def create_cards_table(conn):
    # Create a cursor object
    cursor = conn.cursor()
    
    # Create the 'cards' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cards (
                        id INTEGER PRIMARY KEY,
                        recto_image BLOB NOT NULL,
                        verso_image BLOB NOT NULL,
                        category TEXT,
                        label INTEGER CHECK (label >= 1 AND label <= 3)
                    )''')

def insert_card(conn, recto_image_data, verso_image_data, label, category):
    # Create a cursor object
    cursor = conn.cursor()

    # Insert data into the 'cards' table
    cursor.execute("INSERT INTO cards (recto_image, verso_image, label, category) VALUES (?, ?, ?, ?)", (recto_image_data, verso_image_data, label, category))

    # Commit changes
    conn.commit()

def main():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('cards.db')

    # Create the 'cards' table
    create_cards_table(conn)

    # Path to the directory containing the images
    directory = r'data\Processed'

    # List all directories in the directory
    categories = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]

    # Iterate through categories
    for category in categories:
        category_dir = os.path.join(directory, category)
        image_files = os.listdir(category_dir)
        # Sort the filenames based on card IDs
        image_files.sort(key=lambda x: int(x.split('_')[0]))

        # Iterate through the sorted filenames
        for filename in image_files:
            if filename.endswith("_recto.jpg"):
                card_id = filename.split('_')[0]
                recto_image_path = os.path.join(category_dir, filename)
                verso_image_path = os.path.join(category_dir, f"{card_id}_verso.jpg")
                
                # Read binary data of images
                with open(recto_image_path, 'rb') as f:
                    recto_image_data = f.read()
                with open(verso_image_path, 'rb') as f:
                    verso_image_data = f.read()

                # Insert data into the database
                label = 1  # Default label
                insert_card(conn, recto_image_data, verso_image_data, label, category)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()

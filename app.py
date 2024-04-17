import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import random
import io

class CardLabelerApp(tk.Tk):
    def __init__(self, db_path, labels):
        super().__init__()
        self.title("Card Labeler")
        self.configure(background='#DEE4E7')
        
        self.db_path = db_path
        self.labels = labels
        
        self.cards = self.load_cards()
        self.index_order = list(range(len(self.cards)))
        random.shuffle(self.index_order)
        self.current_index = 0
        self.side = 'recto'
        self.category = 'Anatomy'
        
        # Dictionary to store card labels
        self.card_labels = {}
        
        self.create_widgets()
        
    def load_cards(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT recto_image, verso_image, category, label FROM cards")
        cards = cursor.fetchall()
        conn.close()
        return cards
    
    def create_widgets(self):
       # Label to display card category
        self.category_text_var = tk.StringVar()
        self.category_display_label = tk.Label(self, textvariable=self.category_text_var, background='#DEE4E7', foreground='#000000', font=('Inter', 12))
        self.category_display_label.pack(pady=10)

        # Display the card image
        self.card_frame = tk.Frame(self, background='#DEE4E7')
        self.card_frame.pack(padx=20, pady=20)
        
        self.card_label = tk.Label(self.card_frame)
        self.card_label.pack()
        
        # Label to display current label
        self.label_text_var = tk.StringVar()
        self.label_display_label = tk.Label(self, textvariable=self.label_text_var, background='#DEE4E7', foreground='#000000', font=('Inter', 12))
        self.label_display_label.pack(pady=10)
        
        # Label instructions
        self.instructions_label = tk.Label(self, text="'Space bar' to switch sides, hit number key to apply label:\n (1) To be learned, (2) Partially learned, (3) Learned", background='#DEE4E7', foreground='#808080', font=('Inter', 10))
        self.instructions_label.pack(pady=10)
        
        # Initialize with the first card
        self.show_card()
        
        # Bind keyboard events
        self.bind("<Key>", self.key_pressed)
        
    def show_card(self):
        card_index = self.index_order[self.current_index]
        recto_image_data, verso_image_data, category, label_index = self.cards[card_index]

        # Check if the card has been labeled before
        card_number = card_index + 1
        label = self.labels[label_index - 1] if label_index else "Not labeled"
        if label:
            label_text = f"Card {card_number}: {label}"
        else:
            label_text = f"Card {card_number}: not labeled"

        # Check card category
        category_text = f"Category: {category}"

        # Determine which image to display based on the side
        if self.side == 'verso':
            card_image_data = verso_image_data
        else:
            card_image_data = recto_image_data

        card_image = Image.open(io.BytesIO(card_image_data))
        card_image.thumbnail((400, 400))  # Resize image if necessary
        self.card_photo = ImageTk.PhotoImage(card_image)

        # Display the card image
        self.card_label.configure(image=self.card_photo)
        self.card_label.image = self.card_photo

        # Display the label information
        self.label_text_var.set(label_text)

        # Display the category information
        self.category_text_var.set(category_text)


    def toggle_side(self):
        # Toggle between recto and verso sides of the card
        if self.side == 'recto':
            self.side = 'verso'
            print("verso")
        else:
            self.side = 'recto'
            print("recto")
        self.show_card()
        
    def label_card(self, label_index):
        label = self.labels[label_index]
        card_index = self.index_order[self.current_index]
        card_id = card_index + 1  # Calculate the card ID
        print(f"Card {card_id}: {label}")
        
        # Store the label for the current card
        self.card_labels[card_id] = label
        
        # Save label to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE cards SET label = ? WHERE id = ?", (label_index + 1, card_id))
        conn.commit()
        
        # Fetch updated card information from the database
        cursor.execute("SELECT recto_image, verso_image, category, label FROM cards WHERE id = ?", (card_id,))
        updated_card = cursor.fetchone()
        
        # Update the self.cards list with the updated card information
        self.cards[card_index] = updated_card
        
        conn.close()
        
        # Move to the next card
        self.current_index += 1
        self.side = 'recto'
        if self.current_index >= len(self.index_order):
            print("All the cards have been seen!")
            random.shuffle(self.index_order)
            self.current_index = 0
        self.show_card()

        
    def key_pressed(self, event):
        if event.char == ' ':
            self.toggle_side()
        elif event.char in ['1', '2', '3']:
            self.label_card(int(event.char) - 1)

# Example database path and labels
db_path = "cards.db"
labels = ["To be learned", "Partially learned", "Learned"]

# Create and run the application
app = CardLabelerApp(db_path, labels)
app.mainloop()

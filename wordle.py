import tkinter as tk
from tkinter import messagebox
import nltk
from nltk.corpus import words

nltk.download('words')  # Ensure the words corpus is downloaded

class WordleSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Solver")

        self.green_row = self.create_input_row("Green Letters:", row=0)
        self.yellow_row = self.create_input_row("Yellow Letters:", row=1)
        self.grey_row = self.create_input_row("Grey Letters:", row=2, num_boxes=12)

        self.submit_button = tk.Button(master, text="Submit", command=self.submit_feedback)
        self.submit_button.grid(row=3, column=0, columnspan=10, pady=10)

        self.english_words = set(words.words())
        self.candidate_words = [word.lower() for word in self.english_words if len(word) == 5]

    def create_input_row(self, label_text, row, num_boxes=5):
        label = tk.Label(self.master, text=label_text)
        label.grid(row=row, column=0, columnspan=2, sticky="w")

        entry_boxes = []
        for i in range(num_boxes):
            entry = tk.Entry(self.master, width=3, validate="key", validatecommand=(self.master.register(self.validate_entry), '%P'))
            entry.grid(row=row, column=i * 2 + 2)
            entry.bind('<KeyRelease>', self.handle_key_release)
            entry_boxes.append(entry)
        return entry_boxes

    def validate_entry(self, text):
        return text == "" or (text.isalpha() and len(text) == 1)

    def handle_key_release(self, event):
        entry_widget = event.widget
        if len(entry_widget.get()) == 1:
            next_widget = entry_widget.tk_focusNext()
            next_widget.focus_set()



    def update_candidate_words(self):
        green_letters = [entry.get().lower() if entry.get() else "_" for entry in self.green_row]
        yellow_letters = [entry.get().lower() if entry.get() else "_" for entry in self.yellow_row]
        grey_letters = [entry.get().lower() if entry.get() else "_" for entry in self.grey_row]

        new_candidate_words = []

        for word in self.english_words:
            if len(word) == 5:
                valid = True

                for i, letter in enumerate(green_letters):
                    if letter != "_" and word[i] != letter:
                        valid = False
                        break

                for i, letter in enumerate(yellow_letters):
                    if letter != "_":
                        if letter == word[i]:
                            valid = False
                            break
                        elif letter not in word:
                            valid = False
                            break

                for letter in grey_letters:
                    if letter != "_" and letter in word:
                        valid = False
                        break

                if valid:
                    new_candidate_words.append(word)

        self.candidate_words = new_candidate_words





    def display_candidates(self):
        sorted_candidates = sorted(self.candidate_words)
        
        if not sorted_candidates:
            messagebox.showinfo("No Solutions", "There are no remaining possible words.")
        else:
            messagebox.showinfo("Possible Words", f"Remaining possible words: {', '.join(sorted_candidates)}")


    def submit_feedback(self):
        self.update_candidate_words()
        self.display_candidates()


def main():
    root = tk.Tk()
    wordle_solver = WordleSolver(root)
    root.mainloop()

if __name__ == "__main__":
    main()

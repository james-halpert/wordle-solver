from flask import Flask, render_template, request
import nltk
from nltk.corpus import words

nltk.download('words')  # Ensure the words corpus is downloaded

app = Flask(__name__)

# Load and preprocess words
english_words = set(words.words())
candidate_words = [word.lower() for word in english_words if len(word) == 5]

def update_candidate_words(green_letters, yellow_letters, grey_letters):
    new_candidate_words = []

    for word in candidate_words:
        valid = True

        # Check green letters
        for i, letter in enumerate(green_letters):
            if letter and word[i] != letter:  # Skip if letter is empty
                valid = False
                break

        # Check yellow letters
        for i, letter in enumerate(yellow_letters):
            if letter:
                if letter == word[i]:  # Letter cannot be in the same position
                    valid = False
                    break
                if letter not in word:  # Letter must be in the word
                    valid = False
                    break

        # Check gray letters
        for letter in grey_letters:
            if letter in word:
                valid = False
                break

        if valid:
            new_candidate_words.append(word)

    return sorted(new_candidate_words)


@app.route("/", methods=["GET", "POST"])
def wordle_solver():
    green_letters = [""] * 5
    yellow_letters = [""] * 5
    grey_letters = ""
    result = None

    if request.method == "POST":
        green_letters = [request.form.get(f"green{i}", "").lower() for i in range(5)]
        yellow_letters = [request.form.get(f"yellow{i}", "").lower() for i in range(5)]
        grey_letters = request.form.get("grey", "").lower()

        grey_letters = ''.join(char for char in grey_letters if char.isalpha())
        result = update_candidate_words(green_letters, yellow_letters, grey_letters)

    return render_template("index.html", result=result, green_letters=green_letters, yellow_letters=yellow_letters, grey_letters=grey_letters)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=99)

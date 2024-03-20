import os
import re
from pathlib import Path

import typer

app = typer.Typer()

import spacy
from huspacy import components

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, blue, green, red, orange

# Define colors for different entity types
entity_colors = {
    "PER": blue,
    "ORG": orange,
    "LOC": red,
    "MISC": green
    # Add more entity types and their colors here
}


def wrap_text_(text, max_width, canvas, font_name="Helvetica", font_size=10):
    """Wrap text to fit into a specified width and return line positions."""
    words = text.split(' ')
    wrapped_lines = []
    line_positions = []  # List to store start and end positions of each line in the original text
    current_line = ''
    current_position = 0  # Track the current character position in the original text
    line_start_position = 0  # Start position of the current line in the original text

    for word in words:
        # Include a space before the word if it's not the first word in the line
        if current_line:  # Not the first word
            test_line = f"{current_line} {word}"
            additional_length = len(word) + 1  # +1 for the space
        else:  # First word in the line
            test_line = word
            additional_length = len(word)

        # Check if adding the next word exceeds the max width
        if canvas.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
            current_position += additional_length
        else:
            # Append the current line and its positions if the next word would exceed the max width
            wrapped_lines.append(current_line)
            line_positions.append((line_start_position, current_position - (len(word) + 1 if current_line else len(word))))
            current_line = word
            line_start_position = current_position - len(word)
            current_position += additional_length

            # If this was the first word of the line, adjust the line start position correctly
            if current_line == word:
                line_start_position += 1  # Adjust for space

    # Add the last line if there's any
    if current_line:
        wrapped_lines.append(current_line)
        line_positions.append((line_start_position, current_position))

    return wrapped_lines, line_positions


def wrap_text(text, max_width, canvas, font_name="Helvetica", font_size=10):
    """Wrap text to fit into a specified width and return line positions."""
    words = text.split(' ')
    wrapped_lines = []
    line_positions = []
    current_line = ''
    line_start_position = 0

    def add_word_to_line(word, is_first_word):
        """Adds a word to the current line, adjusting for spacing and calculating width."""
        nonlocal current_line, line_start_position
        if is_first_word:
            new_line = word
        else:
            new_line = f"{current_line} {word}"
        return new_line

    for index, word in enumerate(words):
        is_first_word = index == 0 or not current_line
        new_line = add_word_to_line(word, is_first_word)

        if canvas.stringWidth(new_line, font_name, font_size) > max_width and not is_first_word:
            # Line is full, append current line and reset for new line
            wrapped_lines.append(current_line)
            line_positions.append((line_start_position, line_start_position + len(current_line)))
            line_start_position += len(current_line) + 1  # Account for space
            current_line = word  # Start new line with current word
        else:
            current_line = new_line  # Add word to line

    # Handle last line if it exists
    if current_line:
        wrapped_lines.append(current_line)
        line_positions.append((line_start_position, line_start_position + len(current_line)))

    # Adjust end positions for accuracy
    adjusted_line_positions = []
    for start, end in line_positions:
        end_position = start + len(text[start:end].rstrip())  # Adjust end to ignore trailing spaces
        adjusted_line_positions.append((start, end_position))

    return wrapped_lines, adjusted_line_positions


def add_page(c, y_position, page_height):
    """Check if a new page is needed and add it if so."""
    if y_position < 50:  # Assuming 50 as bottom margin
        c.showPage()
        c.setFont("Helvetica", 10)
        return page_height - 40  # Reset to top position with top margin
    return y_position

def render_pdf_with_wrapped_text(texts, entities_list, filename="output.pdf"):
    remove_spec_chars = lambda x: x.replace("Ő", "Ö").replace("ő", "ö").replace("Ű", "Ü").replace("ű", "ü")
    # Ensure the output directory exists
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    page_width, page_height = letter
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 10)
    y_position = page_height - 40  # Starting Y position with top margin
    line_height = 14  # Adjust based on font size and preferences
    padding_between_texts = 20  # Space between different texts
    max_width = 460  # Maximum width for text before wrapping

    for text, entities in zip(texts, entities_list):
        # First, wrap the entire text as if there were no entities
        wrapped_lines, positions = wrap_text(text, max_width, c)

        # Next, process each line to handle entities within it
        for line, (start_idx_in_text, end_idx_in_text) in zip(wrapped_lines, positions):
            y_position = add_page(c, y_position, page_height)  # Check if we need a new page

            line_entities = [e for e in entities if e.start_char < end_idx_in_text and e.end_char > start_idx_in_text]

            current_x_position = 72  # Reset X position for each new line
            current_position_in_line = 0

            for entity in line_entities:
                entity_start_in_line = max(entity.start_char - start_idx_in_text, 0)
                entity_end_in_line = min(entity.end_char - start_idx_in_text, len(line))

                # Text before the entity in the current line
                before_entity_text = line[current_position_in_line:entity_start_in_line]
                before_entity_text = remove_spec_chars(before_entity_text)
                c.setFillColor(black)
                c.drawString(current_x_position, y_position, before_entity_text)
                current_x_position += c.stringWidth(before_entity_text, "Helvetica", 10)

                # Entity text
                entity_text = line[entity_start_in_line:entity_end_in_line]
                entity_text = remove_spec_chars(entity_text)
                c.setFillColor(entity_colors.get(entity.label_, black))
                c.drawString(current_x_position, y_position, entity_text)
                current_x_position += c.stringWidth(entity_text, "Helvetica", 10)

                current_position_in_line = entity_end_in_line

            # Text after the last entity or the whole line if no entities
            after_last_entity_text = line[current_position_in_line:]
            after_last_entity_text = remove_spec_chars(after_last_entity_text)
            c.setFillColor(black)
            c.drawString(current_x_position, y_position, after_last_entity_text)

            y_position -= line_height  # Move to the next line

        y_position -= padding_between_texts  # Extra space before the next text block
        y_position = add_page(c, y_position, page_height)  # Ensure space for the next text

    c.save()

def clean_text(text):
    text = text.replace('\n', ' ')
    return text

# Step 2: Text cleaning function
def preprocess_text(text):
    # Replace "\n-" with nothing
    processed_text = re.sub(r'-\n', '', text)
    # # Lowercase
    # processed_text = text.lower()
    # Replace newline characters and redundant whitespaces with a single space
    processed_text = re.sub(r'\s+', ' ', processed_text)
    # Remove punctuation
    processed_text = re.sub(r'[^\w\s]', '', processed_text)
    # Trim leading and trailing spaces
    processed_text = processed_text.strip()
    return processed_text

def get_ner(nlp, ocr_text):
    doc = nlp(ocr_text)
    entities = dict()
    for ent in doc.ents:
        label, text = ent.label_, ent.text
        if label not in entities:
            entities[label] = []
        entities[label].append(text)
    for label in entities:
        entities[label] = ";".join(entities[label])

    return entities, doc.ents


def load_model(model_path: Path):
    nlp = spacy.load(model_path)
    # nlp.add_pipe("conll_formatter")
    return nlp

@app.command()
def ner_it(
        model_path: Path = "/storage/huspacy/hu_core_news_trf/models/hu_core_news_trf-3.7.0",
        input_path: Path = "/storage/huspacy/ner_test/data/",
        output_path: Path = "/storage/huspacy/ner_test/results/"
):
    nlp = load_model(model_path)

    texts = []
    entities_list = []

    for i, input_file in enumerate(input_path.glob("*.txt")):
        # if i != 4:
        #     continue
        with open(input_file, 'r') as inp:
            ocr_text = inp.read()
            print(f"Input text:\n{ocr_text}")
            cleaned_text = preprocess_text(ocr_text)
            entities_dict, entities_spacy = get_ner(nlp, cleaned_text)
            texts.append(cleaned_text)
            entities_list.append(entities_spacy)
            print("\nEntities:")
            for label, text in entities_dict.items():
                print(f"\t{label}: {text}")
            print("\n")

    render_pdf_with_wrapped_text(texts, entities_list, os.path.join(output_path, "ner_results.pdf"))


if __name__ == "__main__":
    app()

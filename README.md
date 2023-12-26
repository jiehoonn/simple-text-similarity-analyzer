# Project Overview
- The 'TextModel' class in Python, serving as a omprehensive tool for analyzing and comparing textual content. This was developed as my final project in CS111 in hopes of being able to detect whether multiple pieces of text are written by the same author.

## Core Functionalities
- **Model Initialization:** Initializes with a model name and creates dictionaries for words, word lengths, stems, sentence lengths, and first-person pronouns.
- **Text Analysis:** Analyzes text to populate the dictionaries with data, handling sentence segmentation and word processing.
- **Stemming Algorithm:** Includes a custom 'stem' function to normalize words by removing common prefixes and suffixes.
- **Text Comparison:** Implements 'similarity_scores' to compute log similarity scores between different text models, based on features like word usage and sentence structure.
- **Classification Feature:** Uses the 'classify' method to compare a text model against two other models, determining the more likely source of the text.
- **File Handling:** Features 'add_file', 'save_model', and 'read_model' methods for processing text files and saving/loading model data.
- **Test Function:** Incorporates a 'run_tests' function to demonstrate the model's capabilities with various text samples.

## Technical Implementation
- Utilizes Python's object-oriented programming capabilities to create a versatile and reusable text analysis tool.
- Employs mathematical and statistical techniques for analyzing text features and calculating similarity scores.

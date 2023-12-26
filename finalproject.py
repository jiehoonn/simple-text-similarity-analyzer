#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 17:50:37 2023

@author: jiehoonn
"""
import math

class TextModel:
    
    def __init__(self, model_name):
        """ constructor for class TextModel
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.first_person_pronouns = {}


        
    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of first person pronouns: ' + str(len(self.first_person_pronouns)) 
        return s
    
    def add_string(self, s):
        """ Analyzes the string s and adds its pieces
            to all of the dictionaries in this text model.
        """
        # Update for sentence lengths
        sentences = s.replace('.', '|').replace('!', '|').replace('?', '|').split('|') # Account for all sentence-ending punctuation
        
         # This doesn't seem to work with single sentence strings... # FIXED
        for sentence in sentences:
            words = clean_text(sentence)
            sentence_length = len(words)
            if sentence_length > 0: # Avoid empty sentences
                if sentence_length in self.sentence_lengths:
                    self.sentence_lengths[sentence_length] += 1
                else:
                    self.sentence_lengths[sentence_length] = 1
        
        # Clean the text and split it into a list of words
        word_list = clean_text(s)
        
        pronouns = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
        
        for w in word_list:
            # Update self.words to reflect w
            # Either add a new key-value pair for w
            # or update the existing key-value pair
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
    
            # Update self.word_lengths
            word_length = len(w)
            if word_length in self.word_lengths:
                self.word_lengths[word_length] += 1
            else:
                self.word_lengths[word_length] = 1
            
            # Update for stem(s)
            stemmed = stem(w)
            if stemmed in self.stems:
                self.stems[stemmed] += 1
            else:
                self.stems[stemmed] = 1
                
            # Update for first person pronouns    
            lower_word = w.lower()
            if lower_word in pronouns:
                if lower_word in self.first_person_pronouns:
                    self.first_person_pronouns[lower_word] += 1
                else:
                    self.first_person_pronouns[lower_word] = 1
                    
            
    def add_file(self, filename):
        """ Adds all of the text in the file identified by filename to the 
            model.
        """
        with open(filename, 'r', encoding='utf8', errors='ignore') as f:
            content = f.read()
        self.add_string(content)
        
    def save_model(self):
        """ Saves the TextModel object by writing its feature dictionaries
            to separate files.
        """
        
        # WORDS
        words_filename = self.name + '_words'
        f_words = open(words_filename, 'w')
        f_words.write(str(self.words)) 
        f_words.close()
        
        # WORD LENGTHS
        word_lengths_filename = self.name + '_word_lengths'
        f_word_lengths = open(word_lengths_filename, 'w')
        f_word_lengths.write(str(self.word_lengths))  
        f_word_lengths.close()
        
        # UPDATE STEMS
        f_stems = open(self.name + '_stems', 'w') # Instead of creating another variable to hold self.name + '_stems', just directly input into open function
        f_stems.write(str(self.stems))
        f_stems.close()
        
        # UPDATE SENTENCE_LENGTHS
        f_sentence_lengths = open(self.name + '_sentence_lengths', 'w')
        f_sentence_lengths.write(str(self.sentence_lengths))
        f_sentence_lengths.close()
        
        # UPDATE FIRST_PERSON_PRONOUNS
        f_first_person_pronouns = open(self.name + '_first_person_pronouns', 'w')
        f_first_person_pronouns.write(str(self.first_person_pronouns))
        f_first_person_pronouns.close()
    
    def read_model(self):
        """ Reads the model data from files and updates the TextModel object's 
            feature dictionaries.
        """
        
        # WORDS
        words_filename = self.name + '_words'
        f_words = open(words_filename, 'r')
        words_str = f_words.read()
        self.words = dict(eval(words_str))
        f_words.close()
        
        # WORD LENGTHS
        word_lengths_filename = self.name + '_word_lengths'
        f_word_lengths = open(word_lengths_filename, 'r')
        word_lengths_str = f_word_lengths.read()
        self.word_lengths = dict(eval(word_lengths_str))
        f_word_lengths.close()
        
        # UPDATE STEMS
        f_stems = open(self.name + '_stems', 'r') # SAME THING ^^^^^
        self.stems = dict(eval(f_stems.read())) # Directly input f_stems.read() into dict(eval()) instead of making another variable to make more concise
        f_stems.close()
        
        # UPDATE SENTENCE_LENGTHS
        f_sentence_lengths = open(self.name + '_sentence_lengths', 'r')
        self.sentence_lengths = dict(eval(f_sentence_lengths.read()))
        f_sentence_lengths.close()
        
        # UPDATE FIRST_PERSON_PRONOUNS
        f_first_person_pronouns = open(self.name + '_first_person_pronouns', 'r')
        self.first_person_pronouns = dict(eval(f_first_person_pronouns.read()))
        f_first_person_pronouns.close()
        
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring the 
            similarity of self and other – one score for each type of feature 
            (words, word lengths, stems, sentence lengths, and your additional 
            feature).
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sentence_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        first_person_pronouns_score = compare_dictionaries(other.first_person_pronouns, self.first_person_pronouns)
        scores = [word_score, word_length_score, stem_score, sentence_length_score, first_person_pronouns_score]
        return scores
    
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other “source” 
            TextModel objects (source1 and source2) and determines which of 
            these other TextModels is the more likely source of the called 
            TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)

        print('scores for ' + source1.name + ': ' + str(scores1))
        print('scores for ' + source2.name + ': ' + str(scores2))

        count_source1 = 0
        count_source2 = 0

        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count_source1 += 1
            elif scores2[i] > scores1[i]:
                count_source2 += 1

        if count_source1 > count_source2:
            result_message = self.name + ' is more likely to have come from ' + source1.name
        elif count_source2 > count_source1:
            result_message = self.name + ' is more likely to have come from ' + source2.name
        else:
            result_message = self.name + ' has an equal likelihood of coming from ' + source1.name + ' or ' + source2.name

        print(result_message)

        
def clean_text(txt):
    """ takes a string of text txt and returns a list containing the words in txt
        after being processed without worring about punctuation or special characters.
    """
    punctuation = ".,?\"'!;:"
    for symbol in punctuation:
        txt = txt.replace(symbol, '')
    txt = txt.lower()
    words = txt.split()
    return words

def stem(s):
    """ helper function that returns the stem of string s, excluding prefixes and suffixes
    """
    # Plural words ending in 'es'
    if s[-2:] == 'es':
        if s[-3:] == 'ies':
            return s[:-3] + 'i' # Replace 'ies' with 'i' ('parties' to 'parti)
        else:
            return s[:-2]
    # Plural words ending in 's'
    elif s[-1:] == 's':
        return s[:-1]
    # Words ending in 'ing'
    elif s[-3:] == 'ing':
        if len(s) > 4 and s[-4] == s[-5]: # Deals with potential double lettering
            return s[:-4]
        else:
            return s[:-3]
    # Past tense with 'ed'
    elif s[-2:] == 'ed':
        return s[:-2]
    # Words ending in 'er'
    elif s[-2:] == 'er':
        return s[:-2]
    # Words ending in 'ly'
    elif s[-2:] =='ly':
        return s[:-2]
    # Words ending in 'ful'
    elif s[-3:] == 'ful':
        return s[:-3]
    # Words ending in 'y'
    elif s[-1] == 'y':
        return s[:-1] + 'i'
    # Words ending in 'e' that are at least 4 characters long
    elif s[-1] == 'e' and len(s) >= 4:
        return s[:-1]
    # Words ending in 'iers' or 'ers'?
    elif s[-3:] == 'ers':
        return s[:-3]
    elif s[-3:] == 'ies':
        return s[:-3] + 'y'
    elif s[-2:] == 'es' and s[-4:] != 'ness':
        return s[:-2]
    elif s[-1:] == 's' and s[-2:] != 'ss':
        return s[:-1]
    elif s[-3:] == 'ing':
        if len(s) > 4 and s[-4] == s[-5]:
            return s[:-4]
        else:
            return s[:-3]
    elif s[-2:] == 'ed' and len(s) > 4:
        return s[:-2]
    elif s[-2:] in ['er', 'ly'] and len(s) > 4:
        return s[:-2]
    elif s[-3:] == 'ful':
        return s[:-3]
    elif s[-1] == 'y':
        return s[:-1] + 'i'
    elif s[-1] == 'e' and len(s) >= 4:
        return s[:-1]
    elif s[-3:] == 'ers':
        return s[:-3]
    elif s[-4:] == 'ness':
        return s[:-4]
    # Leave word as is
    return s

def compare_dictionaries(d1, d2):
    """ takes two feature dictionaries d1 and d2 as inputs, and it should 
        compute and return their log similarity score
    """
    # If dictionary is empty
    if d1 == {}:
        return -50
    # Get total amount
    total = 0
    for key in d1:
        total += d1[key]
    # Scoring calculation
    score = 0
    for item in d2:
        if item in d1:
            probability = d1[item] / total
        else:
            probability = 0.5 / total
            
        score += d2[item] * math.log(probability)
    return score

# Copy and paste the following function into finalproject.py
# at the bottom of the file, *outside* of the TextModel class.
def run_tests():
    # Text File 1
    source1 = TextModel('how i met your mother')
    source1.add_file('HIMYM.txt')

    # Text File 2
    source2 = TextModel('friends')
    source2.add_file('Friends.txt')

    # Text File 3
    new1 = TextModel('how i met your mother 2')
    new1.add_file('HIMYM1.txt')
    new1.classify(source1, source2)

    # Text File 4
    new2 = TextModel('friends 2')
    new2.add_file('Friends1.txt')
    new2.classify(source1, source2)
    
    # Text File 5
    new3 = TextModel('the big bang theory')
    new3.add_file('TBBT.txt')
    new3.classify(source1, source2)
    
    # Text File 6
    new4 = TextModel('the office')
    new4.add_file('TheOffice.txt')
    new4.classify(source1, source2)
    
    
    
    
    

# -*- coding: utf-8 -*-
"""
Class Player 
"""

word_length = 5

class Game:
    
    def __init__(self): 
        
        self.filename = 'palabras.txt'
        self.word_length = 5 
        file = open(self.filename, 'r', encoding = 'utf-8')
        lst = []
        
        for word in file:
            word = word.strip()
            if len(word) == self.word_length:
                lst.append(word)
        file.close()
        
        self.wordlst = lst
        self.storage = []
        self.status = 'Next'
        
        

class Player(Game):
    
    def __init__(self, wordlst, storage):
        
        self.wordlst = wordlst
        self.storage = storage
    
        Game.__init__(self)
        
        
    def candidate(self, user_word):
        
        result = False
        if len(user_word) != word_length:
            
            print(f'The user word has not {word_length} letters.')
            
        elif user_word not in self.wordlst:
            
            print("The word is not in filename.")
        
        elif user_word in self.storage:
            print("You have already tried with that word")
        
        else:
            self.storage.append(user_word)
            result = True

        return result



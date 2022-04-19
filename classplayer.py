"""
Class Player 
"""

word_length = 5

class Player:
    
    def __init__(self, wordlst, storage):
        
        self.wordlst = wordlst
        self.storage = storage
    
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


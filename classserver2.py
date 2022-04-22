import random

class Game:
    
    def __init__(self):
        
        self.filename = 'ruta archivo'
        self.maxattempts = 6 #intentos hasta que uno de los jugadores los adivine
        self.word_length = 5
        file = open(self.filename, 'r', encoding = 'utf-8')
        lst = []
        #formamos una lista de palabras con aquellas que tienen la longitud pedida
        for word in file:
            word = word.strip()
            
            if len(word) == self.word_length:
                lst.append(word)
        file.close()
        
        self.wordlst = lst
        
        self.storage = {}

       
class Server:
    
    def __init__(self, wordlst):
        
        self.wordlst = wordlst
        
    def generate_secret(self):
        #palabra aleatoria del fichero que escojamos 
        random.seed()
        secret_word = self.wordlst[random.randint(0, len(self.wordlst) - 1)]
        self.secret_word = secret_word
        return secret_word
        
    def get_clue(self, guess):
        pass
        #correccion de la palabra del usuario 
        #return objeto lista-palabra
        
    def get_secret(self):
        
        return self.secret_word
    
    
    
class Correction: 
    
    def __init__(self, guess, clue_cmpnts):
    
        self.guess = guess
        self.clue_cmpnts = clue_cmpnts
    
    def correction_word(secret_word, guessed_word):
        
        lista_aciertos = [0]*(len(secret_word))
        secret_word_list = list(secret_word)
        guessed_word_list = list(guessed_word)
        
        for i in range(len(secret_word)):
            
            if guessed_word_list[i] in secret_word_list:
            
                if guessed_word_list[i] == secret_word[i]:
                
                    lista_aciertos[i] = 0
            
                elif guessed_word_list[i] != secret_word[i]:
                
                    lista_aciertos[i] = 1
        
            elif guessed_word_list not in secret_word_list:
            
                lista_aciertos[i] = 2
                
        return Correction(guessed_word, lista_aciertos)
    
    def is_winner(self):
        pass
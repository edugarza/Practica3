

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
        
    def start_game(self):
        
        self.server = Server(self.wordlst)
        
        self.secret_word = self.server.generate_secret()
        print("Secret word: " + str(self.secret_word))
        self.cont = 0

       
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
        
        guess_clue = Correction.correction_word(self.secret_word , guess)
        return Correction(guess, guess_clue.clue_cmpnts)
        
    def get_secret(self):
        
        return self.secret_word

#añadimos los colores para las soluciones
SEPARATOR = "  "
red = '\033[31m'
green = '\033[32m'
white = '\033[0m'    
    
    
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
        
        winner = True
        
        for pos in self.clue_cmpnts:
            if pos != 0:
                winner = False
                break
        
        return winner
    
    def __str__(self): #representacion de CLUE (verde, rojo y blanco)
        
        word = []
    
        for num, letter in enumerate(self.guess):
        
            if self.clue_cmpnts[num] == 0:
                
                word.append(green + letter.upper() + white) 
                
            elif self.clue_cmpnts[num] == 1:
                
                word.append(red + letter.upper() + white)
                
            elif self.clue_cmpnts[num] == 2:
                
                word.append(letter.upper())
            
            else:
                
                word = ""
    
        return SEPARATOR.join(word)
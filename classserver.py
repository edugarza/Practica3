import random


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
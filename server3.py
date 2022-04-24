import paho.mqtt.client as mqtt
import random
from time import sleep
########################################

BROKER = "wild.mat.ucm.es"
TOPIC_SUB = "clients/EGS_mqtt/questions"
TOPIC_PUB = "clients/EGS_mqtt/answers"

class Game:
    
    def __init__(self):
        
        self.filename = 'lemario.txt'
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

        
    def on_message(self, client, data, msg):
        
        self.storage = []
        user_word = msg.payload.decode('utf-8')
        self.current_clue = self.server.get_clue(user_word)
        final = Correction(user_word, self.current_clue.clue_cmpnts)
        self.storage[user_word] = final.clue_cmpnts
        self.cont += 1
        disconected = True

        if final.is_winner():
            message = f"Congratulations\n{str(self.current_clue)}\nCongratulations, you found the secret word!"
        elif self.cont < self.maxattempts:
            message = 'Next\n' + str(self.current_clue)
            disconected = False
        else:
            message = f'Lost\nTry again! The secret word was {self.secret_word}.'
        
        print(f"Recibido: {user_word}")

        client.publish(TOPIC_PUB, message)

        if disconected:
            print(message.split('\n', 1)[1])
            client.disconnect()

    def start_game(self):
        
        self.server = Server(self.wordlst)
        
        self.secret_word = self.server.generate_secret()
        print("Secret word: " + str(self.secret_word))
        self.cont = 0


        self.client = mqtt.Client() #create new instance
        self.client.connect(BROKER) #connect to broker
        self.client.on_message = self.on_message
        self.client.subscribe(TOPIC_SUB)
        self.client.loop_forever() #start the loop
        
        
class Server:
    
    def __init__(self, wordlst):
        
        self.wordlst = wordlst
        
    def generate_secret(self):
        
        random.seed()
        secret_word = self.wordlst[random.randint(0, len(self.wordlst) - 1)]
        self.secret_word = secret_word
        return secret_word
        
    def get_clue(self, guess):
        
        guess_clue = Correction.correction_word(self.secret_word , guess)
        return Correction(guess, guess_clue.clue_cmpnts)
        
    def get_secret(self):
        
        return self.secret_word

    

SEPARATOR = "  "
red = '\033[31m'
green = '\033[32m'
white = '\033[0m'    
   
class Correction:
    
    def __init__(self, candidate, clue):
        
        self.candidate = candidate
        self.clue = clue
    
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
                
            elif self.clue_cmpnts[num] == 2:
                
                word.append(red + letter.upper() + white)
                
            elif self.clue_cmpnts[num] == 1:
                
                word.append(letter.upper())
            
            else:
                
                word = ""
    
        return SEPARATOR.join(word)


if __name__ == '__main__':
    Game().start_game()
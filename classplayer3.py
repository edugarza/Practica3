import paho.mqtt.client as mqtt
from multiprocessing import Process
from time import sleep

########################################

BROKER="wild.mat.ucm.es"
TOPIC_PUB = "clients/EGS_mqtt/questions"
TOPIC_SUB = "clients/EGS_mqtt/answers"

game_state = 'Next'

class Game:
    
    def __init__(self):
        
        self.filename = 'lemario.txt'
        self.word_length = 5 #solo seleccionar palabras de 5 letras (base de juego)
        #se puede añadir un input para establecer una configuracion del juego
        file = open(self.filename, 'r', encoding = 'utf-8')
        lst = []
        #formamos una lista de palabras con aquellas que tienen la longitud pedida
        for word in file:
            word = word.strip()
            
            if len(word) == self.word_length:
                lst.append(word)
        file.close()
        
        self.wordlst = lst
        
        self.storage = []

        self.status = 'Next'
        
    def on_message(self, client, data, msg):
        global game_state
        response = msg.payload.decode('utf-8').split('\n', 1)
        print(response[1])
        # si no somos nosotros los que hemos escrito la palabra, forzamos un enter
        print('Presiona Enter si no enviaste la palabra...',)
        game_state = response[0]
        client.disconnect()


    def subscriber(self):
        global game_state

        while game_state == 'Next':
            self.client_sub.connect(BROKER) #connect to broker
            self.client_sub.subscribe(TOPIC_SUB)
            self.client_sub.on_message = self.on_message
            if game_state == 'Next':
                self.client_sub.loop_forever()


    def start_game(self):
        
        self.player = Player(self.wordlst, self.storage)
        
        client_pub = mqtt.Client() #create new instance
        client_pub.connect(BROKER) #connect to broker

        self.client_sub = mqtt.Client() #create new instance

        # Lanzar subproceso
        self.subscriber_process = Process(target=self.subscriber,
                      name=f"subscriber_process")
        self.subscriber_process.start()

        while self.subscriber_process.is_alive():
            client_pub.loop_start()
            current_word = input("Write a 5 letter word:\n")
            # or key in word
            while not self.player.next_candidate(current_word) and self.subscriber_process.is_alive():
                current_word = input("Write a 5 letter word:\n")
            client_pub.publish(TOPIC_PUB, current_word)
            client_pub.loop_stop()
            self.subscriber_process.join(timeout=0)
            sleep(1)
        print('End of game')

class Player(Game):
    
    def __init__(self, wordlst, storage): #herencia de datos de la clase Game
        
        self.wordlst = wordlst
        self.storage = storage
    
        Game.__init__(self)
    
    def next_candidate(self, user_word):
        
        result = False
        if len(user_word) != self.word_length:
            
            # print(f'The user word has not {self.word_length} letters.')
            pass
            
        elif user_word not in self.wordlst:
            
            print("The word is not in filename.")
        
        elif user_word in self.storage:
            print("You have already tried with that word")
        
        else:
            self.storage.append(user_word)
            result = True

        return result

if __name__ == '__main__':
    Game().start_game()
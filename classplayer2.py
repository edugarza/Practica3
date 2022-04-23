import paho.mqtt.client as mqtt
from random import randint
from time import sleep
########################################

BROKER="wild.mat.ucm.es"
TOPIC_PUB = "clients/EGS_mqtt/questions"
TOPIC_SUB = "clients/EGS_mqtt/answers"

word_found = False

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
        
    def on_message(self, client, data, msg):
        response = msg.payload.decode('utf-8').split('\n', 1)
        print(response[1])
        self.status = response[0]
        sleep(1)
        client.disconnect()

    def start_game(self):
        
        self.player = Player(self.wordlst, self.storage)
        
        client_pub = mqtt.Client() #create new instance
        client_pub.connect(BROKER) #connect to broker

        client_sub = mqtt.Client() #create new instance

        while self.status == 'Next':
            client_sub.connect(BROKER) #connect to broker
            client_sub.subscribe(TOPIC_SUB)
            client_sub.on_message = self.on_message
            client_pub.loop_start()
            word = input("Write a 5 letter word: ")
            while not self.player.candidate(word):
                word = input("Write a 5 letter word: ")
            client_pub.publish(TOPIC_PUB, word)
            client_pub.loop_stop()
            client_sub.loop_forever()



class Player(Game):
    
    def __init__(self, wordlst, storage):
        
        self.wordlst = wordlst
        self.storage = storage
    
        Game.__init__(self)
        
        
    def candidate(self, user_word):
        
        result = False
        if len(user_word) != word_length:
            
            # print(f'The user word has not {word_length} letters.')
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
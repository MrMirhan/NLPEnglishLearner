import pandas as pd
import numpy as np
import spacy
nlp = spacy.load("tr_core_news_lg")

lang_df = pd.read_csv('./TR2EN.txt', sep='\t', header=None, names=['en', 'tr'])

class Player:
    def __init__(self):
        self.name = "Player"
        self.points = 0
        self.lives = 3
        self.level = 1
        self.learned_words = []

    def change_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def get_points(self):
        return self.points
    
    def get_lives(self):
        return self.lives
    
    def get_level(self):
        return self.level
    
    def get_learned_words(self):
        return self.learned_words
    
    def add_points(self, points):
        self.points += points

    def add_lives(self, lives):
        self.lives += lives

    def add_level(self, level):
        self.level += level

    def add_learned_words(self, en, tr):
        self.learned_words.append([en, tr])

    def remove_lives(self, lives):
        self.lives -= lives

    def remove_level(self, level):
        self.level -= level

    def remove_learned_words(self, en, tr):
        self.learned_words.remove([en, tr])

    def reset_points(self):
        self.points = 0

    def reset_lives(self):
        self.lives = 3

    def reset_level(self):
        self.level = 1

    def reset_learned_words(self):
        self.learned_words = []

    def reset_all(self):
        self.reset_points()
        self.reset_lives()
        self.reset_level()
        self.reset_learned_words()

    def calculate_points(self, level, word_len):
        # Make harder gain points every level and gain poıints by correct words length
        return level * word_len

    def level_up(self):
        # Calculate new level based on current level and points
        level_scale_factor = 1.2  # adjust this value to make the requirements more or less challenging
        next_level_points = int(self.level ** level_scale_factor * 100)
        
        if self.points >= next_level_points:
            self.level += 1
            
            # Increase starting lives and points based on new level
            self.lives = 3 + self.level // 5
            self.points = int((self.level - 1) ** level_scale_factor * 100)
            
            print(f"Congratulations, you've reached level {self.level}!")
            print(f"You now have {self.lives} lives and {self.points} points.")

    def __str__(self):
        return f"Name: {self.name}\nPoints: {self.points}\nLives: {self.lives}\nLevel: {self.level}\nLearned Words: {len(self.learned_words)}"

class Game:
    def __init__(self):
        self.words = []
        self.current_word = ""
        self.words = lang_df
    
    def get_current_word(self):
        return self.current_word
    
    def __str__(self):
        return f"Player: {self.player}\nWords: {self.words}\nCurrent TR: {self.current_word.iloc[0]['tr']}\nCurrent EN: {self.current_word.iloc[0]['tr']}"
    
    def get_random_word(self):
        return self.words.sample(n=1)
    
    def check_similarity(self, word1, word2):
        doc1 = nlp(word1)
        doc2 = nlp(word2)
        return doc1.similarity(doc2)
    
class Main:
    def __init__(self):
        self.game = Game()
        self.player = Player()
        self.game.player = self.player
        self.game.current_word = self.game.get_random_word()
        print("Welcome to the game!")
        print("Please enter your name: ")
        self.player.change_name(input())

    def start(self):
        print(f"Welcome {self.player.get_name()}")
        print("Press [1] to start the game")
        print("Press [2] to show player info")
        print("Press [3] to show game info")
        print("Press [4] to reset all")
        print("Press [5] to exit")
        choice = input()
        if choice == "1":
            self.game_loop()
        elif choice == "2":
            print(self.player)
            self.start()
        elif choice == "3":
            print(self.game)
            self.start()
        elif choice == "4":
            self.player.reset_all()
            self.start()
        elif choice == "5":
            print("Goodbye!")
            exit()
        else:
            print("Wrong choice!")
            self.start()

    def game_loop(self):
        while self.player.get_lives() > 0:
            self.game.current_word = self.game.get_random_word()
            print(f"Question: {self.game.current_word['en'].values[0]}")
            guess = input("Enter your guess (or 'menu' to go back to menu): ").lower()
            if guess == "menu":
                self.start()
                break
            if self.game.check_similarity(guess, self.game.current_word.iloc[0]["tr"].lower()) > 0.60:
                self.player.add_points(self.player.calculate_points(self.player.get_level(), len(self.game.current_word['en'].values[0])))
                self.player.add_learned_words(self.game.current_word['en'].values[0], self.game.current_word['tr'].values[0])
                self.player.level_up()
                print("Correct answer! You earned points and leveled up.")
            else:
                self.player.remove_lives(1)
                print("Incorrect answer! Tha answer was `" + self.game.current_word.iloc[0]["tr"] + "` You lost one life.")

        print("Game over!")

if __name__ == "__main__":
    main = Main()
    main.start()
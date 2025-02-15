from os import system
from time import time

class Data_Handler:
    def __init__(self):
        self.charts = [
            {"name": "funny test", 
             "difficulty": 1, 
             "patterns": ["test test test test"] * 2},
            
            {"name": "first map ong", 
             "difficulty": 8, 
             "patterns": [
                 "first map ong",
                 "imagine super long word",
                 "do you got hippopotomonstrosesquipedaliophobia?",
                 ":)",
                 "1 2 3 4 5 6 7 8 9 0",
                 "qwerty yuiop",
                 "pretty fun chart"
                 ]},
        ]

    def get_chart(self, name):
        for chart in self.charts:
            if chart["name"] == name:
                return chart

class User:
    def __init__(self):
        self.lives = 3
        self.menu_ptr = 0
        self.best = {"name": "", 
                     "time": -1, 
                     "wpm": -1, 
                     "score": -1}

    def clear_console(self):
        system("cls")

    def set_best(self, chart, time, wpm, score):
        if time == -1 or wpm == -1:
            return
        else:
            self.best["name"] = chart["name"]
            self.best["time"] = time
            self.best["wpm"] = wpm
            self.best["score"] = score
            
    def display_menu(self, game, data):
        game_started = False
        while not game_started:
            self.clear_console()
            print(" - {} ({})".format(data.charts[self.menu_ptr]["name"], data.charts[self.menu_ptr]["difficulty"]))
            menu_action = input(">> ")
            if menu_action.lower() == "prev":
                if len(data.charts) - 1 > self.menu_ptr:
                    self.menu_ptr += 1
            elif menu_action.lower() == "next":
                if len(data.charts) > abs(self.menu_ptr):
                    self.menu_ptr -= 1
            elif menu_action.lower() == "play":
                game_started = True
                game.start_chart(data.charts[self.menu_ptr]["name"], data, self)      

class Game:
    def __init__(self):
        self.current_chart = {"name": '',
                              "difficulty": -1, 
                              "score": -1, 
                              "wpm": -1,
                              "combo": -1,
                              "maxcombo": -1}

    def start_chart(self, name, data, user):
        chart = data.get_chart(name)
        if chart:
            start_time = time()
            
            self.current_chart["name"] = chart["name"]
            self.current_chart["difficulty"] = chart["difficulty"]
            self.current_chart["score"] = 0
            self.current_chart["combo"] = 0
            
            for pattern in chart["patterns"]:
                user.clear_console()
                if user.lives > 0:
                    input_start = time()
                    print(pattern)
                    input_pattern = input(">> ")
                    input_end = time()
                    if pattern != input_pattern:
                        user.lives -= 1
                    else:
                        if (1000 * len(pattern.split(' ')) * (len(pattern) / 2)) - ((input_end - input_start) * 1000) > 0:
                            self.current_chart["score"] += (1000 * len(pattern.split(' ')) * (len(pattern) / 2)) - ((input_end - input_start) * 1000)
                            self.current_chart["combo"] += 1
                        else:
                            user.lives -= 1
                            if self.current_chart["maxcombo"] < self.current_chart["combo"]:    
                                self.current_chart["maxcombo"] = self.current_chart["combo"]
                            self.current_chart["combo"] = 0
                else:
                    break
            
            user.clear_console()
            end_time = time()
            
            if user.lives > 0:
                print("you won!")
            else:
                print("you lose!")
            if self.current_chart["maxcombo"] < self.current_chart["combo"]:    
                self.current_chart["maxcombo"] = self.current_chart["combo"]
            self.current_chart["time"] = end_time - start_time
            
            print("time elapsed: {:.2f}s\n".format(self.current_chart["time"]) +
                  "score earned: {:.2f}\n".format(self.current_chart["score"]) + 
                  "max / last combo: {}/{}\n".format(self.current_chart["maxcombo"], self.current_chart["combo"]))
            user.set_best(chart, self.current_chart["time"], self.current_chart["wpm"], self.current_chart["score"]) 
            
            input("press Enter to continue")
            user.display_menu(self, data)
            
            self.current_chart["name"] = ""
            self.current_chart["difficulty"] = -1
            self.current_chart["wpm"] = -1
            self.current_chart["score"] = -1
            self.current_chart["combo"] = -1
            self.current_chart["maxcombo"] = -1    
            
def main():
    data = Data_Handler()
    user = User()
    game = Game()
    user.display_menu(game, data)

if __name__ == "__main__":
    main()
    
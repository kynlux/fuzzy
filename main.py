from os import system, mkdir, listdir, remove
from os.path import isdir, isfile, join
from time import time, sleep
import threading

class Data_Handler:
    def __init__(self):
        self.charts = []
        
    def init_maps(self, user):
        if isdir("./charts"):
            charts = [f for f in listdir("./charts") if isfile(join("./charts", f))]
            for chart in charts:
                if isfile("./charts/" + chart):
                    chart_file = open("./charts/" + chart)
                    
                    chart_info = {"filename": "./charts/" + chart, "name": "", "difficulty": -1, "creator": "no name", "patterns": []}
                    info_collected = 0
                    for chart_line in chart_file:
                        if info_collected != 3:
                            info_line = chart_line.strip().split(" : ")
                            if len(info_line) > 1:
                                if info_line[1] != "__BASE__":
                                    if info_line[0] == "display":
                                        info_collected += 1
                                        chart_info["name"] = info_line[1]
                                    elif info_line[0] == "diff":
                                        info_collected += 1
                                        chart_info["difficulty"] = info_line[1]
                                    elif info_line[0] == "creator":
                                        info_collected += 1
                                        chart_info["creator"] = info_line[1]
                                else:
                                    info_collected += 1
                        else:
                            if chart_line.strip() != "":
                                chart_info["patterns"].append(chart_line.strip())
                    
                    self.charts.append(chart_info)
                    
                    chart_file.close()
        else:
            mkdir("./charts")
            user.leave("your game has initialized, download base pack of maps (zip in last release) to play\n")

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
                     "score": -1,
                     "maxcombo": -1}

    def clear_console(self):
        system("cls")
        
    def leave(self, reason = ""):
        self.clear_console()
        print(reason + "see you next time\n")
        input("(press Enter to exit)\n")

    def set_best(self, game):
        self.best["name"] = game.current_chart["name"]
        self.best["time"] = game.current_chart["time"]
        self.best["score"] = game.current_chart["score"]
        self.best["maxcombo"] = game.current_chart["maxcombo"]
        
        change_time = False
        change_score = False
        change_maxcombo = False
        
        if isdir("./bests"):
            if not isfile("./bests/" + game.current_chart["name"] + ".txt"):
                create_file = open("./bests/" + game.current_chart["name"] + ".txt", "w")
                create_file.close()
                
            best_file = open("./bests/" + game.current_chart["name"] + ".txt")
            for best_line in best_file:
                info_line = best_line.strip().split(" : ")
                if info_line[0] == "time":
                    self.best["time"] = min(float(self.best["time"]), float(info_line[1]))
                elif info_line[0] == "score":
                    self.best["score"] = max(float(self.best["score"]), float(info_line[1]))
                elif info_line[0] == "maxcombo":
                    self.best["maxcombo"] = max(float(self.best["maxcombo"]), float(info_line[1]))
            best_file.close()
            
            with open("./bests/" + game.current_chart["name"] + ".txt", "w") as f:
                f.write("time : {:.2f}\nscore : {}\nmaxcombo : {}\nscored in: {}".format(self.best["time"], int(self.best["score"]), int(self.best["maxcombo"]), game.version))
                f.close()
        else:
            mkdir("./bests")
            
            if not isfile("./bests/" + game.current_chart["name"] + ".txt"):
                create_file = open("./bests/" + game.current_chart["name"] + ".txt", "w")
                create_file.close()
                
            best_file = open("./bests/" + game.current_chart["name"] + ".txt")
            for best_line in best_file:
                info_line = best_line.strip().split(" : ")
                if info_line[0] == "time":
                    self.best["time"] = min(float(self.best["time"]), float(info_line[1]))
                elif info_line[0] == "score":
                    self.best["score"] = max(float(self.best["score"]), float(info_line[1]))
                elif info_line[0] == "maxcombo":
                    self.best["maxcombo"] = max(float(self.best["maxcombo"]), float(info_line[1]))
            best_file.close()
            
            with open("./bests/" + game.current_chart["name"] + ".txt", "w") as f:
                f.write("time : {:.2f}\nscore : {}\nmaxcombo : {}\nscored in: {}".format(self.best["time"], int(self.best["score"]), int(self.best["maxcombo"]), game.version))
                f.close()
        
    def display_menu(self, game, data):
        game_started = False
        while not game_started:
            self.clear_console()
            if data.charts != []:
                print(" - {} [ {} ]\n    made by {}".format(data.charts[self.menu_ptr]["name"], data.charts[self.menu_ptr]["difficulty"], data.charts[self.menu_ptr]["creator"]))
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
                elif menu_action.lower() == "delete":
                    if isfile(data.charts[self.menu_ptr]["filename"]):
                        remove(data.charts[self.menu_ptr]["filename"])
                        data.charts.pop(self.menu_ptr)
                    self.menu_ptr = 0
                elif menu_action.lower() == "leave":
                    game_started = True
                    self.leave()
            else:
                self.leave("no initial songs! please donwload them from last github release and extract to ./charts folder!\n")

class Game:
    def __init__(self):
        self.current_chart = {"name": '',
                              "difficulty": -1, 
                              "score": -1, 
                              "combo": -1,
                              "maxcombo": -1}
        self.version = "v1.2.2-imsorry"

    def start_chart(self, name, data, user):
        chart = data.get_chart(name)
        if chart:
            start_time = time()
            
            self.current_chart["name"] = chart["name"]
            self.current_chart["difficulty"] = chart["difficulty"]
            self.current_chart["score"] = 0
            self.current_chart["combo"] = 0
            self.current_chart["maxcombo"] = 0  
            user.lives = 3        
            
            for pattern in chart["patterns"]:
                user.clear_console()
                if user.lives > 0:
                    input_start = time()
                    print(pattern + "\n\nlives: {}  combo: {}  score: {:.2f}".format(user.lives, self.current_chart["combo"], self.current_chart["score"]))
                    input_pattern = input(">> ")
                    input_end = time()
                    if pattern != input_pattern:
                        user.lives -= 1
                    else:
                        if (1000 * len(pattern.split(' ')) * (len(pattern) / 2)) - ((input_end - input_start) * 1000) > 0:
                            self.current_chart["score"] += ((1000 * len(pattern.split(' ')) * (len(pattern) / 2)) - ((input_end - input_start) * 1000)) * (self.current_chart["combo"] / 2)
                            self.current_chart["combo"] += 1
                            if user.lives < 3:
                                if self.current_chart["combo"] > 15:
                                    user.lives += 1
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
                if self.current_chart["maxcombo"] < self.current_chart["combo"]:    
                    self.current_chart["maxcombo"] = self.current_chart["combo"]
                self.current_chart["time"] = end_time - start_time
                
                print("time elapsed: {:.2f}s\n".format(self.current_chart["time"]) +
                    "score earned: {:.2f}\n".format(self.current_chart["score"]) + 
                    "max / last combo: {}/{}\n".format(self.current_chart["maxcombo"], self.current_chart["combo"]))
                user.set_best(self) 
            else:
                print("you lose!")
            
            input("(press Enter to continue)")
            user.display_menu(self, data)
            
            self.current_chart["name"] = ""
            self.current_chart["difficulty"] = -1
            self.current_chart["score"] = -1
            self.current_chart["combo"] = -1
            self.current_chart["maxcombo"] = -1    
            user.lives = 3
            
def main():
    data = Data_Handler()
    user = User()
    game = Game()
    data.init_maps(user)
    user.display_menu(game, data)

if __name__ == "__main__":
    main()
    
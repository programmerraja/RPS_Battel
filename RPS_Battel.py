import tkinter as t
from os.path import join
from os import getcwd, _exit
from requests.exceptions import ConnectionError
from tkinter import messagebox
from firebase import firebase
from threading import Thread


class RPS_Battel:
    """ game window"""

    def __init__(s, my_key, my_name, p_key, p_name, app, link, old_root):
        # my keysand name
        s.my_key = my_key
        s.my_name = my_name
        # player key and name
        s.p_key = p_key
        s.p_name = p_name
        # firbase app and link to database
        s.app = app
        s.link = link
        s.old_root = old_root
        # root window
        s.root = t.Tk()
        color = "#26006f"
        s.b_color = "red"
        s.root.wm_resizable(0, 0)
        s.root.configure(bg=color)

        s.root.geometry("590x520+320+30")
        s.root.title("ROCK PAPPER SCISSORS")
        # score for players
        s.my = 0
        s.player = 0
        # round
        s.round = 0

        # frame
        s.frame1 = t.Frame(s.root, height=200, width=600, bg=color)
        s.frame1.place(x=0, y=0)

        # image  for vs
        s.battle_image = t.PhotoImage(file=join(getcwd(), "image", "battle1.png"))
        s.battle = t.Label(s.frame1, image=s.battle_image, bg=color)
        s.battle.place(x=0, y=0)

        # player name and score
        s.my1 = t.Label(
            s.frame1,
            text=s.my_name.upper(),
            font=("arieal", 15, "italic"),
            bg="#01314A",
            fg="yellow",
        )
        s.my1.place(x=40, y=40)
        s.score1 = t.Label(
            s.frame1,
            text=str(s.my),
            font=("arieal", 15, "italic"),
            bg="#01314A",
            fg="yellow",
        )
        s.score1.place(x=60, y=90)

        # opponet name and score
        s.robo = t.Label(
            s.frame1,
            text=s.p_name.upper(),
            font=("arieal", 15, "italic"),
            bg="#FA1C23",
            fg="yellow",
        )
        s.robo.place(x=450, y=40)

        s.score2 = t.Label(
            s.frame1,
            text=str(s.player),
            font=("arieal", 15, "italic"),
            bg="#FA1C23",
            fg="yellow",
        )
        s.score2.place(x=470, y=90)

        s.status = t.Label(
            s.frame1, text="", font=("arieal", 20, "italic"), bg=color, fg="yellow"
        )
        s.status.place(x=150, y=170)

        """    rock papper scissors button """
        s.frame = t.Frame(height=280, width=500, bg=color)
        s.frame.place(x=50, y=200)
        s.scssisor_image = t.PhotoImage(file=join(getcwd(), "image", "scissors.png"))
        s.scissor = t.Button(
            s.frame,
            height=140,
            width=140,
            image=s.scssisor_image,
            command=lambda: s.check("3"),
            relief="groove",
            activebackground=s.b_color,
        )
        s.scissor.place(x=5, y=50)

        s.rock_image = t.PhotoImage(file=join(getcwd(), "image", "rock.png"))
        s.rock = t.Button(
            s.frame,
            width=140,
            height=140,
            image=s.rock_image,
            command=lambda: s.check("1"),
            relief="groove",
            activebackground=s.b_color,
        )
        s.rock.place(x=165, y=50)

        s.paper_image = t.PhotoImage(file=join(getcwd(), "image", "paper.png"))
        s.paper = t.Button(
            s.frame,
            width=140,
            height=140,
            image=s.paper_image,
            command=lambda: s.check("2"),
            relief="groove",
            activebackground=s.b_color,
        )
        s.paper.place(x=325, y=50)

        s.f = t.Frame(height=10, width=20, bg=color).grid()
        s.status["text"] = "   CLICK ANY ONE ! "
        s.backbut = t.Button(
            s.root,
            text="Back To Lobby",
            fg="black",
            bg="green",
            command=s.back,
            activebackground="#f95d9b",
        ).place(x=150, y=470)

        s.exit = t.Button(
            s.root,
            text="Exit",
            font=("arieal", 8, "bold"),
            command=lambda: s.at_exit(1),
            activebackground="#f95d9b",
            bg="green",
            width=10,
        )
        s.exit.place(x=350, y=470)
        # at exit handler
        s.root.protocol("WM_DELETE_WINDOW", s.at_exit)
        
        s.root.mainloop()

    def score_check(s):
        """ match result """

        if s.round == 5:
            if s.my == s.player:
                messagebox.showinfo("DRAW", "  IT'S DIE  !!!")
            else:
                winner = s.my_name.upper() if s.my > s.player else s.p_name.upper()
                messagebox.showinfo("WINNER", winner + " WON THE BATTLE!!!")
            s.back()

    def check(s, my_move):
        """eval the result"""

        try:
            # puting my move on his document
            s.app.put(s.link + "/" + s.p_key, "p_move", my_move)
        except (ConnectionError):
            messagebox.showinfo("WARNING", "No Internet Connection")
            return
        # getting his move from my document
        i = 0
        while i < 11:
            try:
                p_move = s.app.get(s.link, s.my_key + "/p_move")
                if p_move != "0":
                    s.app.put(s.link + "/" + s.my_key, "p_move", "0")
                    break
                else:
                    i += 1
                    if i > 9:
                        messagebox.showinfo(
                            "TIME OUT ", "No Response From Player Try Again Later"
                        )
                        s.back()
            except (ConnectionError):
                messagebox.showinfo("WARNING", "No Internet Connection")
                return

        if my_move == "1":
            if p_move == "1":
                s.status["text"] = "     IT'S  DIE       "
                s.status["fg"] = "black"
            elif p_move == "2":
                s.player = s.player + 1
                s.score2["text"] = ":" + str(s.player)
                s.status["text"] = "     YOU LOOSE !     "
                s.status["fg"] = "red"
            elif p_move == "3":
                s.my += 1
                s.score1["text"] = ":" + str(s.my)
                s.status["text"] = "     YOU WON !        "
                s.status["fg"] = "green"

        elif my_move == "2":
            if p_move == "1":
                s.my += 1
                s.score1["text"] = ":" + str(s.my)
                s.status["text"] = "     YOU WON !        "
                s.status["fg"] = "green"
            elif p_move == "2":
                s.status["text"] = "     IT'S  DIE     "
                s.status["fg"] = "black"
            elif p_move == "3":
                s.player = s.player + 1
                s.score2["text"] = ":" + str(s.player)
                s.status["text"] = "     YOU LOOSE !    "
                s.status["fg"] = "red"
        elif my_move == "3":
            if p_move == "1":
                s.player = s.player + 1
                s.score2["text"] = ":" + str(s.player)
                s.status["text"] = "    YOU LOOSE !    "
                s.status["fg"] = "red"
            elif p_move == "2":
                s.my += 1
                s.score1["text"] = ":" + str(s.my)
                s.status["text"] = "     YOU WON !       "
                s.status["fg"] = "green"
            elif p_move == "3":
                s.status["text"] = "     IT'S  DIE      "
                s.status["fg"] = "black"
        s.round += 1
        s.score_check()

    def back(s):

        """ back to the lobby  """
        # putting back opponent to normal form
        try:
            s.app.put(s.link + "/" + s.p_key, "inv", "0")
            s.app.put(s.link + "/" + s.p_key, "p_key", " ")
            s.app.put(s.link + "/" + s.p_key, "p_name", " ")
            # making plyer to not  playing
            s.app.put(s.link + "/" + s.my_key, "is_playing", "0")
            s.root.destroy()
            s.old_root.Create_lobby(True)
        except (ConnectionError):
            messagebox.showinfo("WARNING", "No Internet Connection")
            return

    def at_exit(s, handler=0):
        """ removing player from database """
        if (s.my_key):
            try:
                s.app.delete(s.link, s.my_key)
            except (requests.exceptions.ConnectionError):
                messagebox.showinfo("WARNING", "No Internet Connection")
                return
        if( handler):
            s.root.destroy()
        _exit(0)


class Game_lobby:
    def __init__(s):

        s.old_data = {}  # for update player
        s.my_name = ""
        s.my_key = ""
        s.check_running = True
        s.update_running = True
        s.Create_lobby()

    def Create_lobby(s, isback=False):
        """ create lobby"""

        s.root = t.Tk()
        color = "#26006f"
        s.root.wm_resizable(0, 0)
        s.root.configure(bg=color)
        s.root.geometry("590x540+320+30")
        s.root.title("Game Lobby")

        s.lobby_image = t.PhotoImage(file=join(getcwd(), "image", "lobby3.png"))
        s.lobby = t.Label(s.root, image=s.lobby_image, bg=color)
        s.lobby.place(x=0, y=0)

        s.score = t.Label(
            s.root,
            text="Enter your name:",
            font=("arieal", 10, "bold"),
            bg=color,
            fg="yellow",
        )
        s.score.place(x=120, y=120)

        s.reg = t.Button(
            s.root,
            text="Register",
            font=("arieal", 10, "bold"),
            command=s.Register,
            activebackground="#f95d9b",
        )
        s.reg.place(x=390, y=140)

        s.entry = t.Entry(s.root, font=("arieal", 15, "italic"))
        s.entry.place(x=120, y=140)
        s.entry.bind("<Return>", s.Register)

        s.lobby = t.Label(
            s.root,
            text="Choose Player ",
            font=("arieal", 20, "italic"),
            bg=color,
            fg="yellow",
        )
        s.lobby.place(x=150, y=180)

        s.frame = t.Frame(s.root, width=500, height=270, bg="yellow")
        s.frame.place(x=50, y=230)

        s.exit = t.Button(
            s.root,
            text="Exit",
            font=("arieal", 8, "bold"),
            bg="green",
            command=lambda: s.at_exit(1),
            activebackground="#f95d9b",
            width=10,
        )
        s.exit.place(x=250, y=510)

        # at exit handler
        s.root.protocol("WM_DELETE_WINDOW", s.at_exit)
     
        if (isback):
            s.check_running = True
            s.update_running = True

            check_thread = Thread(target=s.check_challange, args=(s.my_key,), daemon=True)
            # creating thread to check for new player in backgroud
            update_thread = Thread(target=s.Update_player, daemon=True)
            
            s.entry.insert(0, s.my_name)
            s.entry["state"] = "disabled"
            #start the thread 
            update_thread.start()
            check_thread.start()

        s.root.mainloop()

    def Register(s, event=None):
        """the player need to register his name in database inorder to play """

        try:
            s.link = "https://pydatabase.firebaseio.com/player"
            s.app = firebase.FirebaseApplication(
                "https://pydatabase.firebaseio.com/", None
            )
            s.my_name = s.entry.get()
            if (s.my_name):
                data = {
                    "name": s.my_name,
                    "is_playing": "0",
                    "p_move": "0",
                    "p_key": "",
                    "inv": "0",
                    "p_name": "",
                }
                my_key = s.app.post(s.link, data)
                # player key
                s.my_key = my_key["name"]
                # creating thread to check challenge in backgroud
                check_thread = Thread(target=s.check_challange, args=(s.my_key,), daemon=True)
                # creating thread to check for new player in backgroud
                update_thread = Thread(target=s.Update_player, daemon=True)
                
                update_thread.start()
                check_thread.start()
                # disable the entry so the player not make spam
                s.entry["state"] = "disabled"
            else:
                messagebox.showinfo("WARNING", "Pleas Enter Your Name ")
                s.entry["state"] = "normal"
                return
        except (ConnectionError):
            messagebox.showinfo("WARNING", "No Internet Connection")
            return

    def Update_player(s):
        """update the lobby """
        # keep running until he start playing
        while( s.update_running):

            try:
                new_data = s.app.get(s.link, "")

            except (ConnectionError):
                messagebox.showinfo("WARNING", "No Internet Connection")
                return
            # if no new player come don't update the lobby
            if (new_data != s.old_data):
                s.old_data = new_data
                if (s.old_data):
                    s.keys_dic = {}
                    s.b = []
                    k = 0
                    x, y = (5, 5)
                    # iterating each person in document
                    for i in s.old_data.keys():
                        # To avoid adding player itself
                        if i != s.my_key:

                            # if the player is not  playing only display him
                            if s.old_data[i]["is_playing"] == "0":
                                # storing the key(unique id) and name in dict
                                s.keys_dic[s.old_data[i]["name"]] = i
                                # adding button to lobby frame
                                s.b.append(
                                    t.Button(
                                        s.frame,
                                        text=s.old_data[i]["name"],
                                        activebackground="#f95d9b",
                                    )
                                )
                                s.b[k].place(x=x, y=y)
                                s.b[k].bind("<Button-1>", s.Invite_player)
                                # spacing between buttons
                                k += 1
                                if x > 380:
                                    x = 5
                                    y += 70
                                else:
                                    x += 70

    def Invite_player(s, event):
        """ invite player to battle  """

        s.check_running = False
        s.update_running = False

        # opponet player key
        p_key = s.keys_dic[event.widget["text"]]
        try:
            result = s.app.get(s.link, p_key + "/is_playing")
        except (ConnectionError):
            messagebox.showinfo("WARNING", "No Internet Connection")
            return
        if( result == "1"):
            messagebox.showinfo("WARNING", "He Is In Battle Feild!!")
            return

        # puting value 1 to invite on opponet player document
        try:
            s.app.put(s.link + "/" + p_key, "p_key", s.my_key)
            s.app.put(s.link + "/" + p_key, "p_name", s.my_name)
            # need to add at last else the name and key not read by opponet
            s.app.put(s.link + "/" + p_key, "inv", "1")
        except (ConnectionError):
            messagebox.showinfo("WARNING", "No Internet Connection")
            return
        # loop is used if he not respond the time out will displayed
        i = 0
        while (i <= 10):

            try:
                result = s.app.get(s.link, p_key + "/is_playing")
                if( result == "1"):
                    s.app.put(s.link + "/" + s.my_key, "is_playing", "1")
                    # geting opponent player name
                    p_name = s.app.get(s.link, p_key + "/name")

                    # destroy the lobby
                    s.root.destroy()
                    
                    game=RPS_Battel(s.my_key, s.my_name, p_key, p_name, s.app, s.link, s)

                # if player reject the battle
                elif( "-1" == s.app.get(s.link, p_key + "/inv")):
                    s.check_running = True
                    s.update_running = True
                    # creating thread to check challenge in backgroud
                    check_thread = Thread(target=s.check_challange, args=(s.my_key,), daemon=True)
                    # creating thread to check for new player in backgroud
                    update_thread = Thread(target=s.Update_player, daemon=True)
                    
                    update_thread.start()
                    check_thread.start()
                    try:
                        s.app.put(s.link + "/" + p_key, "inv", "0")
                        s.app.put(s.link + "/" + p_key, "p_key", " ")
                        s.app.put(s.link + "/" + p_key, "p_name", " ")
                        messagebox.showinfo(
                            "TIME OUT ", "No Response From Player Try Again Later"
                        )
                    

                    except (ConnectionError):
                        messagebox.showinfo("WARNING", "No Internet Connection")
                        return
                else:
                    i += 1

            except (ConnectionError):
                messagebox.showinfo("WARNING", "No Internet Connection")
                return

        # if he not accepting we need to put back normal
        s.check_running = True
        s.update_running = True

        # creating thread to check challenge in backgroud
        check_thread = Thread(target=s.check_challange, args=(s.my_key,), daemon=True)
        # creating thread to check for new player in backgroud
        update_thread = Thread(target=s.Update_player, daemon=True)
        update_thread.start()
        check_thread.start()
        try:
            s.app.put(s.link + "/" + p_key, "inv", "0")
            s.app.put(s.link + "/" + p_key, "p_key", " ")
            s.app.put(s.link + "/" + p_key, "p_name", " ")
            messagebox.showinfo("TIME OUT ", "No Response From Player Try Again Later")

        except (ConnectionError):
            messagebox.showinfo("WARNING", "No Internet Connection")
            return

    def check_challange(s, my_key):
        """checking for any new challenge"""

        invite = "0"
        while (not invite != "0" and s.check_running):

            try:
                # checking is any one invite me to play
                invite = s.app.get(s.link, my_key + "/inv")

            except (ConnectionError):
                messagebox.showinfo("WARNING", "No Internet Connection")
                return

        if (s.check_running):
            # getting oponent player name
            p_name = s.app.get(s.link, my_key + "/p_name")
            p_key = s.app.get(s.link, my_key + "/p_key")
            if(p_name):
               msg = messagebox.askquestion("BATTLE", "Would like To Accept Challenge From  " + p_name)
            if (msg.lower()== "yes"):
                s.check_running = False
                s.update_running = False
                try:
                    s.app.put(s.link + "/" + my_key, "is_playing", "1")
                    # putting our name ,key ,name on his document
                    s.app.put(s.link + "/" + p_key, "p_key", s.my_key)
                    s.app.put(s.link + "/" + p_key, "p_name", s.my_name)
                    # getting opponent player key
                    p_key = s.app.get(s.link, my_key + "/p_key")
                    s.root.destroy()
                    # starting battle  ground
        
                    game=RPS_Battel(s.my_key, s.my_name, p_key, p_name, s.app, s.link, s)

                except (ConnectionError):
                    messagebox.showinfo("WARNING", "No Internet Connection")
                    return
            elif msg == "no":
                try:
                    # if player reject to play put inv is -1
                    s.app.put(s.link + "/" + my_key, "inv", "-1")
                except (ConnectionError):
                    messagebox.showinfo("WARNING", "No Internet Connection")
                    return
            

    def at_exit(s, handler=0):
        """ removing player from database"""

        if s.my_key:
            try:
                s.app.delete(s.link, s.my_key)
            except (ConnectionError):
                messagebox.showinfo("WARNING", "No Internet Connection")
                return
            if handler == 1:
                s.root.destroy()
        s.check_running = False
        s.update_running = False
        _exit(0)


Game_lobby()

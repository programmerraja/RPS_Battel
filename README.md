# RPS_Battel
This is multiplayer game using firebase database 

# how this work ?
  <p> first it ask user to register the player by entering his name and the player  details are  send to database to stored <br>
 <prev>
  the data is 
  
  data = {
                    "name": s.my_name, #player name 
                    "is_playing": "0",  #used to check if player is playing 
                    "p_move": "0",   # player move which weapon the player is choosed (1-scssisor 2-rock 3-papper) 
                    "p_key": "",   #a unique key to identified the player
                    "inv": "0",   # if any player invite him to play mean it change  to 1
                    "p_name": "",   # this name for the opponent player name  
                }
  </prev>
</p>
<p> After player registerd sucess the online player name are shown in text area player need to select any one to battle </p>
<p> in background the two thread are created. one thread constantly checking if   player has any invite .second thread constantly 
# what are thing i learn from it ?
    <ul>
    <li> Firebase <p> To store the user move in database such that it can be acess by other player </p></li> 
    <li> Threading <p> To get the oppent move from the firbase database threading is used so the game won't get interupted </p> </li>
    </ul>
    




![preview](image/img1.png)


![preview2](image/img2.png)



External module required <br>
 1.Requests <br>
 2.Firebase-python
 

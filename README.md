# RPS_Battel
This is multiplayer game using firebase database 

# how this work ?
  <p> First it ask user to register the player by entering his name and the player  details are  send to database to stored </p>
 <prev>
  the data is 

  data = {
                    "name": s.my_name, #player name 
                    "is_playing": "0",  #used to check if player is playing 
                    "p_move": "0",   # player move which weapon the player is choosed (1-scssisor 2-rock 3-papper) 
                    "p_key": "",   #a unique key to identified the opponent player
                    "inv": "0",   # if any player invite him to play mean it change  to 1
                    "p_name": "",   # this name for the opponent player name  
                }
  </prev>
  <br>
<p> After player registerd sucess the online player name are shown in text area player need to select any one to battle </p>
<p> In background the two thread are created. one thread constantly checking if   player has any invite .second thread constantly  checking any player came to play by checking the database </p>
<p> If player1 select player2 to battle then the player2 data <b>inv</b> is changed to 1 by using the opponent unique key and the player1 name is add to player2 data <b> p_name:player1 </b> after player2 get notification that tell that player1 like to battle with you would llike to accept his invite 
if he accept the both player get in to the lobby to play </p>
<p> how the player1 know that player2 know 
</p>
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
 

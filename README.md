# Mandatory assignment in the course INF142 Networking 

## Group 98

Members: Tobias Sagvaag Kristensen (tkr048@uib.no)



## Prerequisites

    git clone https://github.com/Tobbelobby/Oblig.git
    pip install -r requirements.txt



## How to Play

Start the by running server.py, then run the db.py. Wait until the server is outputting "DB". After this you can start the player.py.

As for now the game is on the localhost, open 4 terminal. CD to the Game folder and type ./server.py. In the second terminal type ./bd.py, for the remanding two terminal ./player.py. You can run more player.py instances, but the program wil only run one game at a time. But after the game is done, the new game instance will start. 

## For the next iteration 

As for now there are little to non error handling, i tried to implement timout, but to no lock. 
Making the server run multiple game is also something for the next iteration. Also a way to close the server and the db in a more elegant way than CTRL C.  

## DB

The DB is two files (some_champs.txt and db.json), the game is dependent on both files. "some_...." store the champs, and db.py lodes the champs, and send it to the server. db.json sore game stats like match history, champs stats and total score for red and blue team.   

## Task 

Hi there! Have you played our brand new game? It is called Team Local Tactics and
it is available here. So far, we have only managed to develop a local version, but users
are asking for more features. They want to be able to play online or versus an AI and, of
course, they also want more champions. Our user base is asking for more than we can
handle at the moment. However, with your help, we believe we can transform TLT into
a distributed application. In doing so, we can finally change its name to Team Network
Tactics, which obviously is good branding. So, are you up for the job?
We think TNT should consist of three processes that communicate with each other
over the Internet:
    • A database for storing champions and stats.
    • A server running the logic of the game.
    • A client for the players.
This architecture would allow us to patch champions (nerf or buff) while players are
still playing the game; and to place our servers close to our users, see Figure 1.
We thank you in advance for your help and politely ask you to send us a minimum
viable product (MVP) of TNT no later than 11.03.2022.

You will count on the extremely valuable support of two of our tech leads (your
mentor TAs) and, from time to time, you can also request the service of our Head of
Silly Names (the course instructor).

   Your application will be considered a MVP if it fulfills all of the following requirements:
    • It consists of at least three Python scripts, one for each of the aforementioned
    processes.
    • Socket programming is used.
    • Data associated to champions, match history or other stats must persist in a database
    or in a file.
The three processes can run, without any isolation, in the same device by using localhost. Note that this is the minimum you have to accomplish. Of course, your tech leads encourage to do more.

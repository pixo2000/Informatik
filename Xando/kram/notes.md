# Das Game
### Idee:
- Ein game das online und offline läuft(Kommt auf den PC an und ob er gerade online ist)
- Autovpn damit es in der schule läuft
- Maybe browserversion

- Einfacher 2d Shooter
- Main GUI: customtkinter
- Game: pygame

## Server:
- Port: 52983

### Errors:
- Crash when moving GUI while in game

### Jetzt:
- Movement senden, empfangen, brodcasten und rendern

- Gui dark mode always users have no choice
- accounts -> nametags
- Teams
- Clients auf demselben server


### Aktuell:
- servergui
- maybe live map reload/map maker
- mehr blöcke(nur für ein team etc)
- esc menu/quit with esc
- movement with w+a to yeah
- check maps on client no desync
- map is too small
- add running(standart, when aiming/holding shift 50% speed) 
- make game bigger
- better design for gui
- grafiken

### Morgen:
- Maps by server
- HP-System
- offline option to explore map
- nametags

# Die tage:
- teams
- ping with name and serverconsole to dc webhook
- console tells you type(game start/ping)
- login system


### Idk how:
- add close gui also quits game


### Ziel bis weinachten:
- Es funktioniert ohne bugs
- 3 Modi: Duel, Team(3v3&5v5), Battle Royale
- Party System
- 5 Maps
- Login system
- 5 Waffen
- Anticheat
- Bessere Grafiken
- Server
- Leaderboard
- Chat
- Shop
- Customization
- Borderless
- Codes im Store
- Settings(Grafik und steuerung)


#### Danach:
- Echtgeld
- Mehr Waffen
- Mehr Maps
- Discord RPC
- Mobile Version
- Browser Version ohne Login mit autovpn


### ganz viel später:
- version für nintendo switch und net nur cracked switch(PS3 incomming?)




i have game.py and the stuff in the server folder. please ass the following things: clients can join the server and see other clients. the server uses their usernames as userid's for sending the information on where wich player moves. then add a basic map. modify each file how its needed and use for example for the map another file so later i can create other maps just in a single file. after this, connect the camera to the local player. the map should have some blocks and a woldborder. to tell the server the username, you also need to make a small login screen with the user features from the server before starting the game. always send me the entire finished file
### Ziel: Server connection
- [ ] Client Login  
- Server database check
- Client interface
- pass information to the game :skull:<br>
<br>
- [ ] Client Rendering -> Map ertellen  


 Server:
- Bei der Login request wird eine HWID mitgeschickt. 
- Aus HWID, Username und Passwort wird ein 24h gültiger authcode erstellt der dem Client geschickt wird
- Der client schickt den authcode beim gamestart in kombi mit modusnamen
- nur die passende HWID kann sich mit dem authcode einloggen
- bei jedem clientstart checkt  er ob der authcode noch gültig is. wenn net nochmal anmelden
- bei einem neuen login wird der alte authcode ungültig gemacht
- authcode wird eif in ner config gesaved oda so


- admin command zum sperren von HWID's und Accounts
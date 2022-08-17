
# TCP/IP Client S/W for TEST M487Board
## Index
  - [Preview](#preview)
  - [Description](#description)
  - [Enviorment](#enviorment) 
  - [Reference](#reference)
  
## Preview
![image](https://user-images.githubusercontent.com/108905975/185076644-5a706416-440b-4897-b0f5-a042e579fbd3.png)

## Description
<!--Wirte one paragraph of project description -->  
- First.therad  : Add hot key F4: START F5 : STOP  
- Second.thread : As TCP/IP Client role send key data to Server  
- Third.thread  : As Key Hooker send pressed key data to Second.thread   

## Enviorment
<!-- Write enviromnet about this project -->
- Python : 3.10.5 
- Library : pyautogui 
```
pip install pyautogui
```

## Reference
<!-- Write the way to contribute -->
 - (https://yhkim4504.tistory.com/2) - Client Side Daemon thread
 - (https://webnautes.tistory.com/1381) - Python Socekt Commuinication 

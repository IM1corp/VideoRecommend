#Finding similar anime/films using users votes
#### This project uses python <a href="https://github.com/benfred/implicit">implicit</a> library to build model and predict data
In original , this project used to run on **Windows**. It **should**(probably) run on linux, but author didn't test it
##How to run this code
1) Install dependencies using command `pip install -r requirements.txt`
<br>P.S. if you want to use GPU version - install implicit using conda: `conda install -c conda-forge implicit implicit-proc=*=gpu`
2) Configure environment - create `.env` file and put in it next code:
```commandline
YUMMY_SECRET=SuperSecretServerSecter           # secret parameter
YUMMY_API_URL=https://example.com/server/url   # server url
TRAIN_FACTORS=50                               # model train facors
```
3) If you want this script to be executed every hour/day/week (on Windows) - configure Task Scheduler [main.bat](main.bat).

If you want to use custom python version - edit [main.bat](main.bat) first argument

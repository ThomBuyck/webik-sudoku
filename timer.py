def timer():
    import time
    Sec = 0
    Min = 0
    while Min < 10:
        Sec += 1
        print(str(Min) + " Minuten en " + str(Sec) + " Seconden ")
        time.sleep(1)
        if Sec == 60:
            Sec = 0
            Min += 1
            print(str(Min) + " Minute")
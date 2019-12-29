from datetime import datetime


def logError(error):
    file1 = open("log.txt","a")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    file1.write('[ ' + str(current_time) + ' ]   ' + error + '\n')
    file1.close()
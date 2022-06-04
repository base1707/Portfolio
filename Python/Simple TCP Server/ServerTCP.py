import socket
import re

##########################################
## CONSTANTS
##########################################

# Using PrintError(...) and PrintMessage(...) functions
DEBUG_MESSAGES = True

# Regex: BBBBxNNxHH:MM:SS.zhqxGGCR
INPUT_REGULAR = r"[0-9]{4}\s[A-Z0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}\s[A-Z0-9]{2}"

##########################################
## SUPPORT FUNCTIONS 
##########################################

def PrintError(message):
    if DEBUG_MESSAGES == True:
        print(f"[!] {message}")

def PrintMessage(message):
    if DEBUG_MESSAGES == True:
        print(f"[#] {message}")

##########################################
## SERVER
##########################################

class CServerTCP:
    def __init__(self, SOCKET_HOST, SOCKET_PORT):
        # Log file
        try:
            self.logFile = open("log.txt", "w")
        except Exception as ex:
            PrintError(f"Filesystem error: {ex}")
            raise(ex)

        # Socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as ex:
            PrintError(f"Filesystem error: {ex}")
            raise(ex)

        try:
            self.socket.bind((SOCKET_HOST, SOCKET_PORT))
        except:
            PrintError(f"Port binding failed: {SOCKET_HOST}:{SOCKET_PORT}")
            raise(ex)

        # Start server: 1 client (demo mode)
        self.socket.listen(1)

        # Create a connection
        self.connection, self.connectionIP = self.socket.accept()
        PrintMessage(f"Connected: {self.connectionIP}")

    def __del__(self):
        if self.connection:
            self.connection.close()

        if self.logFile and self.logFile.closed == False:
            self.logFile.close()

    # Write string to log-file
    def WriteLog(self, message):
        if self.logFile and self.logFile.closed == False:
            self.logFile.write(message + "\r")

    def Work(self):
        if not self.connection:
            return

        while True:
            # Get a byte array (1KB)
            if data := self.connection.recv(1024):
                # Stop server
                if not data:
                    break

                self.ParseData(data)

                # Manual exit
                if data.find(b"exit") > 0:
                    break

    def ParseData(self, data):
        if data:
            match = re.findall(INPUT_REGULAR, str(data).strip())
            for i in match:
                source = str(i)
                s_number = source[0:4]
                s_id = source[5:7]
                s_time = source[8:16]
                s_time_additional = source[17:20]
                s_group = source[21:23]

                m = f"Спортсмен, нагрудный номер {s_number} прошёл отсечку {s_id} в время {s_time}"
                self.WriteLog(f"{m}.{s_time_additional}")
                if (s_group == "00"):
                    print(m)


##########################################
## ENTRY POINT
##########################################

def main():
    # 4demo: run on localhost:9090
    Server = CServerTCP("", 9090)
    Server.Work()
    del Server

# EntryPoint
if __name__ == "__main__":
    main()
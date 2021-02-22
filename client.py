# Import socket module
import socket

def printinfo(m,lifes): # a helping function just to print conveniently the infos that server has sended.
    word=""
    for c in m: word+=c+" "
    print(f"{word} ({lifes} lifes remain)")


def main():

    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect
    port = 12345

    # connect to the server on local computer
    s.connect(('127.0.0.1', port))

    while True:  # a loop until the game is over

        # receive data from the server
        lifes = s.recv(1024)
        hidden_word = s.recv(1024).decode()
        printinfo(hidden_word, lifes[0])

        if lifes[0] == 0 or (not "_" in hidden_word):  # if one of these conditions are true the game has ended
            break

        c = input("Give a character: ")  # client trying to guess a letter in the hidden word
        s.send(c.encode())

    print(f"The correct word is {s.recv(1024).decode()}")  # server informs client for the correct word
    if lifes[0] > 0:
        print("You win")
    else:
        print("You lose")

    # close the connection
    s.close()


if __name__ == "__main__":
    main()
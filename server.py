# first of all import the socket library
import socket
import random


def Edit(word): # splitting all the words in a sentence.
    return word.translate({ord(i): None for i in ",."}).split(" ")

def main():
    # creating a socket object
    s = socket.socket()
    print("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 12345

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print("socket binded to %s" % (port))

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
    # random sentence that each word will be seperated and server will choose one randomly
    dictionary = Edit(
        "It seems likely that this character will never get Devil Fruit. "
        "Aside from it being unnecessary for his character, it would be very trite and boring to see any more o"
        "f the crew suddenly gain Devil Fruit abilities."
        " It just furthers the strength of crew seeing them get as far as they "
        "are without the need of superhuman powers.")

    index_of_word = random.randint(0, len(dictionary) - 1)  # the (index_of_word+1)th word of the dictionary is selected

    hiding_word = dictionary[index_of_word][0]  # the first letter is known
    hiding_word += "_" * (len(dictionary[index_of_word]) - 1)  # all the others are hiding.
    hiding_word = list(hiding_word)

    UnFoundLetters = [True for i in range(
        len(hiding_word))]  # every index of letter that client has not found has UnfoundLetters[index]=True
    UnFoundLetters[0] = False  # because the first letter is already known

    # if the chosen word has more than 4 letters the last letter will be provided
    if (len(hiding_word) > 4):
        hiding_word[-1] = dictionary[index_of_word][-1]
        UnFoundLetters[-1] = False  # now and the last letter is known
    lifes = len(hiding_word) # the chances for the client to find the word correct

    # Establish connection with client.
    c, _ = s.accept()
    print("The client has started to play")
    c.send(bytes([lifes]))  # sending his lifes
    c.send("".join(hiding_word).encode())  # the starting info for the hiding word

    while (not ("".join(hiding_word) == dictionary[index_of_word]) and lifes > 0):
        letter = c.recv(1024).decode()
        false_guess = True  # this variable represents if the client did a wrong guess

        for i in range(len(dictionary[index_of_word])):
            if dictionary[index_of_word][i] == letter and UnFoundLetters[i]:
                UnFoundLetters[i] = False  # now an extra letter is found from client
                hiding_word[i] = letter
                false_guess = False  # client picked it up correct this time

        if (false_guess): lifes -= 1  # this means client did a wrong guess so he has to lose 1 life.
        # sending the updated infos to client
        c.send(bytes([lifes]))
        c.send("".join(hiding_word).encode())

    c.send(dictionary[index_of_word].encode())  # sendint to client the hidden word

    if lifes > 0:
        print("Client won")
    else:
        print("Client lost")

    # Close the connection with the client
    c.close()


if __name__ == "__main__":
    main()



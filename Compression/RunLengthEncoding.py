def encode(message: str) -> str:
    i, occorCounter, letter, newMessage = 0, 1, '', ''
    while i < len(message)-1:
        letter = message[i]
        try:
            while letter == message[i+1]:
                occorCounter = occorCounter + 1
                i = i+1
                try:message[i+1]
                except:break
            else:i=i+1
        except Exception:i=i+1
        newMessage = newMessage + str(occorCounter) + letter
        occorCounter = 1
    if len(message) == 1:newMessage = "1" + message

    return newMessage

def decode(encodedMessage:str) -> str :
    DecodedMessage = ""
    for i in range(0,len(encodedMessage),2):
        try : 
            for _ in range(1,int((encodedMessage[i]))):DecodedMessage = DecodedMessage + encodedMessage[i+1]
        except Exception: 
            break
    return DecodedMessage 

if __name__ == "__main__":
    message = input("What is your message\n")
    print(f"{message = }")
    encodedMessage = encode(message)
    print(f"{encode(message) = }")
    print(f"{decode(encodedMessage) = }")

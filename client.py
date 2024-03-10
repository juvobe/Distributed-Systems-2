import xmlrpc.client
import datetime

while True:
    try:
        s = xmlrpc.client.ServerProxy('http://localhost:8000')
        print("1. Add note")
        print("2. Get notes")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            topic = input("Enter the topic: ")
            if not topic:
                print("Topic can't be null.")
                continue
            note_name = input("Enter the note name: ")
            text = input("Enter the text: ")
            timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print("Note added", s.add_note(topic, note_name, text, timestamp))
        elif choice == '2':
            topic = input("Enter the topic: ")
            print("Notes: ", s.get_notes(topic))
        elif choice == '0':
            break
        else:
            print("Incorrect input")
    except ConnectionRefusedError:
        print("Unable to connect to the server.")
        break
    except xmlrpc.client.ProtocolError as e:
        print(f"Protocol error: {e}")
        break
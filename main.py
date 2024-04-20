from smartcard.System import readers
from smartcard.util import toHexString

def read_card_data():
    # Get all the available readers
    card_readers = readers()
    if not card_readers:
        print("No card readers found")
        return

    print("Available readers:", card_readers)

    # Use the first available reader
    reader = card_readers[0]
    print("Using reader:", reader)

    try:
        # Connect to the card
        connection = reader.createConnection()
        connection.connect()

        # Command to get the UID of the NFC card
        # This is a standard command for ISO14443A cards to get the UID
        get_uid_command = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        data, sw1, sw2 = connection.transmit(get_uid_command)

        if sw1 == 0x90 and sw2 == 0x00:
            print("Success: Card UID is", toHexString(data))
        else:
            print("Failed to read card UID")

    except Exception as e:
        print("Failed to connect to the card:", str(e))

if __name__ == "__main__":
    read_card_data()

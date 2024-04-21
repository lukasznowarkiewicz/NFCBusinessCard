from smartcard.System import readers
from smartcard.util import toHexString, toBytes

def send_custom_command():
    # Get all available card readers
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

        while True:
            # Get user input for hex command
            hex_command = input("Enter the hex command to send (or type 'exit' to quit): ")
            if hex_command.lower() == 'exit':
                print("Exiting program.")
                break

            try:
                # Convert the hex command to bytes
                command = toBytes(hex_command)
                # Transmit the command to the card
                data, sw1, sw2 = connection.transmit(command)
                # Print the card's response
                print("Card response:", toHexString(data), "Status words:", "%02X %02X" % (sw1, sw2))
            except Exception as e:
                print("Error sending command:", str(e))

    except Exception as e:
        print("Failed to connect to the card:", str(e))

if __name__ == "__main__":
    send_custom_command()

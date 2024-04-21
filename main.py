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
            # Get user input for hex command or action
            user_input = input("Enter the hex command to send, type 'read_ndef' to read NDEF data, or type 'exit' to quit: ")
            if user_input.lower() == 'exit':
                print("Exiting program.")
                break
            elif user_input.lower() == 'read_ndef':
                print("Reading NDEF data...")
                ndef_content = read_ndef(connection)
                if ndef_content:
                    print("NDEF Data Read from the Card:", ndef_content)
                continue

            try:
                # Convert the hex command to bytes and transmit to the card
                command = toBytes(user_input)
                data, sw1, sw2 = connection.transmit(command)
                print("Card response:", toHexString(data), "Status words:", "%02X %02X" % (sw1, sw2))
            except Exception as e:
                print("Error sending command:", str(e))

    except Exception as e:
        print("Failed to connect to the card:", str(e))

def read_ndef(connection):
    try:
        result_string = ""
        page = 4
        end_of_ndef = False

        while not end_of_ndef:
            command = [0xFF, 0xB0, 0x00, page, 0x10]
            data, sw1, sw2 = connection.transmit(command)
            if sw1 == 0x90 and sw2 == 0x00:
                readable_data = ''.join(chr(x) if 32 <= x <= 126 else '' for x in data)
                result_string += readable_data
                if 0xFE in data:
                    end_of_ndef = True
            else:
                print("Failed to read data at page", page)
                break
            page += 4
        return result_string.strip()

    except Exception as e:
        print("An error occurred while reading NDEF data:", str(e))
        return None

if __name__ == "__main__":
    send_custom_command()

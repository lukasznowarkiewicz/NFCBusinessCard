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
        # Read capability container at page 3 to confirm if NDEF data is present
        command = [0xFF, 0xB0, 0x00, 0x03, 0x10]  # Read 16 bytes starting from page 3
        data, sw1, sw2 = connection.transmit(command)
        if sw1 != 0x90 or sw2 != 0x00:
            print("Failed to read capability container or no NDEF data.")
            return None

        # Checking NDEF Magic Number
        if data[0] != 0xE1:
            print("No NDEF data present.")
            return None
        
        # Calculate total NDEF pages (assuming typical page size is 4 bytes)
        total_pages = (data[2] * 8) // 4  # Convert from total memory size to total pages
        result_string = ""

        # Read the NDEF data from the card
        page = 4  # Start reading from page 4
        while page < total_pages:
            command = [0xFF, 0xB0, 0x00, page, 0x10]
            data, sw1, sw2 = connection.transmit(command)
            if sw1 == 0x90 and sw2 == 0x00:
                # Process each byte in the data
                for byte in data:
                    if byte == 0xFE:
                        # NDEF record terminator found
                        return result_string.strip()
                    if 32 <= byte <= 126:
                        result_string += chr(byte)
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

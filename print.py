import serial
import barcode
from barcode.writer import ImageWriter
import os
import win32print  # For Windows printing
import time

# Open the serial connection to the Arduino
arduino = serial.Serial('COM3', 9600, timeout=1)

def generate_and_print_barcode(barcode_data):
    # Generate a barcode image
    barcode_format = barcode.get_barcode_class('code128')  # Use Code 128 barcode format
    barcode_image = barcode_format(barcode_data, writer=ImageWriter())

    # Save the barcode image to a temporary file
    temp_file = "temp_barcode"
    barcode_image.save(temp_file)

    # Add the file extension (.png)
    barcode_file = f"{temp_file}.png"

    # Print the barcode using the default printer
    try:
        printer_name = win32print.GetDefaultPrinter()  # Get the default printer name
        print(f"Printing to: {printer_name}")

        # Open the printer and send the file to it
        printer_handle = win32print.OpenPrinter(printer_name)
        job_id = win32print.StartDocPrinter(printer_handle, 1, ("Barcode Print Job", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)

        with open(barcode_file, "rb") as f:
            raw_data = f.read()
            win32print.WritePrinter(printer_handle, raw_data)

        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
        win32print.ClosePrinter(printer_handle)

        print("Barcode printed successfully!")
    except Exception as e:
        print(f"Error printing barcode: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(barcode_file):
            os.remove(barcode_file)

def main():
    while True:
        # Check for incoming data from the Arduino
        if arduino.in_waiting > 0:
            response = arduino.readline().decode('utf-8').strip()

            # Check if the response contains barcode data
            if "Barcode Data:" in response:
                # Extract the barcode data
                barcode_data = response.split(":")[1].strip()
                print(f"Received barcode data: {barcode_data}")

                # Generate and print the barcode
                generate_and_print_barcode(barcode_data)


def main():
    while True:
        try:
            # Check for incoming data from the Arduino
            if arduino.in_waiting > 0:
                response = arduino.readline().decode('utf-8').strip()

                # Check if the response contains barcode data
                if "Barcode Data:" in response:
                    # Extract the barcode data
                    barcode_data = response.split(":")[1].strip()
                    print(f"Received barcode data: {barcode_data}")

                    # Generate and print the barcode
                    generate_and_print_barcode(barcode_data)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        arduino.close()

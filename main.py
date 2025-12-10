from reader.keyboard_qr_reader import KeyboardQRReader
from api.api_client import APIClient


def on_qr_scanned(qr_value):

    api.submit({"qr_code": qr_value})

    print("📟 QR Scanned:", qr_value)


if __name__ == "__main__":

    # Initialize API client
    api = APIClient(api_url="https://127.0.0.1:5000/api/submit")

    # Initialize QR scanner with callback
    reader = KeyboardQRReader(callback=on_qr_scanned)
    reader.start()
    print("⌨️ QR Scanner is running. Press Ctrl+C to stop.")

    try:
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        reader.stop()
        print("🛑 Program terminated by user.")
        api.close()

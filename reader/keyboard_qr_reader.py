import sys
import threading

class KeyboardQRReader:


    def __init__(self, callback=None):
        self.buffer = ""
        self.callback = callback
        self.running = False

    def _reader(self):
        """Internal thread to read characters from console"""
        while self.running:
            char = sys.stdin.read(1)

            if char in ["\n", "\r"]:
                scanned = self.buffer.strip()
                self.buffer = ""

                if scanned:
                    if self.callback:
                        self.callback(scanned)
            else:
                self.buffer += char

    def start(self):
        """Start listening for QR scans"""
        self.running = True
        t = threading.Thread(target=self._reader, daemon=True)
        t.start()
        print("⌨️ Keyboard QR reader started...")

    def stop(self):
        """Stop listening"""
        self.running = False
        print("🛑 Keyboard QR reader stopped.")

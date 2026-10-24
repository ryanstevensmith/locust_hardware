import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports
import esptool
import io
import contextlib
import threading
import os, sys

FIRMWARE_FILE = "firmware.bin"
BOOTLOADER_FILE = "bootloader.bin"
PARTITIONS_FILE = "partitions.bin"

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return filename

def list_serial_ports():
    return [p.device for p in serial.tools.list_ports.comports()]

def flash_device():
    port = port_var.get()
    if not port:
        messagebox.showwarning("No Port", "Please select a COM port.")
        return

    # Start flashing in a background thread
    threading.Thread(target=run_esptool, args=(port,), daemon=True).start()

def run_esptool(port):
    args = [
        "--chip", "esp32s3",
        "--port", port,
        "--baud", "460800",
        "write_flash", "-z",
        "0x0", BOOTLOADER_FILE,
        "0x8000", PARTITIONS_FILE,
        "0x10000", FIRMWARE_FILE
    ]

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"Flashing to {port}...\n\n")
    root.update()

    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            try:
                esptool.main(args)
                success = True
            except SystemExit as e:
                success = e.code == 0

        output = buf.getvalue()
        text_output.insert(tk.END, output)

        if success:
            root.after(0, lambda: messagebox.showinfo("Success", "Firmware flashed successfully!"))
        else:
            root.after(0, lambda: messagebox.showerror("Flashing Failed", "esptool reported an error.\nSee log below."))

    except Exception as e:
        output = f"\n[EXCEPTION]: {str(e)}\n"
        text_output.insert(tk.END, output)
        root.after(0, lambda: messagebox.showerror("Unexpected Error", str(e)))



def refresh_ports():
    port_combo['values'] = list_serial_ports()

# GUI setup
root = tk.Tk()
root.title("Locust Firmware Updater v0.5.2")
root.geometry("500x400")
root.iconbitmap(resource_path("updater.ico"))

ttk.Label(root, text="Select COM Port:").pack(pady=5)
port_var = tk.StringVar()
port_combo = ttk.Combobox(root, textvariable=port_var, values=list_serial_ports(), state='readonly')
port_combo.pack(pady=5)

ttk.Button(root, text="Refresh Ports", command=refresh_ports).pack(pady=5)
ttk.Button(root, text="Flash Firmware", command=flash_device).pack(pady=10)

text_output = tk.Text(root, height=15, wrap='word')
text_output.pack(padx=10, pady=10, fill='both', expand=True)

root.mainloop()

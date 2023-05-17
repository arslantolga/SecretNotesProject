import tkinter
from PIL import Image, ImageTk
from cryptography.fernet import Fernet

storage_encrpyt = []
storage_masterkey = []
storage_genkey = []

def save_encrypt():
    global storage_encrpyt
    global storage_genkey
    global storage_masterkey
    global f
    key = Fernet.generate_key()
    f = Fernet(key)
    input_title = title_entry.get()
    masterkey = masterkey_entry.get()
    entered_text = secret_textbox.get("1.0", tkinter.END)
    encrypt_string = f.encrypt(entered_text.encode())
    secret_textbox.delete("1.0", tkinter.END)
    title_entry.delete(0, tkinter.END)
    masterkey_entry.delete(0,tkinter.END)

    if input_title == "" or masterkey == "":
        print_label.config(text="Enter Title and Master Key!",font=FONT,pady=10)
        print_label.pack()

    else:
        storage_encrpyt.clear()
        storage_genkey.clear()
        storage_masterkey.clear()
        print_label.config(text="Successful!",font=FONT,pady=10)
        print_label.pack()
        with open('mysecret.txt', "a+", encoding='UTF-8') as f:
            f.write(input_title + '\n' + encrypt_string.decode() + '\n')
        with open('mysecret.txt', "r", encoding='UTF-8') as f:
            f.seek(0)
            icerik = f.read()
            kelimeler = icerik.split()
            for indeks, value in enumerate(kelimeler):
                if indeks % 2 != 0:
                    storage_encrpyt.append(value)

        with open('venv/Scripts/passwords.txt', "a+", encoding='UTF-8') as f:
            f.write(masterkey + '\n' + key.decode() + '\n')
        with open('venv/Scripts/passwords.txt', "r", encoding='UTF-8') as f:
            f.seek(0)
            icerik = f.read()
            kelimeler = icerik.split()
            for indeks, value in enumerate(kelimeler):
                if indeks % 2 == 0:
                    storage_masterkey.append(value)
                else:
                    storage_genkey.append(value)

def decrypt():
    entered_text = secret_textbox.get("1.0", tkinter.END)
    entered_text = entered_text.split()
    masterkey = masterkey_entry.get()
    storage_encrpyt.clear()
    storage_genkey.clear()
    storage_masterkey.clear()
    try:
        with open('mysecret.txt', "r", encoding='UTF-8') as f:
            f.seek(0)
            icerik = f.read()
            kelimeler = icerik.split()
            for indeks, value in enumerate(kelimeler):
                if indeks % 2 != 0:
                    storage_encrpyt.append(value)

        with open('venv/Scripts/passwords.txt', "r", encoding='UTF-8') as f:
            f.seek(0)
            icerik = f.read()
            kelimeler = icerik.split()
            for indeks, value in enumerate(kelimeler):
                if indeks % 2 == 0:
                    storage_masterkey.append(value)
                else:
                    storage_genkey.append(value)

        if entered_text[0] in storage_encrpyt:
            indeks_encrpyt = storage_encrpyt.index(entered_text[0])
            if masterkey == storage_masterkey[indeks_encrpyt]:
                a = storage_genkey[indeks_encrpyt]
                b = storage_encrpyt[indeks_encrpyt]
                f = Fernet(a.encode())
                original_str = f.decrypt(b.encode()).decode()
                secret_textbox.delete("1.0", tkinter.END)
                secret_textbox.insert(tkinter.END, f"{original_str}")
                print_label.config(text="Successful!", font=FONT, pady=10)
                print_label.pack()

            else:
                print_label.config(text="Unmatched Master Key!", font=FONT, pady=10)
                print_label.pack()
        else:
            print_label.config(text="Encrypting string not found!", font=FONT, pady=10)
            print_label.pack()

    except:
        print_label.config(text="File not found!", font=FONT, pady=10)
        print_label.pack()

window = tkinter.Tk()
window.title("Secret Notes")
window.geometry("380x650")

myImage = ImageTk.PhotoImage(Image.open("images.png"))

FONT = ("Arial", 15)

image_label = tkinter.Label(image=myImage)
image_label.pack()

title_label = tkinter.Label(text="Enter your title",font=FONT,pady=10)
title_label.pack()

title_entry = tkinter.Entry(window)
title_entry.pack()

secret_label = tkinter.Label(text="Enter your secret",font=FONT,pady=10)
secret_label.pack()

secret_textbox = tkinter.Text(window,width=25,height=10)
secret_textbox.pack()

masterkey_label = tkinter.Label(text="Enter master key",font=FONT,pady=10)
masterkey_label.pack()

masterkey_entry = tkinter.Entry(window)
masterkey_entry.pack()

scape_label = tkinter.Label(text="",pady=0.01)
scape_label.pack()

save_button = tkinter.Button(text="Save & Encrypt",command=save_encrypt)
save_button.pack()

scape_label = tkinter.Label(text="",pady=0.01)
scape_label.pack()

decrypt_button = tkinter.Button(text="Decrypt",command=decrypt)
decrypt_button.pack()

print_label = tkinter.Label(text="")
print_label.pack()

window.mainloop()

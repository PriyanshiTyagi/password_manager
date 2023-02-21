import json
from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip


# ---------------------------- PASSWORD SEARCH ------------------------------- #
def search_password():
    try:
        with open("passwords.json") as file:
            file_data = json.load(file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"No data file found.")
    else:
        try:
            website = website_entry.get()
            password = file_data[website]["password"]
            email = file_data[website]["email"]
        except KeyError:
            messagebox.showinfo(title="Error", message=f"No details for the website exists.")

        else:
            messagebox.showinfo(title=website, message=f"Email:{email}\n Password: {password}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generate():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password = []
    password += [choice(letters) for x in range(randint(8, 10))]
    password += [choice(numbers) for x in range(randint(2, 4))]
    password += [choice(symbols) for x in range(randint(2, 4))]

    shuffle(password)
    password = "".join(password)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="OOPS", message="You left some field empty..!")
    else:
        message = messagebox.askokcancel(title=website, message=f"These are the details you entered\n"
                                                                f"Email:{email}\n"
                                                                f"Password:{password}\n"
                                                                f"Is it okay to save?")
        if message:
            try:
                with open("passwords.json", "r") as file:
                    # reading old data
                    data = json.load(file)
                    # updating data with new data
                    data.update(new_data)

            except FileNotFoundError:
                with open("passwords.json", "w") as file:
                    json.dump(new_data, file, indent=4)

            else:
                with open("passwords.json", "w") as file:
                    # saving the updated data
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_entry = Entry(highlightthickness=2, highlightcolor="#31E1F7")
website_entry.grid(row=1, column=1, sticky="EW")
website_entry.focus()

email_entry = Entry(width=35, highlightthickness=2, highlightcolor="#31E1F7")
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(END, "bam@gmail.com")

password_entry = Entry(width=21, highlightthickness=2, highlightcolor="#31E1F7")
password_entry.grid(row=3, column=1, sticky="EW")

generate_button = Button(text="Generate Password", command=password_generate)
generate_button.grid(row=3, column=2, sticky="EW")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=search_password)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()

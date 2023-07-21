import random
import string
from rich.console import Console
import pyperclip
import mysql.connector

def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def save_to_database(sitename, username, password):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword",
        database="password_manager"
    )
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO passwords (sitename, username, password)
        VALUES (%s, %s, %s)
    """, (sitename, username, password))
    connection.commit()
    connection.close()

def view_passwords(sitename):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword",
        database="password_manager"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM passwords WHERE sitename = %s", (sitename,))
    password = cursor.fetchone()
    connection.close()

    if not password:
        print(f"No password found for sitename: {sitename}")
    else:
        pyperclip.copy(password[0])  # Copy the password to the clipboard
        console.print(f"[green]Password for {sitename}: {password[0]}[/green]")
        console.print("[bold cyan]Copied to clipboard![/bold cyan]")

if __name__ == "__main__":
    console = Console()
    try:
        while True:
            console.print("[bold yellow]Menu:[/bold yellow]")
            console.print("[bold yellow]1. Store a new password[/bold yellow]")
            console.print("[bold yellow]2. Generate a random password[/bold yellow]")
            console.print("[bold yellow]3. View a password[/bold yellow]")
            console.print("[bold yellow]4. Exit[/bold yellow]")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                sitename = input("Enter the sitename: ")
                username = input("Enter the username: ")
                password = input("Enter the password: ")

                save_to_database(sitename, username, password)
                console.print("[bold cyan]Data saved to the database successfully![/bold cyan]")

            elif choice == "2":
                password_length = int(input("Enter the desired password length: "))
                if password_length <= 0:
                    console.print("[bold red]Password length must be greater than zero.[/bold red]")
                else:
                    password = generate_random_password(password_length)
                    pyperclip.copy(password)  # Copy the password to the clipboard
                    console.print(f"[green]Generated password:[/green] {password}")
                    console.print("[bold yellow]Copied to clipboard![/bold yellow]")
            elif choice == "3":
                sitename = input("Enter the sitename for which you want to view the password: ")
                view_passwords(sitename)

            elif choice == "4":
                console.print("[red] Program stopped successfully [/red]")
                break

            else:
                console.print("[bold red]Invalid choice. Please choose a valid option (1/2/3/4).[/bold red]")

    except ValueError:
        console.print("[bold red]Invalid input. Please enter a valid positive integer for the password length.[/bold red]")

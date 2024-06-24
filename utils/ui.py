import os

def create_env_file():
    """Creates a .env file with user-provided credentials."""
    try:
        credentials = {
            "RH_ACCESS_TOKEN": os.getenv('RH_ACCESS_TOKEN'),
            "GROQ_API_KEY": os.getenv('GROQ_API_KEY'),
            "DC_EMAIL": os.getenv('DC_EMAIL'),
            "DC_PASS": os.getenv('DC_PASS'),
            "FB_EMAIL": os.getenv('FB_EMAIL'),
            "FB_PASS": os.getenv('FB_PASS'),
            "G_HOME_EMAIL": os.getenv('G_HOME_EMAIL'),
            "G_HOME_PASS": os.getenv('G_HOME_PASS')
        }

        with open(".env", "w") as env_file:
            for key, value in credentials.items():
                env_file.write(f"{key}='{value}'\n")
        print(".env file created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_ui():
    """Simulates the UI function for Heroku environment."""
    print("UI function called. No tkinter needed.")
    create_env_file()

# Call create_ui if this script is run directly
if __name__ == "__main__":
    create_ui()

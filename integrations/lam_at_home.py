import os
import sys
import logging
import time
from utils import splash_screen_function, config_function, journal_function

def save(entry: journal_function.Entry) -> None:
    '''
    Save the given entry's resources to disk.
    '''
    if entry:
        if config_function.config['lamathomesave_isenabled']:
            save_path = config_function.config['lamathomesave_path']
            save_path = os.path.expanduser(save_path)
            save_path = os.path.expandvars(save_path)
            
            if not os.path.exists(save_path):
                try:
                    os.makedirs(save_path)
                except OSError as error:
                    logging.error(f"Error creating directory: {error}")
                    save_path = os.path.expandvars(config_function.config['cache_dir'])
            
            entry.save_resources(save_path)

def terminate() -> None:
    '''
    Terminate the LAMatHome application.
    '''
    if not config_function.config["lamathometerminate_isenabled"]:
        logging.error("LAMatHome termination is not enabled.")
        return
    print(splash_screen_function.colored_splash_goodbye)
    sys.exit()

def lam_at_home_function():
    print("Inside lam_at_home_function")
    splash_screen_function()
    config_function()
    journal_function()
    
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting LAMatHome with Rabbit access token")
    
    try:
        while True:
            # Example task to keep the app running
            logging.info("LAMatHome is running...")
            time.sleep(60)  # Sleep for 60 seconds before repeating
    except KeyboardInterrupt:
        print("Exiting LAMatHome... Goodbye!")
        terminate()

if __name__ == "__main__":
    print("Starting LAMatHome...")
    lam_at_home_function()
    print("LAMatHome is exiting... Goodbye!")

import os

DEBUG = os.getenv("DEBUG", False)

# Comment 

if DEBUG:
    print("Wir sind in Wartungsarbeiten")
    from pathlib import Path
    from dotenv import load_dotenv
    env_path = Path(".") / ".env.debug"
    load_dotenv(dotenv_path=env_path)
    from settings_files.development import *
else:
    print("Wir sind in Wartungsarbeiten")
    from settings_files.production import *

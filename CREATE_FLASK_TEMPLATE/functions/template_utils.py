import markdown
from datetime import datetime

def format_message(message):
    return markdown.markdown(message)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
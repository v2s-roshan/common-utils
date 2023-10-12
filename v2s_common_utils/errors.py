import configparser

def load_error_messages(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    
    error_messages = {}
    
    for section in config.sections():
        for key, value in config.items(section):
            error_messages[key.upper()] = value
    
    return error_messages



# Path to your message.properties file
MESSAGE_PROPERTIES_FILE_PATH = 'message.properties'

# Load the error messages
error_messages = load_error_messages(MESSAGE_PROPERTIES_FILE_PATH)

# Create a function to retrieve error messages by error code
def get_error_message(error_code):
    return error_messages.get(error_code, 'Undefined error')


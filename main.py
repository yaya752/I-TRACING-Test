from AbuseIPDBClient import AbuseIPDBClient
from Logger import Logger
import certstream

def print_callback(message,context):
    print(message)

def on_open():
    print("Connection successfully established!")

def on_error(exception):
    print("Exception in CertStreamClient! -> {}".format(exception)) 



def main():
    certstream.listen_for_events(print_callback, on_open=on_open, on_error=on_error, url='ws://localhost:8080/')
	

if __name__ == "__main__":
	main()
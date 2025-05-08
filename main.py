from AbuseIPDBClient import AbuseIPDBClient
from Logger import Logger
import certstream
import Levenshtein
# Configuration
OUR_DOMAIN = "pepito"
SIMILARITY_THRESHOLD = 0.75
def similarity_check(domain1, domain2):
    """
    Check if two domains are similar based on Levenshtein ratio.
    """
    ratio = Levenshtein.ratio(domain1, domain2)
    
    return ratio
def my_callback(message, context): 
    #print(f"[LOG] {message}") 
    for domain in message['data']['leaf_cert']['all_domains']:
        similar_domains = []
        domains_split = domain.split('.') + domain.split('-') + domain.split('_')
        for word in domains_split:
            if similarity_check(word, OUR_DOMAIN) >= SIMILARITY_THRESHOLD:
                similar_domains.append(domain)
                print(f"[LOG] Similar domains found: {similar_domains},{similarity_check(word, OUR_DOMAIN)}")

def on_open():
    print("Connection successfully established!")

def on_error(exception):
    print("Exception in CertStreamClient! -> {}".format(exception)) 



def main():
    certstream.listen_for_events(my_callback, on_open=on_open, on_error=on_error, url='ws://localhost:8080/')
	

if __name__ == "__main__":
	main()
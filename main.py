from AbuseIPDBClient import AbuseIPDBClient
from Logger import Logger
import certstream
import Levenshtein
import socket
import os
from dotenv import load_dotenv


# Configuration
load_dotenv("API.env") 
OUR_DOMAIN = "google"
SIMILARITY_THRESHOLD = 0.75
API_KEY = os.getenv("ABUSEIPDB_API_KEY")
abuse_client = AbuseIPDBClient(api_key=API_KEY)
'''
Similarity check function: use levenshtein ratio to check if two domains are similar.
Returns a float between 0 and 1.
The closer to 1, the more similar the domains are.
'''
def similarity_check(domain1, domain2):
    """
    Check if two domains are similar based on Levenshtein ratio.
    """
    ratio = Levenshtein.ratio(domain1, domain2)
    
    return ratio

'''
Resolve IP function: use socket to resolve the domain name to an IP address.
Returns the IP address as a string.
If the domain name cannot be resolved, returns None.
'''
def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None
    
'''
Callback function: this function is called when a new certificate is found.
It checks if the domain name is similar to OUR_DOMAIN and print domain,IP,issuing auth.
'''
def my_callback(message, context): 
    #print(f"[LOG] {message}") 
    for domain in message['data']['leaf_cert']['all_domains']:
        domain_is_typo = False
        # Check if the domain is similar to OUR_DOMAIN
        domains_split = domain.split('.') + domain.split('-') + domain.split('_')
        for word in domains_split:
            if similarity_check(word, OUR_DOMAIN) >= SIMILARITY_THRESHOLD:
                domain_is_typo = True
        if domain_is_typo:
            # Log the suspicious domain
            print(f"[LOG] Suspicious domain found: Domain : {domain}, IP : {resolve_ip(domain)}, criticity {abuse_client.check_reputation(resolve_ip(domain))}, issuing authority: {message['data']['leaf_cert']['issuer']['aggregated']}")

def on_open():
    print("Connection successfully established!")

def on_error(exception):
    print("Exception in CertStreamClient! -> {}".format(exception)) 



def main():
    certstream.listen_for_events(my_callback, on_open=on_open, on_error=on_error, url='ws://localhost:8080/')
	

if __name__ == "__main__":
	main()
from AbuseIPDBClient import AbuseIPDBClient
from Logger import Logger
import certstream
import Levenshtein
import socket
import os
from dotenv import load_dotenv

# Configuration
OUR_DOMAIN = "pepito"
load_dotenv("API.env") 
SIMILARITY_THRESHOLD = 0.80
API_KEY = os.getenv("ABUSEIPDB_API_KEY")


abuse_client = AbuseIPDBClient(api_key=API_KEY)



'''
Similarity check function: use levenshtein ratio to check if two domains are similar.
Returns a float between 0 and 1.
The closer to 1, the more similar the domains are.
'''
def similarity_check(domain1, domain2):

    #Check if two domains are similar based on Levenshtein ratio.

    ratio = Levenshtein.ratio(domain1, domain2)
    return ratio

'''
Resolve IP function: use socket to resolve the domain name to an IP address.
Returns the IP address as a string.
If the domain name cannot be resolved, returns None.
'''
def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain.lstrip('*.'))
    except Exception:
        return None
    
'''
Callback function: this function is called when a new certificate is found.
It checks if the domain name is similar to OUR_DOMAIN and print domain,IP,issuing auth.
'''

def my_callback(message,context): 
    domains_typo = []
    for domain in message['data']['leaf_cert']['all_domains']:
        for word in domain.split("."):
            similarity = similarity_check(word, OUR_DOMAIN)
            if  similarity >= SIMILARITY_THRESHOLD:
                domains_typo.append(domain+" ("+str(int(similarity*100))+")")
                break
    # Log the suspicious domain
    if len(domains_typo) > 0:
        issuing_authority = message['data']['leaf_cert']['issuer']['aggregated']
        reputation =  abuse_client.check_reputation(resolve_ip(domains_typo[0]))
          
        if reputation == -1 :
            if (1 + similarity)/2 >= SIMILARITY_THRESHOLD and "Let's Encrypt" in issuing_authority:
                level = "High"
            else:
                level = "Medium"
        elif reputation >= 50:
            level = "High"
        elif reputation >= 20:
            level = "Medium"
        else:
            level =  "Low"
        Logger(print_logs=True).alert(level, domains_typo, issuing_authority)

def on_open():
    print("Connection successfully established!")

def on_error(exception):
    print("Exception in CertStreamClient! -> {}".format(exception)) 



def main():
    certstream.listen_for_events(my_callback, on_open=on_open, on_error=on_error, url='ws://localhost:8080/')
	

if __name__ == "__main__":
	main()
# Technical test for SOAR Engineer position
## Context
Look for any potential threat or attack that use a typosquatting website
## Installation
```pip install -r requirements.txt```\
    ```python main.py```\
Install and deploy certstream-server-go by d-Rickyy-b on your own local machine/serveur to get certificate update
## Troubleshoot
As the calidog server is down (issues https://github.com/CaliDog/certstream-python/issues/69 and https://github.com/CaliDog/certstream-python/issues/70)  I have set up my own server using https://github.com/d-Rickyy-b/certstream-server-go?tab=readme-ov-file
## TO DO

- [x] The domain name is close to that of your site. Use any method you like to do this, either by generating a list of similar keywords in advance (add this script to the rendering), or by calculating this similarity in real time (using Levenshtein for example).
- [x] The issuing authority: a Let's Encrypt certificate is less likely to be trusted.
- [x] The domain's AbuseIPDB score Note: the API can only check the score of IPs, but not of domains. You must therefore first resolve the domain(s) in question in order to obtain their score.
- [x] Implement the BaseClient and AbuseIPDBClient classes so that you can retrieve a one-line reputation score from your hand.
- [x] If a domain analysed is suspicious, add a line to a suspicious_domains.log file containing at least the following information
at least the following information:
1. Criticality level
2. The domains concerned
3. Issuing authority
- [ ] BONUS




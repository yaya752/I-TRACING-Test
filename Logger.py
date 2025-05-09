import os

LOGFILE = "{}/suspicious_domains.log".format(os.path.dirname(os.path.abspath(__file__)))

class Logger(object):
	def __init__(self, print_logs: bool = False):
		self.print_logs = print_logs

	def alert(self ,level: str,domains: str, issuer: str):
		domains_string = []
		for domain in domains:
			domains_string.append(domain[0] +" (" + domain[1] + ")")
		domain_str = ", ".join(domains_string)
		message = f"[{level.upper()}] {domain_str} ({issuer})"
		with open(LOGFILE, "a") as f:
			f.write(message + "\n")
		if self.print_logs:
			print(message)
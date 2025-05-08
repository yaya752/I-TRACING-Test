import os

LOGFILE = "{}/suspicious_domains.log".format(os.path.dirname(os.path.abspath(__file__)))

class Logger(object):
	def __init__(self, print_logs: bool = False):
		self.print_logs = print_logs

	def alert(self ,level: str,domains: str, issuer: str):
		domain_str = ",".join(domains)
		message = f"[{level.upper()}] {domain_str} ({issuer})"
		with open(LOGFILE, "a") as f:
			f.write(message + "\n")
		if self.print_logs:
			print(message)
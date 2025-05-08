from BaseClient import BaseClient

class AbuseIPDBClient(BaseClient):
	def __init__(self, api_key: str):
		super().__init__("https://api.abuseipdb.com/api/v2/", {
            "Key": api_key,
            "Accept": "application/json"
        })

	def check_reputation(self, ip: str = None):
		try:
			result = self.http_request("GET","check",params={"ipAddress": ip, "maxAgeInDays": 90})
			return result["data"]["abuseConfidenceScore"]
		except Exception as e:
			print(f"[ERROR] AbuseIPDB request failed: {e}")
			return -1
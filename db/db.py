import redis

class Db:

	def __init__(self):
		self.f = redis.Redis(host='redis', port=6379, decode_responses=True)

	def get(self, request_id):
		return self.f.get(request_id)

	def get_all_keys(self):
		return self.f.keys()

	def set(self, request_id, value):
		self.f.set(request_id, value)
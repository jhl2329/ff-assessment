import redis


class Db:

	def __init__(self):
		self.f = redis.Redis(host='redis', port=6379, decode_responses=True)

	def get(self, request_id):
		try:
			return self.f.get(request_id)
		except redis.ConnectionError:
			pass
		# return self.f.get(request_id)

	def get_all_keys(self):
		try:
			return self.f.keys()
		except redis.ConnectionError:
			pass

	def set(self, request_id, value):
		try:
			self.f.set(request_id, value)
		except redis.ConnectionError:
			pass
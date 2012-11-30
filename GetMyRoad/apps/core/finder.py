from core.models import Place, TripPoint
from collections import deque


class CurrentPoint(object):

	def __init__(self, previous_point, place, category, s_lan, s_lon):
		self.previous_point = previous_point
		self.place = place
		self.s_lan = s_lan
		self.s_lon = s_lon
		self.category = category
		if self.previous_point:
			self.len = self.previous_point.len + 1
			self.rate = self.previous_point.rate + self.place.rate
			self.time = self.previous_point.time + \
				self.previous_point.get_time_to_get(place.lat, place.lon)
		else:
			self.len = 1
			self.rate = 0
			self.time = self.previous_point.get_time_to_get(
				s_lan, s_lon, reverse=True
			)

	def can_add(self, point, time_limit):
		if self.time + self.place.get_time_to_get(point.lan, point.lon) \
			+ self.place.get_time_to_get(self.s_lan, self.s_lon) >= time_limit:
			return False

	def get_unused_categories(self, categories):
		used_categories = set()
		p = self
		while p:
			used_categories.add(p.category)
			p = p.previous_point
		return categories - used_categories



def find(lat, lon, categories, places, time_limit):
	'''
	lat, long - coordinates of start point
	categories - set of prefered categories
	time_limit - time limit
	places - best places of each category, groupped by category
	'''

	# in each step we are adding 3 most close point to our que
	q = deque([])
	candidates = []
	for cat, cat_places in places.items():
		for place in cat_places:
			if place.get_time_to_get(lat, lon) \
				+ place.get_time_to_get(lat, lon, reverse=True) < time_limit:
				candidates += [
					place.get_time_to_get(lat, lon, reverse=True),
					place, category
				]
	candidates.sort()
	for candidate in candidates[:3]:
		q.append(CurrentPoint(
			None, candidate[1], candidate[2], lan, lon
		))

	best_cp = None
	while q:
		if not best_cp or (best_cp.len < cp.len):
			best_cp = cp

		candidates = []
		cp = q.popleft()
		for cat in cp.get_unused_categories(categories):
			for place in places[cat]:
				if cp.can_add(place.lat, place.lon, time_limit):
					new_cp = CurrentPoint(cp, place, cat, lat, lon)
					candidates += [
						new_cp.time,
						new_cp
					]
		candidates.sort()
		for candidate in candidates[:3]:
			q.append(candidate[1])

	return best_cp

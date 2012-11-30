import logging

from core.models import Place, TripPoint
from collections import deque


logger = logging.getLogger("gmr.%s" % __name__)


PARALLEL_PLACES_COUNT = 3


class CurrentPoint(object):

	def __init__(self, previous_point, place, category, s_lat, s_lon):
		self.previous_point = previous_point
		self.place = place
		self.s_lat = s_lat
		self.s_lon = s_lon
		self.category = category
		if self.previous_point:
			self.len = self.previous_point.len + 1
			self.rank = self.previous_point.rank + self.place.rank
			time_to_get = self.previous_point.place.get_time_to_get(place.lat, place.lon)
			self.time = self.previous_point.time + time_to_get
			self.rank = self.previous_point.rank
		else:
			self.len = 1
			self.rank = 0
			self.time = self.place.get_time_to_get(
				s_lat, s_lon, reverse=True
			)
			self.rank = 0
		self.rank += self.place.rank
		self.time += self.place.get_avg_spend_time(self.time)

	def can_add(self, point, time_limit):
		if self.time + self.place.get_time_to_get(point.lat, point.lon) + \
			self.place.get_avg_spend_time(self.time) + \
			self.place.get_time_to_get(self.s_lat, self.s_lon) \
		>= time_limit:
			return False
		# TODO check if place works at that time
		return True

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

	def sort_by(values):
		# we don't care about 5 minutes different
		# rank is more important in this situation
		return int(values[0].total_seconds() / 5 / 60), values[1]

	# in each step we are adding PARALLEL_PLACES_COUNT most close point to our que
	q = deque([])
	candidates = []
	for cat, cat_places in places.items():
		for place in cat_places:
			# checking if we are still fitting to the time limit
			if place.get_time_to_get(lat, lon) + \
			place.get_avg_spend_time(place.get_time_to_get(lat, lon)) + \
			place.get_time_to_get(lat, lon, reverse=True) < time_limit:
				candidates.append((
					place.get_time_to_get(lat, lon, reverse=True),
					place.rank,
					place, cat
				))
	candidates = sorted(candidates, key=sort_by)
	for candidate in candidates[:PARALLEL_PLACES_COUNT]:
		q.append(CurrentPoint(
			None, candidate[2], candidate[3], lat, lon
		))

	best_p = None
	while q:
		cp = q.popleft()
		if not best_p or (best_p.len < cp.len) or \
			(best_p.len == cp.len and best_p.rank < cp.rank):
			best_p = cp

		candidates = []
		for cat in cp.get_unused_categories(categories):
			for place in places[cat]:
				# checking if we are still fitting to the time limit
				# and possibly other reasons(place don't work on that time, etc)
				if cp.can_add(place, time_limit):
					new_cp = CurrentPoint(cp, place, cat, lat, lon)
					candidates.append((
						new_cp.time, new_cp.rank, new_cp
					))
		candidates = sorted(candidates, key=sort_by)
		for candidate in candidates[:PARALLEL_PLACES_COUNT]:
			q.append(candidate[2])

	route = []
	time = best_p.time + best_p.place.get_time_to_get(lat, lon)
	cp = best_p
	while cp:
		route.append(cp)
		if not cp.previous_point:
			time += cp.place.get_time_to_get(lat, lon, reverse=True)
		cp = cp.previous_point
	return route, time

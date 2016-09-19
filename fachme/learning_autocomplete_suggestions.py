import redis
import logging


class LearningAutocompleteSuggestions(object):

    def __init__(self, namespace='LEARNING_AUTOCOMPLETE', port=6379, db=0, host='localhost'):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.search_time_to_live = 60 * 60  # One hour
        self.REDIS_NAMESPACE = namespace

    def register_search(self, search_string, search_id=None):
        """
        Associate a search string with this search session
        """
        logging.debug("Searching for %s with id %s" % (search_string, search_id))
        if search_id:
            key = self._search_key(search_id)
            self.redis.rpush(key, search_string)
            self.redis.expire(key, self.search_time_to_live)

    def suggestion_generator(self, search_string, ignore_values=[]):
        """
        A generator of suggested canonical results for a search string
        """
        logging.debug("Searching for %s" % (search_string))
        ignore_strings = [str(n) for n in ignore_values]
        key = self._suggestion_key(search_string)
        for r in self.redis.zrevrange(key, 0, -1):
            if r not in ignore_strings:
                yield r

    def associate_canonical(self, canonical, search_id):
        """
        Associate a canonical value with all the previous searches from this
        session
        """
        logging.debug("Associating the canonical value %s with id %s" % (canonical, search_id))
        user_search_key = self._search_key(search_id)

        searches = self.redis.lrange(user_search_key, 0, -1)

        # Even though queries come in bursts, all substrings are equally valid.
        # Normalize the searches into all indexable strings
        search_substrings = set()
        for search_string in searches:
            for i in xrange(len(search_string)):
                sub_str = search_string[0:i + 1]
                search_substrings.add(sub_str)

        for sub_str in search_substrings:
            self._associate(sub_str, canonical)

        self.redis.delete(user_search_key)

    def _associate(self, search_string, canonical):
        """
        Associate a search string with a canonical value
        """
        logging.debug("Associating search %s with the canonical value %s" % (search_string, canonical))
        key = self._suggestion_key(search_string)
        self.redis.zincrby(key, canonical, 1)

    def _suggestion_key(self, search_string):
        return "%s:suggestions:%s" % (self.REDIS_NAMESPACE, search_string)

    def _search_key(self, search_id):
        return "%s:searches:%s" % (self.REDIS_NAMESPACE, search_id)

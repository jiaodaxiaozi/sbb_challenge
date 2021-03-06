import isodate


class Resource(object):
    def __init__(self, data):
        self._data = data
        self.id = self._data["id"]
        self.sections = []

        self.free = True
        self.last_used_by = None
        self.last_exit_time = None
        self.currently_used_by = None

        self.release_time = isodate.parse_duration(self._data["release_time"]).seconds

    def get_id(self):
        return self.id

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def get_release_time(self):
        """
        describes how much time must pass between release of a resource by one train and the following occupation by the next train. See Business Rules for details.
        """
        return self.release_time

    def get_following_allowed(self):
        """flag whether the resource is of following type (true) or of blocking type (false).
        As mentioned, all resources in all the provided problem instances have this field set to false
        """
        return self._data["following_allowed"]

    def __str__(self):
        return "%s (%i s)" % (self.get_id(), self.get_release_time())

    def is_free_for(self, train):
        if self.free:
            return True

        if train == self.last_used_by:
            return True

        return False

    def enter(self, train, at):
        assert self.currently_used_by is None or self.currently_used_by == train

        self.free = False
        self.currently_used_by = train
        self.last_used_by = train

    def exit(self, train, at):
        assert self.free is False
        assert self.last_used_by == train

        self.currently_used_by = None
        self.last_exit_time = at

    def release(self, train, release_time):
        if release_time < self.last_exit_time:
            return
        if self.currently_used_by is not None:
            return

        assert self.free is False
        assert self.currently_used_by is None, "%s %s" % (train, self)
        assert train == self.last_used_by

        self.free = True

    def __hash__(self):
        return hash(self.get_id())

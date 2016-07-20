from collections import deque


class Task(object):
    def __init__(self, function_queue, priority):
        self.__queue = deque(function_queue)
        self.priority = priority

    @property
    def is_done(self):
        return len(self.__queue) == 0

    def execute_step(self):
        function = self.__queue.popleft()
        return function()

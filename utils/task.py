from collections import deque


class Task:
    def __init__(self, function_queue):
        self.__queue = deque(function_queue)

    @property
    def is_done(self):
        return len(self.__queue) == 0

    def execute_step(self):
        function = self.__queue.popleft()
        return function()
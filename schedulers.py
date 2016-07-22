from time import sleep


class BaseTaskScheduler(object):
    
    def __init__(self):
        self._current_task = None

    def update_tasks(self, tasks):
        raise NotImplementedError(
                '%s does not have an update_tasks method' %
                self.__class__.__name__
            )

    def execute_step(self):
        if self._current_task and not self._current_task.is_done:
            result = self._current_task.execute_step()
            self._current_task = self._current_task if result is not False else None
            sleep(2)

class RandomizedTaskScheduler(BaseTaskScheduler):

    def __init__(self):
        super(self.__class__, self).__init__()

    def update_tasks(self, tasks):
        from random import shuffle
        shuffled = tasks[:]
        shuffle(shuffled)

        selected_task = shuffled[0]
        for task in shuffled:
            if task.priority > selected_task.priority:
                selected_task = task

        if (
            not self._current_task
            or selected_task.priority > self._current_task.priority
            or self._current_task.is_done
        ):
            self._current_task = selected_task

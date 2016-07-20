class BaseTaskScheduler(object):
    
    def __init__(self):
        self._current_task = None

    def update_tasks(self, tasks):
        raise NotImplementedError(
                'BaseTaskScheduler.update_tasks is abstract'
            )

    def execute_step(self):
        if self._current_task and not self._current_task.is_done:
            result = self._current_task.execute_step()
            self._current_task = self._current_task if result else None

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

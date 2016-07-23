from basemodule import BaseModule, task


class IdleModule(BaseModule):

    def execute(self):
        return self.cycle()

    @task
    def cycle(self):
        print('Idle')

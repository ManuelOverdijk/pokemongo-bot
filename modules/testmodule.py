from basemodule import BaseModule, task


class TestModule(BaseModule):

    def execute(self):
        print('TestModule executed')
        return self.do_stuff() + self.do_other_stuff()

    @task
    def do_stuff(self):
        print('Stuff was done')
        return True

    @task
    def do_other_stuff(self):
        print('Other stuff was done')
        return True

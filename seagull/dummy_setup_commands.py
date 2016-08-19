from distutils.cmd import Command



class DummyCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print('This command is only supported on Python 3.5 or newer')


class Watch(DummyCommand):
    pass


class Stop(DummyCommand):
    pass


class Recompile(DummyCommand):
    pass

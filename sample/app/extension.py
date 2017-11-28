from gallium.interface import IExtension, depend_on

class A(IExtension):
    def config_key(self):
        return None

    def initialize(self, core, config = None):
        print('Extension A: Activated')

@depend_on(A)
class B(IExtension):
    def config_key(self):
        return None

    def initialize(self, core, config = None):
        print('Extension B: Activated')

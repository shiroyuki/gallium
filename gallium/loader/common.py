class ILoader(object):
    def configuration_section_name(self):
        """ The configuration section name

            :rtype: str
        """
        raise NotImplemented('Please implement this method.')

    def all(self, *largs, **kwargs):
        """ The configuration section name

            :return: a list or iterator of with a tuple/list of identifier, class type, and class instance.
        """
        raise NotImplemented('Please implement this method.')

from selenium.common.exceptions import NoSuchElementException

class MenuPageElement(object):
    '''element that requires selecting each time its attributes are accessed
    _locator: to find the menu instance on a page
    _selected_locator: to determine whether the menu instance has already been selected
    _selector: method to select self; applied to a Selenium page element
    Note: all attributes not prefixed with '_' sign are preceeded with a self._select() call
    '''
    _locator = staticmethod(lambda : None)
    _selected_locator = staticmethod(lambda : None)
    _selector = staticmethod(lambda x: None)

    def _select(self):
        '''if not selected, select'''
        try:
            # already selected?
            self._selected_locator()
        except NoSuchElementException as e:
            # nope --- click the menu and try again
            self._selector(self._locator())
            self._selected_locator()

    def __getattribute__(self, attrname):
        '''to access attributes, menu instance has to be selected
           all attributes that do not start with the '_' sign are preceeded with a _select() call
        '''
        if attrname.startswith('_'):
            return super(MenuPageElement, self).__getattribute__(attrname)
        object.__getattribute__(self, '_select')()
        return object.__getattribute__(self, attrname)

    def __get__(self, obj, cls=None):
        return self._locator()

from collections import defaultdict


class State:
    def __init__(self, parent):
        self.data = None
        self.parent = parent
    
    @property
    def name(self):
        return self.__class__.__name__
    
    def _recognize(self, value):
        return None #tri-value return: False means bad, True means good, None means dunno
    
    def _accept(self, value):
        pass
    
    def accept(self, value):
        '''
        Try to take data. If it doesn't apply, raise Unrecognized.
        '''
        
        if self._recognize(value) is False: #tri-value, so test for identity
            raise Unrecognized
        else:
            try:
                self._accept(value)
                
                return self
            except:
                raise Unrecognized

class StateMachine(State):
    def __init__(self, states):
        self.active_submachine = None
        self.data = defaultdict(list)
        
        self.states = states
    
    def accept(self, values):
        '''
        if I have an active submachine,
         keep passing data to it until it returns #iterator-based? (next(feed) if consuming, pass if submachine)
        find State that matches
         if found,
          pass value to it
          store state.data (store? append? multidict?)
         if not found,
          terminate
        '''
        
        if self.active_submachine:
            #give the submachine the iterator so it can eat all it wants
            self.data[self.active_submachine.name].append(self.active_submachine.accept(values))
        else:
            for value in values:
                for state in self.states:
                    try:
                        self.data[state.__name__].append(state(self).accept(value))
                    except Unrecognized:
                        pass #intentional

class Peekable:
    def __init__(self, iterator):
        self.iterator = iter(iterator) #iter() is idempotent
        self.current = None
    
    def __iter__(self):
        return self
    
    def __next__(self):
        current, self.current = self.current, None
        
        if current:
            return current
        else:
            return next(self.iterator)
    
    def peek(self):
        if not self.current:
            self.current = next(self.iterator)
        
        return self.current

class BaseSignal(Exception):
    pass

class Unrecognized(BaseSignal):
    pass

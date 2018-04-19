class State:
    def __init__(self, parent):
        self.data = None
        self.parent = parent
    
    @classmethod
    def from_parameters(self, should_enter=lambda x: False, on_enter=lambda x: None):
        pass #TODO: implement
    
    def should_enter(self, value):
        'is this State eligible for entry?'
        
        pass
    
    def on_enter(self, value):
        'do stuff after entry (should only affect self.data)'
        
        pass
    
    def try_entry(self, value):
        if self.should_enter(value):
            self.on_enter(value)
            
            return self #return self or self.data? basically comes down to: instantiate or reuse?
        else:
            return None

class StateMachine(State):
    def __init__(self, states):
        self.active_submachine = None
        
        self.states = {state.__class__.__name__: state(self) for state in states}
    
    def eat(self, value):
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
        
        pass

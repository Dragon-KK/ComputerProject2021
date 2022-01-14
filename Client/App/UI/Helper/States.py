class State:
    def __init__(self, name):
        self.stateName = name

    def __eq__(self, state):
        t = type(state)
        if t == str:
            return self.stateName == state
        elif t == State:
            return self.stateName == state.stateName
        else:
            return False


class StateHolder(list):
    def __init__(self):
        self.OnStateChanged = lambda *args,**kwargs:0

    def AddState(self,state, update = True):
        if state not in self:
            if type(state) == str:
                self.append(State(state))
                if update:self.OnStateChanged(added = self[-1])
            elif type(state) == State:
                self.append(state)
                if update:self.OnStateChanged(added = self[-1])

    def RemoveState(self, state, update = True):
        if state in self:
            self.remove(state)
            if update:self.OnStateChanged(removed = (State(state) if type(state) == str else state))
        return self


    def __add__(self, other):
        self.AddState(other)
        return self

    def __sub__(self,other):
        self.RemoveState(other)
        return self

    def __iadd__(self, other):
        self.AddState(other)
        return self

    def __isub__(self,other):
        self.RemoveState(other)
        return self

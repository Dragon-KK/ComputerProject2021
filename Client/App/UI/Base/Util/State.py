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

class States:
    Visible = State("Visible")
    KeyboardFocused = State("KeyboardFocused")
    Hovered = State("Hovered")
    Focused = State("Focused")

class StateHolder:
    def __init__(self):
        self.States = []
        self.OnChange = lambda *args, **kwargs:0
    


    def __add__(self, other):
        if other not in self.States:
            if type(other) == str:
                self.States.append(State(other))
                self.OnChange(propogate = (other == States.Visible))
            elif type(other) == State:
                self.States.append(other)
                self.OnChange(propogate = (other == States.Visible))

        return self

    def __sub__(self,other):
        if other in self.States:
            self.States.remove(other)
            self.OnChange(removed = [other], propogate = (other == States.Visible))
        return self

    def __contains__(self, item):
        return item in self.States

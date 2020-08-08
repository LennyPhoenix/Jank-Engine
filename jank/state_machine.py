import typing as t

import pyglet


class StateMachine(pyglet.event.EventDispatcher):
    _state: t.Any = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if self.state != state:
            previous_state = self.state
            self._state = state
            self.dispatch_event("on_state_change", state, previous_state)

    def on_state_change(self, state, previous_state):
        """ Called after state change. """


StateMachine.register_event_type("on_state_change")

from enum import Enum
import ipywidgets as widgets


class EventType(Enum):
    KEYWORDS_SELECTED = 'KEYWORDS_SELECTED'


class EventBus:
    def __init__(self):
        self.subscribers = {}

        self.debug_active = False
        self.debug_display = widgets.Textarea()
        self.debug_nesting = 0

    def subscribe(self, event_type: EventType, callback):

        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type: EventType, data):
        self.debug_nesting += 1
        self.show_debug('Event ' + event_type.value + ' published '+str(data))

        responses = []

        if event_type in self.subscribers:
            for i, callback in enumerate(self.subscribers[event_type]):

                if self.debug_active:
                    self.show_debug(str(i) + '. ' + callback.__self__.__class__.__name__ + '.' + callback.__name__)


                response_i = callback(data)

                if response_i is not None:
                    responses.append(response_i)

        self.show_debug('----- event ' + event_type.value + ' done with '+str(len(responses))+' responses' + '\n')
        self.debug_nesting -= 1

        if len(responses) > 0:
            if len(responses) == 1:
                return responses[0]
            else:
                return responses


    def show_debug(self, new_value: str):
        if not self.debug_active:
            return
        self.debug_display.value = self.debug_display.value + '\n' + ''.join(['\t'] * self.debug_nesting) + new_value
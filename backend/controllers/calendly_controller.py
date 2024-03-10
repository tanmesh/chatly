
class CalendlyController:
    def __init__(self, service):
        self.service = service

    def list_scheduled_events(self):
        return self.service.list_scheduled_events()

    def cancel_event(self, args):
        return self.service.cancel_event(args)

    def create_event(self, args):
        return self.service.create_event(args)
    

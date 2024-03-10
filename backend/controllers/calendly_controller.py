
class CalendlyController:
    def __init__(self, service):
        self.service = service

    def list_scheduled_events(self, llm):
        return self.service.list_scheduled_events(llm)

    def cancel_event(self, args):
        return self.service.cancel_event(args)

    def create_event(self, args):
        return self.service.create_event(args)
    

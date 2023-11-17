class EventProvider:

    @staticmethod
    def is_event_time(iteration):
        return iteration % 100 == 0

    @staticmethod
    def is_reevaluation_time(iteration):
        return iteration % 10000 == 0

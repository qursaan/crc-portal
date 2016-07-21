

class ReservationStatus:

    def __init__(self):
        pass

    _pending = 1
    _waiting = 2
    _active = 3
    _expired = 4
    _canceled = 5
    _bulk = 6

    @staticmethod
    def get_all_list():
        return [1, 2, 3, 4, 5, 6]

    @staticmethod
    def get_busy_list(allow_bulk=False, allow_pending=False):
        busy_list = [3]  # active is busy
        if not allow_bulk:
            busy_list.append(6)  # bulk is busy if not allowed
        if not allow_pending:
            busy_list.append(2)  # waiting is busy if not allowed to reserve over
            busy_list.append(1)  # pending is busy
        return busy_list

    @staticmethod
    def get_active():
        return 3

    @staticmethod
    def get_pending():
        return 1

    @staticmethod
    def get_expired():
        return 4

    @staticmethod
    def get_canceled():
        return 5

    @staticmethod
    def get_bulk():
        return 6

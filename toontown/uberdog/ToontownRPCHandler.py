class ToontownRPCHandler:
    def __init__(self, air):
        self.air = air

    def rpc_ping(self, request, data):
        """For testing purposes: This just echos back the provided data."""
        return data

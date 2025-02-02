from adapters import Adapters


class DataIngestion:
    def __init__(self):
        self.features = ["points", "rebounds", "assists"]
        self.adapters = Adapters()
    
    
    async def get_and_process_features(self, features):
        pass
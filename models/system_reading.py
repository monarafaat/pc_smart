class SystemReading:
    """Represents a single hardware performance snapshot."""
    
    def __init__(self, user_id, cpu_usage, ram_usage, disk_usage, timestamp):
        self.user_id = user_id
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self.disk_usage = disk_usage
        self.timestamp = timestamp

    def to_tuple(self):
        """Converts reading instance to a tuple for database insertion."""
        return (self.user_id, self.cpu_usage, self.ram_usage, self.disk_usage, self.timestamp)
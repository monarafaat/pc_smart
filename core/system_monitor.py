import psutil

class SystemMonitor:
    """Monitors real-time hardware metrics including CPU, RAM, Disk, and Network."""
    
    def get_cpu_metrics(self):
        """Returns CPU usage percentage, frequency, and core count."""
        return {
            "usage_percent": psutil.cpu_percent(interval=0.5),
            "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
            "cores": psutil.cpu_count(logical=True)
        }

    def get_ram_metrics(self):
        """Returns RAM total, used, available, and usage percentage."""
        ram = psutil.virtual_memory()
        return {
            "total_gb": round(ram.total / (1024**3), 2),
            "used_gb": round(ram.used / (1024**3), 2),
            "available_gb": round(ram.available / (1024**3), 2),
            "usage_percent": ram.percent
        }

    def get_disk_metrics(self):
        """Returns primary disk usage metrics."""
        disk = psutil.disk_usage('/')
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "usage_percent": disk.percent
        }

    def get_battery_metrics(self):
        """Returns laptop battery percentage and power status if available."""
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged
            }
        return None
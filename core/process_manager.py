import psutil

class ProcessManager:
    """Manages active system processes and handles termination."""
    
    def get_active_processes(self, limit=15):
        """Retrieves top active processes sorted by memory consumption."""
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                p_info = p.info
                p_info['cpu_percent'] = p_info['cpu_percent'] or 0.0
                p_info['memory_percent'] = p_info['memory_percent'] or 0.0
                processes.append(p_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort descending by memory usage
        return sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:limit]

    def terminate_process(self, pid):
        """Terminates a specific process using its Process ID (PID)."""
        try:
            p = psutil.Process(pid)
            p.terminate()
            return True, f"Process {pid} terminated successfully."
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
            return False, str(e)
import os

class SystemAnalyzer:
    """Analyzes storage and scans for large files exceeding thresholds."""
    
    def __init__(self, size_threshold_mb=50):
        # Convert MB threshold to bytes
        self.size_threshold = size_threshold_mb * 1024 * 1024

    def scan_large_files(self, target_path="C:\\Users"):
        """Scans specified directory for files larger than the 50MB threshold."""
        large_files = []
        
        for root, dirs, files in os.walk(target_path):
            # Skip system folders to prevent permission crashes
            if any(sys_folder in root for sys_folder in ["Windows", "System32", "$Recycle.Bin"]):
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size >= self.size_threshold:
                        size_mb = round(file_size / (1024 * 1024), 2)
                        large_files.append({
                            "name": file,
                            "path": file_path,
                            "size_mb": size_mb
                        })
                except (PermissionError, FileNotFoundError):
                    continue
                    
        return sorted(large_files, key=lambda x: x["size_mb"], reverse=True)

    def delete_large_file(self, file_path):
        """Deletes a selected large file from the disk."""
        try:
            os.remove(file_path)
            return True, "File deleted successfully."
        except Exception as e:
            return False, str(e)
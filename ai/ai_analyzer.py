class AIAnalyzer:
    """Analyzes system metrics and provides intelligent recommendations or answers."""
    
    def analyze_system_status(self, cpu_metrics, ram_metrics, processes):
        """Generates automated diagnostic insights based on active hardware usage."""
        recommendations = []
        
        if cpu_metrics["usage_percent"] > 80:
            recommendations.append("Your CPU usage is unusually high.")
            
        if ram_metrics["usage_percent"] > 85:
            top_process = processes[0]['name'] if processes else "An application"
            recommendations.append(f"'{top_process}' is currently consuming most of your RAM.")
            recommendations.append("Recommendation: Close unnecessary browser tabs or heavy background applications.")
            
        if not recommendations:
            recommendations.append("System performance is optimal. All resources are operating within healthy limits.")
            
        return recommendations

    def answer_user_query(self, query, cpu_metrics, ram_metrics):
        """Responds dynamically to custom user inquiries regarding system performance."""
        query_lower = query.lower()
        
        if "slow" in query_lower or "lag" in query_lower:
            if cpu_metrics["usage_percent"] > 75 or ram_metrics["usage_percent"] > 80:
                return "Your computer is running slow because hardware resource usage is currently high. Check the Process Manager to terminate heavy tasks."
            return "Your system hardware metrics appear normal. The slowdown might be due to temporary application response delays."
        
        elif "ram" in query_lower or "memory" in query_lower:
            return f"Current RAM usage is at {ram_metrics['usage_percent']}% ({ram_metrics['used_gb']} GB used out of {ram_metrics['total_gb']} GB)."
            
        elif "cpu" in query_lower:
            return f"Current CPU usage is operating at {cpu_metrics['usage_percent']}% across {cpu_metrics['cores']} cores."
            
        return "I am analyzing your system parameters. Please specify if you need assistance with CPU, RAM, or storage optimization."
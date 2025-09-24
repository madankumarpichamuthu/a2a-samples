"""Simple Time Greeting Method Extension for A2A Protocol."""

from datetime import datetime
from typing import Dict, Any
import zoneinfo


class SimpleTimeGreetingExtension:
    """Minimal method extension that provides time-based greetings."""
    
    def __init__(self):
        self.extension_id = "http://localhost:8080/extensions/simple-time-greeting/v1"
        self.version = "1.0.0"
    
    def time_greeting(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """JSON-RPC method: Get time-appropriate greeting."""
        try:
            timezone_str = params.get("timezone", "UTC")
            
            # Get current time in specified timezone
            try:
                tz = zoneinfo.ZoneInfo(timezone_str)
            except:
                tz = zoneinfo.ZoneInfo("UTC")
            
            now = datetime.now(tz)
            hour = now.hour
            
            # Determine time period and greeting
            if 5 <= hour < 12:
                time_period = "morning" 
                greeting = "Good morning!"
            elif 12 <= hour < 17:
                time_period = "afternoon"
                greeting = "Good afternoon!"
            else:
                time_period = "evening"
                greeting = "Good evening!"
            
            return {
                "greeting": greeting,
                "time_period": time_period
            }
            
        except Exception as e:
            return {
                "error": {
                    "code": -32000,
                    "message": f"Time greeting error: {str(e)}"
                }
            }
    
    def get_extension_metadata(self) -> Dict[str, Any]:
        """Return extension metadata for agent card."""
        return {
            "uri": self.extension_id,
            "version": self.version,
            "type": "method",
            "name": "Simple Time Greeting",
            "description": "Provides time-based greetings (morning, afternoon, evening)",
            "methods": ["time-greeting"]
        }
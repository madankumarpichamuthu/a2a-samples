"""Basic Logging Extension for A2A Protocol."""

import time
import uuid
from datetime import datetime, timezone
from typing import Optional


class BasicLoggingExtension:
    """Minimal logging extension that tracks basic request metrics."""
    
    def __init__(self):
        self.extension_id = "http://localhost:8080/extensions/basic-logging/v1"
        self.version = "1.0.0"
        
    def start_request(self, request_id: Optional[str] = None) -> dict:
        """Start tracking a request and return context."""
        context = {
            "request_id": request_id or f"req_{uuid.uuid4().hex[:8]}",
            "start_time": time.time()
        }
        return context
    
    def log_completion(self, context: dict, status: str = "success") -> dict:
        """Log request completion with basic metrics."""
        end_time = time.time()
        processing_time_ms = int((end_time - context["start_time"]) * 1000)
        
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": context["request_id"],
            "processing_time_ms": processing_time_ms,
            "status": status
        }
        
        print(f"[{log_entry['timestamp']}] {log_entry['request_id']} completed in {processing_time_ms}ms - {status}")
        return log_entry
    
    def get_extension_metadata(self) -> dict:
        """Return extension metadata for agent card."""
        return {
            "uri": self.extension_id,
            "version": self.version,
            "type": "data",
            "name": "Basic Request Logging",
            "description": "Simple request tracking with timestamps and processing time"
        }
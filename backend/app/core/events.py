import logging
from typing import Callable, Dict, List, Any
from datetime import datetime

logger = logging.getLogger("domain_events")

class EventBus:
    """Internal Domain Event Bus for decoupled asynchronous module communication"""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], Any]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], Any]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info(f"Registered subscriber for event: {event_type}")

    def publish(self, event_type: str, payload: Dict[str, Any]):
        payload["_event_type"] = event_type
        payload["_timestamp"] = datetime.utcnow().isoformat()
        logger.info(f"Publishing domain event: {event_type}")
        
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    handler(payload)
                except Exception as e:
                    logger.error(f"Error handling event {event_type} in {handler.__name__}: {str(e)}")

event_bus = EventBus()

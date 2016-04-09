
from .fb import update_fb_events
from .events_at_cu import update_from_eventsatcu
from .engineeringevents import update_engineering_events


scrapers = [
    update_engineering_events,
    update_fb_events,
    update_from_eventsatcu,
]

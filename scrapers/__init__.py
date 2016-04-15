from .fb import update_fb_events
from .events_at_cu import update_from_eventsatcu
from .engineeringevents import update_engineering_events


scrapers = {
    "engineering": update_engineering_events,
    "facebook": update_fb_events,
    "sundial": update_from_eventsatcu,
}

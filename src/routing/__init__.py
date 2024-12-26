from .ping import router as ping_routing
from .countries import router as countries_routing
from .auth import router as auth_routing
from .me import router as me_routing
from .profiles import router as profiles_routing
from .friends import router as friends_routing

all_routers = [ping_routing, countries_routing, auth_routing, me_routing, profiles_routing, friends_routing]

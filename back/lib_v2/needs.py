from collections import namedtuple
from functools import partial
from lib_v2 import roles_constants

PssRouteNeed = namedtuple('pss_route_need', ['method', 'value'])
PssRouteNeedNoArgument = namedtuple('pss_route_need', ['method'])

EventCreatorRoleNeed = partial(PssRouteNeedNoArgument, roles_constants.EVENT_CREATOR)
EventEditNeed = partial(PssRouteNeed, roles_constants.EVENT_CREATOR)
TournamentDirectorRoleNeed = partial(PssRouteNeed, roles_constants.TOURNAMENT_DIRECTOR)

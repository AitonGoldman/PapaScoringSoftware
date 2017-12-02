from collections import namedtuple
from functools import partial
from lib_v2 import roles_constants

PssRouteNeed = namedtuple('pss_route_need', ['method', 'value'])
PssRouteNeedNoArgument = namedtuple('pss_route_need', ['method'])

EventCreatorLoginRoleNeed = partial(PssRouteNeedNoArgument, roles_constants.EVENT_CREATOR_LOGIN)

# -*- coding: utf-8 -*-
# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name

    from .RapportGeofluence import RapportGeofluence
    return RapportGeofluence(iface)

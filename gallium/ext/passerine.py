""" Extension for Passerine ORM """

import os

from ..interface import IExtension

from imagination.entity import CallbackProxy
from imagination.loader import Loader

class Extension(IExtension):
    def config_key(self):
        return 'orm'

    def initialize(self, core, config):
        core.set_entity(
            'passerine.factory',
            'passerine.db.manager.ManagerFactory'
        )

        manager_config  = config['managers']
        service_locator = core.locator
        em_factory      = core.get('passerine.factory')

        for alias in manager_config:
            url = manager_config[alias]['url']

            em_factory.set(alias, url)

            def callback(em_factory, alias):
                return em_factory.get(alias)

            service_locator.set(
                'db.{}'.format(alias),
                CallbackProxy(
                    callback,
                    em_factory,
                    alias
                )
            )

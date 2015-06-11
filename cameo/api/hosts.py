# Copyright 2014 Novo Nordisk Foundation Center for Biosustainability, DTU.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, print_function

import os
import optlang
import cameo
from cameo.util import IntelliContainer
from cameo import load_model
import six

MODEL_DIRECTORY = os.path.join(os.path.join(os.path.split(cameo.__path__[0])[0]), 'tests/data')


class Host(object):

    def __init__(self, name='', models=[], biomass=[], carbon_sources=[]):
        self.name = name
        self.models = IntelliContainer()
        for id, biomass in zip(models, biomass):
            self.models[id] = ModelFacade(id, biomass)

    def __str__(self):
        return self.name


class ModelFacade(object):

    def __init__(self, id, biomass=None, carbon_source=None):
        self._id = id
        self._model = None
        self.biomass = biomass
        self.carbon_source = carbon_source

    def __getattr__(self, value):
        if self._model is None:
            super(ModelFacade, self).__setattr__('_model', load_model(os.path.join(MODEL_DIRECTORY, self._id + '.xml')))
        try:
            return getattr(self._model, value)
        except KeyError:
            return getattr(super(ModelFacade, self), value, self)

    def __dir__(self):
        if self._model is None:
            self._model = load_model(os.path.join(MODEL_DIRECTORY, self._id + '.xml'))
        return dir(self._model)

    def __setattr__(self, key, value):
        if key in ["_id", "_model", "biomass", "carbon_source"]:
            self.__dict__[key] = value
            return
        try:
            return setattr(self._model, key, value)
        except KeyError:
            return setattr(super(ModelFacade, self), key, value)

class Hosts(object):

    def __init__(self, host_spec):
        self._host_spec = host_spec
        self._hosts = list()
        for host_id, information in six.iteritems(self._host_spec):
            host = Host(**information)
            self._hosts.append(host)
            setattr(self, host_id, host)

    def __iter__(self):
        return iter(self._hosts)

    def __dir__(self):
        return list(self._host_spec.keys())


HOST_SPECS = {
    # 'iAF1260', 'iJO1366', 'EcoliCore'
    'ecoli': {
        'name': 'Escherichia coli',
        'models': ('iJO1366',),
        'biomass': ('Ec_biomass_iJO1366_WT_53p95M',),
        'carbon_sources': ('EX_glc_e_',)
    },
    # 'iND750',
    'scerevisiae': {
        'name': 'Saccharomyces cerevisiae',
        'models': ('iMM904', ),
        'biomass': ('',),
        'carbon_sources': ('',)

    }
}

hosts = Hosts(HOST_SPECS)

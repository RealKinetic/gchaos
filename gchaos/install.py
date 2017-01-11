# MIT License

# Copyright (c) 2017 Real Kinetic

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging

from gchaos.config import CHAOS_CONFIG
from gchaos.gae.datastore import install_datastore_hooks

# TODO: Override the logging module so we can get a nice chaos formatted
# message


def install_chaos(config=None):
    """Log a quick message then install the chaos hooks into the Google API
    Proxies.
    """
    logging.info("CHAOS: Going to cause system wide chaos!!!")

    if not config:
        config = CHAOS_CONFIG

    # TODO: Create a to dict method on the ChaosConfig object.
    # logging.info("CHAOS: Default Chaos Config: {0}".format(config))

    install_datastore_hooks(config.datastore)
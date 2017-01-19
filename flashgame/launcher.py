import gym_controlplane
import logging
import os
import subprocess

from gym_controlplane import utils
from gym_flashgames import selenium_wrapper
from universe import error

logger = logging.getLogger(__name__)

def path(*args):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *args))

class FlashgamesLauncher(object):
    def __init__(self, env_id, integrator_mode=False):
        self.env_id = env_id
        self.integrator_mode = integrator_mode
        self.selenium_wrapper = selenium_wrapper.SeleniumWrapperClient(self.env_id)

        if self.env_id is not None:
            self.controlplane_spec = gym_controlplane.spec(self.env_id)
            self.private_directory = path('build/private', self.controlplane_spec.id)
            self.url = self.controlplane_spec.serve_url
            if self.integrator_mode:
                self.url += '?integrator=y'
        else:
            self.controlplane_spec = None
            self.private_directory = None
            self.url = 'http://localhost'

    def healthcheck(self):
        return self.selenium_wrapper.healthcheck()

    def reset(self):
        # Download any needed statics (really only need to do once)
        if self.controlplane_spec is not None and not self.integrator_mode:
            self._git_lfs_pull()

        # Set up the firewall rules. Must precede launching the browser.
        subprocess.check_call(['sudo', '/usr/local/bin/sudoable-env-setup', self.env_id or 'none'])

        for i in range(10):
            launched = self._reset_core(i)
            if launched:
                break
        else:
            raise error.Error('Failed to start environment with 10 consecutive attempts. Probably not going to happen.')

    def _reset_core(self, i):
        # Idempotent, soft reset underbelly: sets up the Chrome and
        # runs the start macro. It can fail a lot.
        logger.info('[%s] Launching new Chrome process (attempt %d/%d)', utils.thread_name(), i, 10)
        if i < 5:
            timeout = 15
        else:
            # Allow for a longer timeout if we haven't come up after 5
            # consecutive attempts.
            timeout = None
        launched = self.selenium_wrapper.launch_browser(timeout=timeout)
        if launched is None:
            return False

        logger.info('[%s] Navigating browser to url=%s', utils.thread_name(), self.url)
        self.selenium_wrapper.set_location(self.url)
        return True

    def _git_lfs_pull(self):
        subprocess.check_call(['sudo', '/usr/local/bin/sudoable-env-setup', 'git-lfs', self.controlplane_spec.id])
        completion_file = os.path.join('/usr/local/openai/git-lfs', self.controlplane_spec.id)
        assert os.path.exists(completion_file), "No such file: {}".format(completion_file)

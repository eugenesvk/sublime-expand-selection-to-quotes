import os
import traceback
from typing import Any, Dict, Tuple

import sublime, sublime_plugin

# package = None
PACKAGE_NAME  = "Expand Selection to Quotes"
cfgU_settings = (f'{PACKAGE_NAME}.sublime-settings')

try: # no access to ST APIs before plugin_loaded is called, so catch import errors here and handle them later
  _e_startup = None
  from . import cfg
except Exception as e:  # pragma: no cover
  traceback.print_exc()
  _e_startup = e

def plugin_loaded():
  _e_load = None 

  try:
    cfg.cfgU.load()
  except Exception as e:
    traceback.print_exc()
    _e_load = e

  if _e_startup or _e_load:
    print(f'❗ {PACKAGE_NAME}: {_e_startup if _e_startup else _e_load}')

def plugin_unloaded():
  pass

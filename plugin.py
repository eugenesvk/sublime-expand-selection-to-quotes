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

  # global package
  # package_path = os.path.dirname (os.path.abspath(__spec__.origin))
  # if   os.path.isfile(package_path): # Package is a .sublime-package, so get its filename
  #   package, _ = os.path.splitext(os.path.basename(package_path))
  # elif os.path.isdir( package_path): # Package is a dir             , so get its basename
  #   package = os.path.basename(package_path)
  # on_settings_change(__name__, lambda: colors.clear())

  try:
    cfg.cfgU.load()
  except Exception as e:
    traceback.print_exc()
    _e_load = e

  if _e_startup or _e_load:
    print(f'❗ {PACKAGE_NAME}: {_e_startup if _e_startup else _e_load}')

def plugin_unloaded():
  pass

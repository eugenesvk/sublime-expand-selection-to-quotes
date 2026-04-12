import sublime, sublime_plugin

import logging

DEFAULT_LOG_LEVEL = logging.WARNING
_log = logging.getLogger(__name__)
_log.setLevel(DEFAULT_LOG_LEVEL)

from typing import Union
import threading

class Singleton(type): # doesn't deadlock: if both Class_1 and Class_2 implement old singleton pattern, calling the constructor of Class_1 in Class_2 (or vice versa) would dead-lock since all the classes implemented through that meta-class share the same lock
  def __new__(mcs, name, bases, attrs): # Assume target class is created (=this method to be called) in the main thread
    cls = super(Singleton, mcs).__new__(mcs, name, bases, attrs)
    cls.__shared_instance__ = None
    cls.__shared_instance_lock__ = threading.Lock() # class implementing primitive lock objects. It allows the thread running our code to be the only thread accessing the code within the lock's context manager (cls._lock block), so long as it holds the lock
    return cls
  def __call__(cls, *args, **kwargs):
    if         cls.__shared_instance__ is None: # check twice to avoid the edge case when 2 classes are created (alternative is to wrap it in a lock, but it's expensive):
      # 1. cls._instance is None in this thread
      # 2. another thread is about to call cls._instance = super(Singleton, cls).__new__(cls)
      with     cls.__shared_instance_lock__: # another thread could have created the instance before we acquired the lock. So check that the instance is still nonexistent
        if not cls.__shared_instance__:
          cls     .__shared_instance__ = super(Singleton, cls).__call__(*args, **kwargs)
    return     cls.__shared_instance__

DEF = dict()
DEF['q=' ] = ('"', "'", "`")
DEF['qp' ] = (("«","»"), ("‹","›"), ("‘","’"), ("‛","’"), ("“","”"), ("‟","”"), ("„","“"), ("🙶","🙷"))
DEF['esc'] = ['constant.character.escape',] # List of scope names for quotes acting as escape chars (ignore these)
  # esc+ ¦ esc-   in user config adds/removes extra scopes without fully replacing the list
DEF['str'] = ['meta.string','string.quoted.single','string.quoted.double',] # List of scope names for strings (limit quote matching to text within these)
  # str+ ¦ str-   in user config adds/removes extra scopes without fully replacing the list
DEF['str_b'] = ["punctuation.definition.string.begin"] # List of scope names for string begin
DEF['str_e'] = ["punctuation.definition.string.end"  ] # …                              end
DEF['cmt'] = ['comment.line','comment.block',] # List of scope names for comments (limit quote matching to text within these)
  # cmt+ ¦ cmt-   in user config adds/removes extra scopes without fully replacing the list

import copy
class cfgU(metaclass=Singleton):
  C = dict()
  c_types        = {'q=':list,'qp':list,'esc':list,'str':list,'cmt':list,'str_b':list,'str_e':list,}
  c_types_add_rm = {          'qp':list,'esc':list,'str':list,'cmt':list,'str_b':list,'str_e':list,}

  @staticmethod
  def load() -> None:
    """load user config file to a global class and add a watcher event to track changes"""
    cfgU.C = copy.deepcopy(DEF) # copy defaults to be able to reset values on config reload
    try:
      from .plugin import  PACKAGE_NAME, cfgU_settings
      setU = sublime.load_settings(cfgU_settings)
      setU.clear_on_change(PACKAGE_NAME)
      setU.add_on_change  (PACKAGE_NAME, lambda: cfgU.reload())
    except FileNotFoundError:
      _log.info(f'‘{cfgU_settings}’ file not found')
    except Exception as e:  # pragma: no cover
      _log.warn(f"‘{cfgU_settings}’ couldn't be loaded 𝑒: {e}")
    cfgU.add_rm(cfgU.C, setU)

  @staticmethod
  def add_rm(src, dst) -> None:
    for k,T in cfgU.c_types.items():
      if k in dst:
        if type(val := dst.get(k)) is T:
          src[k] = val
        else: _log.warn(f"‘{k}’ key should be {T}, not {type(val)}, from ‘{cfgU_settings}’")

    for k,T in cfgU.c_types_add_rm.items():
      if (k_sfx:=k+'+') in dst:
        if type(val := dst.get(k_sfx)) is T:
          src[k] += val
        else: _log.warn(f"‘{k}’ key should be {T}, not {type(val)}, from ‘{cfgU_settings}’")
      if   (k_sfx:=k+'-') in dst\
        or (k_sfx:=k+'−') in dst: #real minus
        if type(val := dst.get(k_sfx)):
          if val in src[k]:
            src[k].remove(val)
        else: _log.warn(f"‘{k}’ key should be {T}, not {type(val)}, from ‘{cfgU_settings}’")

  @staticmethod
  def unload() -> None: # clear watcher
    cfgU.C = copy.deepcopy(DEF) # reset defaults
    try:
      from .plugin import  PACKAGE_NAME, cfgU_settings
      setU.clear_on_change(PACKAGE_NAME)
    except Exception as e:  # pragma: no cover
      _log.info(f"‘{cfgU_settings}’ couldn't be unloaded")

  @staticmethod
  def reload() -> None:
    # _log.debug('reloading %s', _file_path())
    cfgU.unload()
    cfgU.load()

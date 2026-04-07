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
DEF['q_same'      ] = ('"', "'", "`")
DEF['q_paired'    ] = (("«","»"), ("‹","›"), ("‘","’"), ("‛","’"), ("“","”"), ("‟","”"), ("„","“"), ("🙶","🙷"))
DEF['esc_fallback'] = {'c':'\\', 'sym':['"',"'"]},
DEF['esc'] = {
  # since escape char is a quote ↓ incluce non-quotes to exclude ` from matches
  'source.ahk'  : {'c':'`' , 'sym':['"',"'","`", ";",":","{","n","r","b","t","s","v","a","f",]},
  'source.ahk.1': {'c':'`' , 'sym':['"',"'","`", ";",":","{","n","r","b","t","s","v","a","f",]},
  'source.ahk.2': {'c':'`' , 'sym':['"',"'","`", ";",":","{","n","r","b","t","s","v","a","f",]},
  'source.python':{'c':'\\', 'sym':['"',"'"]}, #ignore non quotes: \n \ a b f n N{name} r t uxxxx Uxxxxxxxx v ooo xhh
}
DEF['esc_self_fallback'] = {'':('',)}
DEF['esc_self'] = { # languages that allow repeated quotes to escape themselves
  'source.ahk.1':('"',"'"),
}
DEF['esc_scope' ] = ['constant.character.escape',] # List of scope names for quotes acting as escape chars (ignore these)
  # esc_scope+ ¦ esc_scope-   in user config adds/removes extra scopes without fully replacing the list

import copy
class cfgU(metaclass=Singleton):
  C = dict()

  @staticmethod
  def load() -> None:
    """load user config file to a global class and add a watcher event to track changes"""
    cfgU.C = copy.deepcopy(DEF) # copy defaults to be able to reset values on config reload
    try:
      from .plugin import  PACKAGE_NAME, cfgU_settings
      setU = sublime.load_settings(cfgU_settings)
      setU.clear_on_change(PACKAGE_NAME)
      setU.add_on_change  (PACKAGE_NAME, lambda: cfgU.reload())
      for k,T in {'q_same':list,'q_paired':list,'esc_fallback':dict,'esc_self_fallback':list,'q_same':list,'esc_scope':list,}.items():
        if k in setU:
          if type(val := setU.get(k)) is T:
            cfgU.C[k] = val
          else: _log.warn(f"‘{k}’ key should be {T}, not {type(val)}, from ‘{cfgU_settings}’")
      T = list
      if (k:='esc_scope+') in setU:
        if type(val := setU.get(k)) is T:
          cfgU.C[k.rstrip('+')] += val
        else: _log.warn(f"‘{k}’ key should be {T}, not {type(val)}, from ‘{cfgU_settings}’")
      if (k:='esc_scope-') in setU:
        if type(val := setU.get(k)) is T:
          cfgU.C[k.rstrip('-')].remove(val)
        else: _log.warn(f"‘{k}’ key should be {T}, not {type(val)}, from ‘{cfgU_settings}’")
      for k,T in {'esc':dict,'esc_self':dict,}.items(): # ST settings collate/cascade ≠ .update, but replace ≝top-level keys, so no granular updates → don't use .sublime-settings within the package
        if k in setU:
          if type(val := setU.get(k)) is T:
            cfgU.C[k].update(val)
          else: _log.warn(f"‘{k}’ key should be {T}, not {type(val)}, from ‘{cfgU_settings}’")
    except FileNotFoundError:
      _log.info(f'‘{cfgU_settings}’ file not found')
    except Exception as e:  # pragma: no cover
      _log.warn(f"‘{cfgU_settings}’ couldn't be loaded 𝑒: {e}")

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

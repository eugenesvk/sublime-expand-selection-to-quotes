# Install `UnitTesting`
# Run `UnitTesting: Test Current File`/`Package`
import os, re
from unittesting import DeferrableViewTestCase

import sublime

# from ..plugin import PACKAGE_NAME, cfgU_settings # fails relative import with an unknown package
# import PackageName.module as module # would work, but we have spaces in package name
PACKAGE_NAME  = "Expand Selection to Quotes"
cfgU_settings = (f'{PACKAGE_NAME}.sublime-settings')

version = sublime.version()

class TestUndo(DeferrableViewTestCase):
  def setUp(self):
    # self.view = sublime.active_window().new_file(syntax='Python.sublime-syntax') # Flashes with async tests
    (self.view,self.vin) = sublime.active_window().create_io_panel(name=PACKAGE_NAME, on_input=None, unlisted=True)
    self.view.assign_syntax('Python.sublime-syntax')
    self.view.set_scratch(True)
    cfg = sublime.load_settings("Preferences.sublime-settings")
    cfg.set("close_windows_when_empty", False)
    cfgU = sublime.load_settings(cfgU_settings)
    cfgU.set("q=",["\"","'","`"])
    cfgU.set("qp", [
      ["`'", "'"],
      [ "'","`'"],
      ["¦+","+¦"] ])

  def tearDown(self):
    if (view := self.view):
      view.set_scratch(True)
      # view.window().run_command("close_file")
      sublime.active_window().destroy_output_panel(name=PACKAGE_NAME)

  def setText(self, string):
    self.view.run_command("select_all")
    self.view.run_command("right_delete")
    self.view.run_command("insert", {"characters":string})

  def test_all(self):
    test_set = {
      'b1=e1' : {
        'txt' :R'''"aaa'____'⎀'____'aaaa"''',  'qb': "'", 'qe': "'", 'qp':False,
        False :   " 5  43   212   34   5 "  ,
        True  :   "3   2    1 1    2    3"  ,  },
    }
    view = self.view
    sels = view.sel()
    flit = sublime.FindFlags.LITERAL

    for name,set_i in test_set.items():
      self.setText(set_i['txt'])

      for inc in [False, True]:
        print(f"{'✓ in' if inc else '✗ ex'}clude quotes {'in' if inc else 'from'} selection")
        for sel in sels:
          sels.subtract(sel)
        caret = view.find('⎀',0,flit)
        sels.add(caret.begin())
        pos = set_i[inc]; pos_valid = sorted(set(re.sub(r'[^\d]','',pos)))

        lb = len(set_i['qb'])
        le = len(set_i['qe'])
        for pos_i in pos_valid:
          view.run_command("expand_selection_to_quotes",{"qp":set_i['qp'],"inc":inc})
          yield #100
          m_i = [m.start() for m in re.finditer(pos_i, pos)]
          beg   =  m_i[0]        ; end   = (beg if len(m_i) == 1 else m_i[1]) + 1
          beg_s = sels[0].begin(); end_s = sels[0].end()
          print(f"{pos_i} → {m_i}  i ≟ s: beg {beg}{'=' if beg == beg_s else '≠'}{beg_s} ¦ end {end}{'=' if end == end_s else '≠'}{end_s}")
          self.assertEqual(beg_s, beg); self.assertEqual(end_s, end)
        print(f"   UNDO")
        for pos_i in reversed(pos_valid[:-1]):
          view.run_command("soft_undo")
          yield #100
          m_i = [m.start() for m in re.finditer(pos_i, pos)]
          beg   =  m_i[0]        ; end   = (beg if len(m_i) == 1 else m_i[1]) + 1
          beg_s = sels[0].begin(); end_s = sels[0].end()
          print(f"{pos_i} → {m_i}  i ≟ s: beg {beg}{'=' if beg == beg_s else '≠'}{beg_s} ¦ end {end}{'=' if end == end_s else '≠'}{end_s}")
          self.assertEqual(beg_s, beg); self.assertEqual(end_s, end)

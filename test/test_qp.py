import os, re
from unittest import TestCase

import sublime

# from ..plugin import PACKAGE_NAME, cfgU_settings # fails relative import with an unknown package
# import PackageName.module as module # would work, but we have spaces in package name
PACKAGE_NAME  = "Expand Selection to Quotes"
cfgU_settings = (f'{PACKAGE_NAME}.sublime-settings')

version = sublime.version()

class TestQuotePaired(TestCase):
  def setUp(self):
    self.view = sublime.active_window().new_file(syntax='Python.sublime-syntax')
    cfg = sublime.load_settings("Preferences.sublime-settings")
    cfg.set("close_windows_when_empty", False)
    cfgU = sublime.load_settings(cfgU_settings)
    cfg.set("qp", [
      ["`'", "'"],
      [ "'","`'"],
      ["¦+","+¦"] ])

  def tearDown(self):
    if (view := self.view):
      view.set_scratch(True)
      view.window().run_command("close_file")

  def setText(self, string):
    self.view.run_command("insert", {"characters":string})

  def getRow(self, row):
    return self.view.substr(self.view.line(self.view.text_point(row - 1, 0)))

  def test_all(self):
    test_set = {
      'b1=e1' : {
        'txt' :R'''"aaa'____'⎀'____'aaaa"''',  'qb': "'", 'qe': "'", 'qp':False,
        False :   " ⁵  ⁴³   ²¹²   ³⁴   ⁵ "  ,
        True  :   "³   ²    ¹ ¹    ²    ³"  ,  },
      'b2≠e1' : {
        'txt' :R'''"aa`'___`'⎀'____'aaaa"''',  'qb':"`'", 'qe': "'", 'qp':True ,
        False :   " ⁵ ⁴ ³  ² ¹²   ³⁴   ⁵ "  ,
        True  :   "³  ²    ¹  ¹    ²    ³"  ,  },
      'b1≠e2' : {
        'txt' :R'''"aaa'____'⎀`'___`'aaa"''',  'qb': "'", 'qe':"`'", 'qp':True ,
        False :   " ⁵  ⁴³   ²¹ ²  ³ ⁴  ⁵ "  ,
        True  :   "³   ²    ¹  ¹    ²   ³"  ,  },
      'b2≠e2' : {
        'txt' :R'''"aa¦+___¦+⎀+¦___+¦aaa"''',  'qb':"¦+", 'qe':"+¦", 'qp':True ,
        False :   " ⁵ ⁴ ³  ² ¹ ²  ³ ⁴  ⁵ "  ,
        True  :   "³  ²    ¹   ¹    ²   ³"  ,  },
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
        pos = set_i[inc]; pos_valid = set(pos.replace(' ',''))

        lb = len(set_i['qb'])
        le = len(set_i['qe'])
        for pos_i in '¹²³⁴⁵':
          if not pos_i in pos_valid: continue
          view.run_command("expand_selection_to_quotes",{"qp":set_i['qp'],"inc":inc})
          m_i = [m.start() for m in re.finditer(pos_i, pos)]
          beg   =  m_i[0]        ; end   = (beg if len(m_i) == 1 else m_i[1]) + le
          beg_s = sels[0].begin(); end_s = sels[0].end()
          print(f"{pos_i} → {m_i}  i ≟ s: beg {beg}{'=' if beg == beg_s else '≠'}{beg_s} ¦ end {end}{'=' if end == end_s else '≠'}{end_s}")
          self.assertEqual(beg_s, beg); self.assertEqual(end_s, end)

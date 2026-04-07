# Install `UnitTesting`
# Run `UnitTesting: Test Current File`/`Package`
import os, re
from unittest import TestCase

import sublime

# from ..plugin import PACKAGE_NAME, cfgU_settings # fails relative import with an unknown package
# import PackageName.module as module # would work, but we have spaces in package name
PACKAGE_NAME  = "Expand Selection to Quotes"
cfgU_settings = (f'{PACKAGE_NAME}.sublime-settings')

version = sublime.version()

md_string = R"""
```ahk
____________________________________
'⎀←¹ this should not break because …
```
```ahk
a = '…←² this is separated by a different language scope
```
"""
md_pos = R"""
```ahk
____________________________________
'1
"""


class TestString(TestCase):
  def setUp(self):
    self.view = sublime.active_window().new_file(syntax='Markdown.sublime-syntax')
    cfg = sublime.load_settings("Preferences.sublime-settings")
    cfg.set("close_windows_when_empty", False)
    cfgU = sublime.load_settings(cfgU_settings)
    cfgU.set("q=", ["\"","'","`"])
    cfgU.set("qp", [
      "«»", "‹›",
      "‘’", "‛’",
      "“”", "‟”", "„“",
      ["🙶","🙷"] , # use [open close] list if opening is `'2 chars or Python fails to parse 2 chars as 2
      ["`'","'"],
      ["'","`'"],
      ["¦+","+¦"],
      ])

  def tearDown(self):
    if (view := self.view):
      view.set_scratch(True)
      view.window().run_command("close_file")

  def setText(self, string):
    self.view.run_command("select_all")
    self.view.run_command("right_delete")
    self.view.run_command("insert", {"characters":string})

  def test_all(self):
    test_set = {
      'no_break_scope' : {
        'txt' :md_string,  'qb': "'", 'qe': "'", 'qp':False, 'is_fail':True,
        False :md_pos  ,
        True  :md_pos  , },
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
          m_i = [m.start() for m in re.finditer(pos_i, pos, re.M)]
          beg   =  m_i[0]        ; end   = (beg if len(m_i) == 1 else m_i[1]) + (0 if set_i['is_fail'] else 1)
          beg_s = sels[0].begin(); end_s = sels[0].end()
          print(f"{pos_i} → {m_i}  i ≟ s: beg {beg}{'=' if beg == beg_s else '≠'}{beg_s} ¦ end {end}{'=' if end == end_s else '≠'}{end_s}")
          self.assertEqual(beg_s, beg); self.assertEqual(end_s, end)

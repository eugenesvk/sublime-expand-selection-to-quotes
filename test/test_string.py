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

class TestString(TestCase):
  def setUp(self):
    self.view = sublime.active_window().new_file(syntax='Python.sublime-syntax')
    cfg = sublime.load_settings("Preferences.sublime-settings")
    cfg.set("close_windows_when_empty", False)
    cfgU = sublime.load_settings(cfgU_settings)
    cfgU.set("q=", ["\"","'"])
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
      'no_break' : {
        'txt' :R''''test' + "•this ⎀ shouldn't break _____________________________________ •"''',  'qb': "'", 'qe': "'", 'qp':False,
        #               ↑    shorter        ↑
        #               ↑    vs                                                             ↑
        #            but    "" string scope limits search scope
        False :   "          1                                                             1 "  ,
        True  :   "         1                                                               1"  , },
      'b' : {
        'txt' :R''''test' + "    '•⎀ txt•'"''',  'qb': "'", 'qe': "'", 'qp':False,
        False :   "               1     1  "  ,
        True  :   "              1       1 "  , },
      'c' : {
        'txt' :R"""'•Single quoted selected, \"\' esc⎀ped \'\" quotes ignored •'""",  'qb': "'", 'qe': "'", 'qp':False,
        #                        meta.string ↑↑↑↑ string.quoted.single  constant.character.escape
        #                        meta.string ↓↓↓↓ string.quoted.double  constant.character.escape
        False :   " 1                                                         1 "  ,
        True  :   "1                                                           1"  , },
      'd' : {
        'txt' :R'''"•Double quoted selected, \"\' esc⎀ped \'\" quotes ignored •"''',  'qb': "'", 'qe': "'", 'qp':False,
        False :   " 1                                                         1 "  ,
        True  :   "1                                                           1"  , },
      'e' : {
        'txt' :R"""'•Ignore shorter pair of →" ⎀•'  +  '"← because this is a different string'""",  'qb': "'", 'qe': "'", 'qp':False,
        False :   " 1                           1                                             "  ,
        True  :   "1                             1                                            "  , },
      'f' : {
        'txt' :R"""'•Ignore shorter pair of →‟ ⎀•'  +  '”← because this is a different string'""",  'qb': "'", 'qe': "'", 'qp':True,
        False :   " 1                           1                                             "  ,
        True  :   "1                             1                                            "  , },
      'g' : {
        'txt' :R"""' Select …       …       →‟•⎀       •”←               the same      …     '""",  'qb': "'", 'qe': "'", 'qp':True,
        False :   "                           1        1                                      "  ,
        True  :   "                          1          1                                     "  , },
      'h' : {
        'txt' :R"""'•qp=F     ignore →‟  ⎀  ” ←ignore •'""",  'qb': "'", 'qe': "'", 'qp':False,
        False :   " 1                                 1 "  ,
        True  :   "1                                   1"  , },
      'i' : {
        'txt' :R"""' qp=T     include→‟• ⎀ •” ←include  '""",  'qb': "'", 'qe': "'", 'qp':True,
        False :   "                    1   1             "  ,
        True  :   "                   1     1            "  , },
      'j' : {
        'txt' :R"""' qp=F inc=T ignore →‟  ⎀  ” ←ignore  '""",  'qb': "'", 'qe': "'", 'qp':False,
        False :   " 1                                   1 "  ,
        True  :   "1                                     1"  , },
      'k' : {
        'txt' :R"""' qp=T inc=T include→‟  ⎀  ” ←include '""",  'qb': "'", 'qe': "'", 'qp':True,
        False :   "                      1   1            "  ,
        True  :   "                     1     1           "  , },
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
        pos = set_i[inc]; pos_valid = sorted(set(pos.replace(' ','')))

        lb = len(set_i['qb'])
        le = len(set_i['qe'])
        for pos_i in pos_valid:
          view.run_command("expand_selection_to_quotes",{"qp":set_i['qp'],"inc":inc})
          m_i = [m.start() for m in re.finditer(pos_i, pos)]
          beg   =  m_i[0]        ; end   = (beg if len(m_i) == 1 else m_i[1]) + 1
          beg_s = sels[0].begin(); end_s = sels[0].end()
          print(f"{pos_i} → {m_i}  i ≟ s: beg {beg}{'=' if beg == beg_s else '≠'}{beg_s} ¦ end {end}{'=' if end == end_s else '≠'}{end_s}")
          self.assertEqual(beg_s, beg); self.assertEqual(end_s, end)

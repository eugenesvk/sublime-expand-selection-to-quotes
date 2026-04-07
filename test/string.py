a = 'test' + "←this ⎀ shouldn't break _____________________________________ →"
#        ←    shorter        →
#vs          ←                                                              →
#but         "" string scope limits search scope
b = 'test' + "    '←⎀ txt→'"

c = '←Single quoted selected, \"\' esc⎀ped \'\" quotes ignored →'
  #               meta.string ↑↑↑↑ string.quoted.single  constant.character.escape
  #               meta.string ↓↓↓↓ string.quoted.double  constant.character.escape
d = "←Double quoted selected, \"\' esc⎀ped \'\" quotes ignored →"

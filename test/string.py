a = 'test' + "←this ⎀ shouldn't break _____________________________________ →"
#        ←    shorter        →
#vs          ←                                                              →
#but         "" string scope limits search scope
b = 'test' + "    '←⎀ txt→'"
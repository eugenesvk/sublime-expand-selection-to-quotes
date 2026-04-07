#Requires AutoHotKey 2.1
syntax_test() {
  a:=1
  MsgBox("•from here ⎀ `"•" a " escape char")
  MsgBox("•from here ⎀  `"" a " escape char")
  MsgBox('•from here ⎀ `'•' a " escape char")
  MsgBox('•from here ⎀  `'' a " escape char")
  MsgBox('•f`b `` ⎀ `"" `'•' a "←`` acting as an escape char is skipped")
  MsgBox('•           "⎀  •' a '"inner double quote skipped')
  ;                   ↑ shorter↑ but
  ;                  …↑ is inside a 'string', which limits search scope
}

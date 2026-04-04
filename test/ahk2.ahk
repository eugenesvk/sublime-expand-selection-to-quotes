#Requires AutoHotKey 2.1
; Test ` escape char
f3:: {
  a:=1
  MsgBox("‹from here ⎀ `"›" a " is: ")
  ;       ↑——————————————↑
  ;       ↓——————————————↓
  MsgBox("‹from here ⎀  `"" a " is: ")
  MsgBox('‹from here ⎀ `'›' a " is: ")
  MsgBox('‹from here ⎀  `'' a " is: ")
}

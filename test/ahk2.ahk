#Requires AutoHotKey 2.1
; Test ` escape char
f3:: {
  a:=1
  MsgBox("‹from here ⎀ `"›" a " is: ")
  ;       ↑——————————————↑
  MsgBox("‹from here ⎀  `"" a " is: ")
  MsgBox('‹from here ⎀ `'›' a " is: ")
  MsgBox('‹from here ⎀  `'' a " is: ")
  MsgBox('‹f`b `` ⎀ `"" `'' a "←`` acting as an escape char is skipped")
  ;                    ↓——————↓
  MsgBox('‹f`b ``   `""⎀ `'' a "←but inner quote isn't ignored as the plugin is not fully string-aware")
}

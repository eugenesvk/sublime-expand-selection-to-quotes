#Requires AutoHotKey 1.0
; Test double quotes escaping themselves
f3::
  a:=1
  MsgBox % "‹from here ⎀ ""›" . a . " is: "
  ;         ↑——————————————↑
  ;         ↓——————————————↓
  MsgBox % "‹from here ⎀  """ . a . " is: "

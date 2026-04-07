#Requires AutoHotKey 1.0
syntax_test() {
  a:=1
  MsgBox % "•from here ⎀ ""•" . a . " double quotes escaping themselves"
  MsgBox % "•from here ⎀  """ . a
}

# ahk-script-gen.py generates a autohotkey script that provides several useful
# keyboard and mouse bindings.
#
# Refer to the comments in the generate script for details on the bindings.


BASE_TEMPLATE = '''\
#persistent

;; Remove line breaks when copying from Adobe Acrobat and SumatraPDF
OnClipboardChange:
  if WinActive("ahk_class AcrobatSDIWindow") or WinActive("ahk_class SUMATRA_PDF_FRAME")
  {{
    StringReplace, clipboard, clipboard, `r`n`r`n, "${{doubleLineBreak}}", All
    StringReplace, clipboard, clipboard, `r`n, %A_Space%, All
    StringReplace, clipboard, clipboard, "{{doubleLineBreak}}", `r`n, All
  }}
return

{GENERATED_SECTION}

;; Holding down "forward" mouse side button and scrolling up and down sends Up
;; and Down key presses.
XButton2 & WheelUp::Send {{Up}}
XButton2 & WheelDown::Send {{Down}}

;; Pressing both side buttons on the mouse sends an Enter key press.
XButton2 & XButton1::Send {{Return}}

;; Holding down the "back" mouse side button and scrolling down cycles through
;; Alt-Tab menu.
XButton1 & WheelDown::AltTab

;; Pressing the "back" mouse side button sends Alt + Tab, switching to previous
;; window.
XButton1::Send {{Alt down}}{{Tab down}}{{Alt up}}

;; Holding down the "back" mouse side button and left-clicking sends
;; Control + z, undoing an operation. Right-clicking sends Control + y, redoing
;; an operation.
XButton1 & LButton::Send {{Ctrl down}}z{{Ctrl up}}
XButton1 & RButton::Send {{Ctrl down}}y{{Ctrl up}}

;; Holding down the "forward" mouse side button and left-clicking sends
;; Control + c, copying the selection. Right-clicking sends Control + p,
;; pasting the item on clipboard.
XButton2 & LButton::Send {{Ctrl down}}c{{Ctrl up}}
XButton2 & RButton::Send {{Ctrl down}}v{{Ctrl up}}

;; Alt + Shift + D enters the current date (e.g., 20160808).
!+d::
  FormatTime, CurrentDateTime, A_NOW, yyyyMMdd
  SendInput %CurrentDateTime%
return

;; Ctrl + Alt + Shift + B makes that active window borderless.
^!+b::
  WinSet, Style, ^0xC00000, A ;removes title bar ^ is a toggle
  WinSet, Style, ^0x40000, A ;removes resize border ^ is a toggle
return

;; Ctrl + Alt + Shift + Z makes that active window borderless and always on top.
^!+z::
  WinSet, AlwaysOntop, Toggle, A
  WinSet, Style, ^0xC00000, A ;removes title bar ^ is a toggle
  WinSet, Style, ^0x40000, A ;removes resize border ^ is a toggle
return
'''

def main():

  generated_section = generate_bindings()
  print(BASE_TEMPLATE.format(GENERATED_SECTION=generated_section))


def generate_bindings():

  BINDING_TEMPLATE = ('Enter & {KEY}::Send {{Ctrl down}}{KEY}{{Ctrl Up}}\n'
                      'CapsLock & {KEY}::Send {{Ctrl down}}{KEY}{{Ctrl Up}}')
  SECTION_HEADING = '''\
;; Ugly hack to rebind Enter key to Control when pressed together with
;; alphabets and numeric keys, but functions as normal Enter key when pressed
;; alone or with Alt and/or Control keys.
;; Doesn't support Control + Shift + <key>.
;; Doesn't support Control + Tab.\
'''

  bindings = [SECTION_HEADING]

  for key in 'abcdefghijklmnopqrstuvwxyz1234567890':
    bindings.append(BINDING_TEMPLATE.format(KEY=key))

  bindings.append('$Enter::Send {Enter} ; Enter key will send Enter when'
                  ' pressed and released by itself')
  bindings.append('$CapsLock::Return ; Disable Capslock key')
  bindings.append("Alt & Enter::Send {Alt down}{Enter}{Alt up}")
  bindings.append("Ctrl & Enter::Send {Ctrl down}{Enter}{Ctrl up}")

  return '\n'.join(bindings)

if __name__ == '__main__':

  main()


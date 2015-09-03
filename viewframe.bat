REM This script allows to view Bruker frames in Windows without starting APEX2
REM Place it in e.g. c:\program files\ and associate it with the .sfrm file ending. 
REM Now you can view frames in a fraction of a second.

C:\bn\Tools\frm2frm.exe %1 /F:5 /OUT:%TMP%\view.jpg /A /B /T
mspaint.exe %TMP%\view.jpg


rem D:\programme\IrfanView\i_view32.exe %TMP%\view.jpg 
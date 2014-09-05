rem This script allows to view Bruker frames in Windows without starting APEX2
rem Dieses skript ermoeglich das betrachten von Bruker Frames

C:\bn\Tools\frm2frm.exe %1 /F:5 /OUT:%TMP%\view.jpg /A /B /T

rem D:\programme\IrfanView\i_view32.exe %TMP%\view.jpg 

mspaint.exe %TMP%\view.jpg


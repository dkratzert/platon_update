
rem ----------------------------------------------------------------------------
rem  "THE BEER-WARE LICENSE" (Revision 42):
rem  <dkratzert@gmx.de> wrote this file. As long as you retain this notice you
rem  can do whatever you want with this stuff. If we meet some day, and you think
rem  this stuff is worth it, you can buy me a beer in return Daniel Kratzert.
rem  ----------------------------------------------------------------------------

rem echo off
C:\pwt\platon.exe -o -u %1.cif

if exist %1.chk ( notepad %1.chk 
  exit 0 )
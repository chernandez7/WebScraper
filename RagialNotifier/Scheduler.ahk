#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
#Persistent 
#SingleInstance
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


SetTimer, Caller, 3600000 ; 1 hour
;SetTimer, Caller, 30000 ;  .5 min DEBUGGING PURPOSES
return

Caller:
Run "RagialLookup.exe" "WoE White Potion Box"
return
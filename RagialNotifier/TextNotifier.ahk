#MaxThreads 2

ParameterAmount = %0%
MessageText = %1%

if (ParameterAmount > 1)
{
  MsgBox "Too many parameters! Exiting program"
  return
}

if (ParameterAmount == 0)
{
  MsgBox "Not enough parameters! Exiting program"
  return
}

pmsg 			:= ComObjCreate("CDO.Message")
pmsg.From 		:= "<ragialnotifications@gmail.com>"
pmsg.To 		:= "7733323927@vtext.com"
pmsg.BCC 		:= ""   ; Blind Carbon Copy
pmsg.CC 		:= ""	; Carbon Copy
pmsg.Subject 	:= ""

pmsg.TextBody 	:= MessageText

sAttach   		:= "" ; can add multiple attachments, the delimiter is |

fields := Object()
fields.smtpserver   := "smtp.gmail.com" 
fields.smtpserverport     := 465 ; 25
fields.smtpusessl      := True ; False
fields.sendusing     := 2   ; cdoSendUsingPort
fields.smtpauthenticate     := 1   ; cdoBasic
fields.sendusername := "ragialnotifications@gmail.com"
fields.sendpassword := "chrisbam77"
fields.smtpconnectiontimeout := 60
schema := "http://schemas.microsoft.com/cdo/configuration/"

pfld :=   pmsg.Configuration.Fields

For field,value in fields
	pfld.Item(schema . field) := value
pfld.Update()

Loop, Parse, sAttach, |, %A_Space%%A_Tab%
  pmsg.AddAttachment(A_LoopField)

pmsg.Send()

/*
q::
  $stop := 0
  Loop, 
  { 
  Send 1
    pmsg.Send()
	;pmsg.TextBody 	:= 
    Sleep 100 
    if ($stop)
    {
      return
    }
  }

w:: $stop := 1



randomChars(length) {

   static   c

   if   !c
      Loop, 26
         c .=   (!c ? "" : "`n") Chr(A_Index + 96)
   Loop %   length
   {
      Random, n, 1, 1296
      Loop %   n
         Sort, c, Random
      str .=   SubStr(c,1,1)
   }
   return   str
}
*/
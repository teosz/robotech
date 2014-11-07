def main():
   handle=time=Byte(0)
   i=fsize=numin=Integer()
   
   DeleteFile("int.txt")
   CreateFile("int.txt",4096,handle)
   
   for i in range(1000,10000,1000):
       WriteLn(handle,i)
       
   CloseFile(handle)
   OpenFileRead("int.txt",fsize,handle);
   
   while (ReadLn(handle,numin)==NO_ERR):
       ClearScreen()
       NumOut(30,LCD_LINE5,numin)
       Wait(500)
   
   CloseFile(handle)


def main():
   handle=time=Byte(0)
   i=fsize=numin=Integer()
   numin=Long()
   
   DeleteFile("long.txt")
   CreateFile("long.txt",4096,handle)
   
   for i in range(100000,1000000,50000):
       WriteLn(handle,i)
       
   CloseFile(handle)
   OpenFileRead("long.txt",fsize,handle);
   
   while (ReadLn(handle,numin)==NO_ERR):
       ClearScreen()
       NumOut(30,LCD_LINE5,numin)
       Wait(500)
   
   CloseFile(handle)


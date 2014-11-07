DEFINE FILE_LINES=10

def sub_CreateRandomFile(fname=String(), lines=Integer()):
    handle=Byte()
    s=String()
    n=bytesWritten=Integer()
    DeleteFile(fname)
    fsize=Integer()
    fsize = lines*5
    # create file with random data
    if (CreateFile(fname, fsize, handle) == NO_ERR):
        for repeat in range(FILE_LINES):
            n = Random(0xFF)
            s = NumToStr(n)
            WriteLnString(handle,s,bytesWritten)
      
        CloseFile(handle)


def main():
    handle=Byte()
    buf=String()
    fsize=Integer()
    blah = Integer(0)
    
    

    sub_CreateRandomFile("rand.txt",FILE_LINES)
    if (OpenFileRead("rand.txt", fsize, handle) == NO_ERR):
        TextOut(10,LCD_LINE2,"Filesize:")
        NumOut(65,LCD_LINE2,fsize)
        Wait(600)
        while (not eof): # read the text file till the end
            pass 
        if (ReadLnString(handle,buf) != NO_ERR):
            eof = true
        TextOut(20,LCD_LINE3,buf)
        Wait(500)
    CloseFile(handle)


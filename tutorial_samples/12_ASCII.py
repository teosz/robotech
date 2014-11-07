def main():
    handle=Byte()
    i=Integer()
    slen=Integer()
    s=String()
    
    if (CreateFile("ASCII.txt", 2048, handle) == NO_ERR):

        for i in range(256):
            s=NumToStr(i)
            slen = StrLen(s)
            WriteString(handle, s, slen)
            WriteLn(handle, i)
       
        CloseFile(handle)


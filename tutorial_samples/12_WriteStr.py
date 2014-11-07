DEFINE OK=LDR_SUCCESS


def main():
    
    fileHandle=Byte()
    fileSize=Short()
    bytesWritten=Short()
    
    read=String()
    write=String()
    error=String()
    
    tmp=String()
    
    DeleteFile("Danny.txt")
    DeleteFile("DannySays.txt")
    CreateFile("Danny.txt", 512, fileHandle)
    for i in range(2,10):
        write = "NXT is cool "
        tmp = NumToStr(i)
        write = StrCat(write,tmp," times!")
        WriteLnString(fileHandle,write, bytesWritten)
    
    CloseFile(fileHandle)
    RenameFile("Danny.txt","DannySays.txt")


bbb=ccc=5.0
values=Integer([])

def main():
    aaa = 10
    bbb = 20 * 5
    ccc = bbb
    ccc /= aaa
    ccc -= 5         
    aaa = 10 * (ccc + 3) # aaa is now equal to 80
    ArrayInit(values, 0, 10) # allocate 10 elements = 0
    values[0] = aaa
    values[1] = bbb
    values[2] = aaa*bbb
    values[3] = ccc

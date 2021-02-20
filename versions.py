cubeversion = "f2-1.9.2"
freertosversion = "10.0.1"
lwipversion = "2.0.3"

def freertos():
    return freertosversion + "+" + cubeversion

def lwip():
    return lwipversion + "+" + cubeversion

#hitungan penambahan
print(1+4)
print((1+2)*(4+5))
# hitungan dengan variabel 
a = 10
b = 20
c = a + b
print(c)

#dengan variable teks
a = "hallo"
b = "dunia"
c = a + " " + b
print(c)
#dengan variable uppercase
a = "hallo"
b = "dunia"
c = a + " " + b
print(c.upper())
#dengan variable lowercase
a = "HALLO"
b = "DUNIA"
c = a + " " + b
print(c.lower())
#dengan variable capitalize
a = "hallo"
b = "dunia"
c = a + " " + b
print(c.capitalize())
#dengan variable split
a = "hallo dunia"
b = a.split()
print(b)
#dengan variable split "o"
a = "hallo dunia"
b = a.split("o")
print(b)
#dengan variable split huruf ke 2
a = "hallo dunia"
b = a[4]
print(b)
#dengan variable split huruf ke 2
a = "hallo dunia"
b = a[-1]
print(b)
#dengan variable slice
a = "hallo dunia"
b = a[0:5]
print(b)
#==================================================================================
#dengan variable dictionary
a = {"a":1,"b":2,"c":3}
b = {"d":4,"e":5,"f":6}
# c = {a + b}
print(a)
#dengan variable dictionary
a = {"a":1,"b":2,"c":3}
b = {"d":4,"e":5,"f":6}
# Menggunakan method update() untuk menggabungkan dictionary
e = a.copy()  # Membuat salinan dari dictionary a
e.update(b)   # Menambahkan elemen dari dictionary b ke e
print(e)
a = {"a":1,"b":2,"c":3}
b = {"d":4,"e":5,"f":6}
c = {**a, **b}  # Menggunakan unpacking operator untuk menggabungkan dictionary
print(c)
#=
#dengan variable tuple
a = (1,2,3,4,5)
b = (6,7,8,9,10)
c = a + b
print(c)
#dengan variable list
a = [1,2,3,4,5]
b = [6,7,8,9,10]
c = a + b
print(c)
#dengan variable float
a = 10.5
b = 20.5
c = a + b
print(c)
#dengan variable integer
a = 10
b = 20
c = a + b
print(c)
#dengan variable boolean
a = True
b = False
print(a,b,a+b)

#dengan variable tag
nama_depan = "gusti"
nama_belakang = "permana"
print(nama_depan,nama_belakang)
#percampuran dengan format text
print("hallo",nama_depan,nama_belakang)
print(f"hallo {nama_depan} {nama_belakang}")
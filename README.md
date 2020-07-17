# prova1

class myFloat(float):
    def __new__(cls, value, name, *args, **kwargs):
        return super().__new__(cls, value)
    def __init__(self, value, name):
        float.__init__(value)
        self.name = name`

myVar = []
for i in range(0, 3):
    myVar.append(myFloat(i,'i'))
print(myVar)

class A:
    def __init__(self, attr1, attr2, color):
        self.attr1 = attr1
        self.attr2 = attr2
        self.color = color
    
    @classmethod
    def set_color(cls, color):
        print("ClassMethod Call")
        cls.color = color

class B(A):
    def __init__(self, attr3, attr4, color):
         self.attr3 = attr3
         self.attr4 = attr4
         self.color = color

    def check(self):
        A.set_color(2)

b = B(1,2,3)
b.check()
print(b.color)


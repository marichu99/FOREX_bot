class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def myFunc(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old")
    
p1=Person("Martin",19)
p1.myFunc()

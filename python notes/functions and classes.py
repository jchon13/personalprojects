"""Simple functions"""

def functionName(number):
    """Comment of function purpose"""
    #function code 
    number *= 2
    return number

#print(functionName(10))


"""Simple classes"""
class Vehicle:
    def __init__(self,wheels:int,capacity:float,brightness:float) -> None:
        self.wheels = wheels
        self.capacity = capacity
        self.brightness = brightness
        self.owner = 'Bob'

    def can_drive(self, val:bool) ->bool:
        pass

car = Vehicle(4,5,15)
print(car.capacity)

class Car1(Vehicle):
    def __init__(self,capacity:float,brightness:float,rego:int) -> None:
        Vehicle.__init__(self,4,capacity,brightness)
        self.rego = rego

car_2 = Car1(4,5,515)
print(car_2.capacity)
print(car_2.rego)


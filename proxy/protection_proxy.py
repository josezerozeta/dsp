class Car:
    def __init__(self, car_driver):
        self.driver = car_driver
    
    def drive(self):
        print(f'Car is being driven by {self.driver.name}')
    

class CarProxy:
    def __init__(self, car_driver):
        self.driver = car_driver
        self._car = Car(car_driver)

    def drive(self):
        if self.driver.age >= 16:
            self._car.drive()
        else:
            print('Driver too young')


class Driver:
    def __init__(self, name, age):
        self.age = age
        self.name = name


if __name__ == '__main__':
    driver = Driver('John', 12)
    car = CarProxy(driver)
    car.drive()
        
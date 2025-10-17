import Pyro4

@Pyro4.expose
class Calculator:
    def add_numbers(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

def main():
    daemon = Pyro4.Daemon()  
    uri = daemon.register(Calculator)  
    print("Calculator service is running.")
    print("URI:", uri)  
    daemon.requestLoop()  

if __name__ == "__main__":
    main()

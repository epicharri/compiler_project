
class ReadAndPrint():
    
    @classmethod
    def read(cls):
      read_input = input()
      return read_input.split(" ")[0]
    
    @classmethod
    def print(cls, value):
        print(value)

    
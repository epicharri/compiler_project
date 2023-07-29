
class ReadAndPrint():
    
    @classmethod
    def read(cls):
      read_input = input()
      return read_input # We do not split based on whitespace other than newline.
    
    @classmethod
    def print(cls, value):
        print(value, end="")

    
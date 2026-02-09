class Athlete:
    """""Athlete class representing a player in the tournament"""
    def __init__(self,name):
        self.name = name 
        self.number=0
    def __str__(self):
        return f"Athlete: {self.name}, Number: {self.number}"
    def __repr__(self):
        return f"Athlete(name='{self.name}', number={self.number})"
    def set_number(self, number):
        self.number = number


if __name__ == "__main__":
   Athlete1 = Athlete ("Lionel Andres Messi Cuccitini")
   Athlete1.number = 10
   print(Athlete1)
   print(repr(Athlete1))

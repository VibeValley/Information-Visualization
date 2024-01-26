print('hej')

class Point:
  def __init__(self,x,y,type):
    self.x = x
    self.y= y
    self.type = type

    def __str__(self):
        return f'{self.x}i{self.y:+}j'


# load csv
def load_csv(file):
    data = []
    with open(file, "r") as file:
        for line in file:
            values = line.strip().split(",")
            data.append(Point(
                float(values[0]),
                float(values[1]),
                values[2]
            ))
    return data
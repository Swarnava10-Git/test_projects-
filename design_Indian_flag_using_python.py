import turtle
colours = [ "green","white","red" ]
t = turtle.Pen()
turtle.bgcolor("black")
for i in range(200):
    t.pencolor(colours[i % 3])
    t.width(i/100 +1)
    t.forward(i)
    t.left(59)
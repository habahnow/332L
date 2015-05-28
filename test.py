import sys

def test(gravity, height):
    y = 350
    heights = []
    ys = []
    while y <= 350:
        height = height - gravity
        y = y - (height)
        heights.append(height)
        ys.append(y)
    print('heights')
    print(heights)
    print('ys')
    print(ys)
    ys.sort()
    print(ys)

args = []
for arg in sys.argv:
    args.append(arg)
test(int(args[1]), int(args[2]))


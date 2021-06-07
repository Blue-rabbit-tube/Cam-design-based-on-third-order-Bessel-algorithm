from dxfwrite import DXFEngine as dxf
import math

file=open("凸轮设计结果.csv","rt+")
drawing = dxf.drawing('凸轮设计.dxf')

x_total=[]
y_total=[]

for i in file:
    content=file.readline()
    sp=content[0:-1]
    # print(sp)
    content_num=sp.split(",")
    try:
        x1=math.cos((3.1415926/180)*float(content_num[0]))*float(content_num[1])
        y1=math.sin((3.1415926/180)*float(content_num[0]))*float(content_num[1])
        x_total.append(x1)
        y_total.append(y1)

        # drawing.add(dxf.point((x1,y1)))
        # print(x,y)
    except:
        pass

print((0.0,0.0),(x_total[0],y_total[0]))

drawing.add(dxf.line((0.0,0.0),(x_total[1],y_total[1])))   
for i in range(0,len(x_total)):
    drawing.add(dxf.line((x_total[i-1],y_total[i-1]),(x_total[i],y_total[i])))
    drawing.add(dxf.circle(radius=1.0,center=(0.0,0.0)))
# drawing.add(dxf.line((0, 0), (10, 0), color=7))

# drawing.add_layer('TEXTLAYER', color=2)
# drawing.add(dxf.text('Test', insert=(0, 0.2), layer='TEXTLAYER'))
drawing.save()
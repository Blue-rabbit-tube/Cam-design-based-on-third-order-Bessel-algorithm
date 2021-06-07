import numpy as np
import math
 
def bezier_curve(p0, p1, p2, p3, inserted):
 """
 三阶贝塞尔曲线
  
 p0, p1, p2, p3 - 点坐标，tuple、list或numpy.ndarray类型
 inserted  - p0和p3之间插值的数量
 """
  
 assert isinstance(p0, (tuple, list, np.ndarray)), u'点坐标不是期望的元组、列表或numpy数组类型'
 assert isinstance(p0, (tuple, list, np.ndarray)), u'点坐标不是期望的元组、列表或numpy数组类型'
 assert isinstance(p0, (tuple, list, np.ndarray)), u'点坐标不是期望的元组、列表或numpy数组类型'
 assert isinstance(p0, (tuple, list, np.ndarray)), u'点坐标不是期望的元组、列表或numpy数组类型'
  
 if isinstance(p0, (tuple, list)):
  p0 = np.array(p0)
 if isinstance(p1, (tuple, list)):
  p1 = np.array(p1)
 if isinstance(p2, (tuple, list)):
  p2 = np.array(p2)
 if isinstance(p3, (tuple, list)):
  p3 = np.array(p3)
  
 points = list()
 for t in np.linspace(0, 1, inserted+2):
  points.append(p0*np.power((1-t),3) + 3*p1*t*np.power((1-t),2) + 3*p2*(1-t)*np.power(t,2) + p3*np.power(t,3))
  
 return np.vstack(points)
 
 
def smoothing_base_bezier(date_x, date_y, k=0.5, inserted=10, closed=False):
 """
 基于三阶贝塞尔曲线的数据平滑算法
  
 date_x  - x维度数据集，list或numpy.ndarray类型
 date_y  - y维度数据集，list或numpy.ndarray类型
 k   - 调整平滑曲线形状的因子，取值一般在0.2~0.6之间。默认值为0.5
 inserted - 两个原始数据点之间插值的数量。默认值为10
 closed  - 曲线是否封闭，如是，则首尾相连。默认曲线不封闭
 """
  
 assert isinstance(date_x, (list, np.ndarray)), u'x数据集不是期望的列表或numpy数组类型'
 assert isinstance(date_y, (list, np.ndarray)), u'y数据集不是期望的列表或numpy数组类型'
  
 if isinstance(date_x, list) and isinstance(date_y, list):
  assert len(date_x)==len(date_y), u'x数据集和y数据集长度不匹配'
  date_x = np.array(date_x)
  date_y = np.array(date_y)
 elif isinstance(date_x, np.ndarray) and isinstance(date_y, np.ndarray):
  assert date_x.shape==date_y.shape, u'x数据集和y数据集长度不匹配'
 else:
  raise Exception(u'x数据集或y数据集类型错误')
  
 # 第1步：生成原始数据折线中点集
 mid_points = list()
 for i in range(1, date_x.shape[0]):
  mid_points.append({
   'start': (date_x[i-1], date_y[i-1]),
   'end':  (date_x[i], date_y[i]),
   'mid':  ((date_x[i]+date_x[i-1])/2.0, (date_y[i]+date_y[i-1])/2.0)
  })
  
 if closed:
  mid_points.append({
   'start': (date_x[-1], date_y[-1]),
   'end':  (date_x[0], date_y[0]),
   'mid':  ((date_x[0]+date_x[-1])/2.0, (date_y[0]+date_y[-1])/2.0)
  })
  
 # 第2步：找出中点连线及其分割点
 split_points = list()
 for i in range(len(mid_points)):
  if i < (len(mid_points)-1):
   j = i+1
  elif closed:
   j = 0
  else:
   continue
   
  x00, y00 = mid_points[i]['start']
  x01, y01 = mid_points[i]['end']
  x10, y10 = mid_points[j]['start']
  x11, y11 = mid_points[j]['end']
  d0 = np.sqrt(np.power((x00-x01), 2) + np.power((y00-y01), 2))
  d1 = np.sqrt(np.power((x10-x11), 2) + np.power((y10-y11), 2))
  k_split = 1.0*d0/(d0+d1)
   
  mx0, my0 = mid_points[i]['mid']
  mx1, my1 = mid_points[j]['mid']
   
  split_points.append({
   'start': (mx0, my0),
   'end':  (mx1, my1),
   'split': (mx0+(mx1-mx0)*k_split, my0+(my1-my0)*k_split)
  })
  
 # 第3步：平移中点连线，调整端点，生成控制点
 crt_points = list()
 for i in range(len(split_points)):
  vx, vy = mid_points[i]['end'] # 当前顶点的坐标
  dx = vx - split_points[i]['split'][0] # 平移线段x偏移量
  dy = vy - split_points[i]['split'][1] # 平移线段y偏移量
   
  sx, sy = split_points[i]['start'][0]+dx, split_points[i]['start'][1]+dy # 平移后线段起点坐标
  ex, ey = split_points[i]['end'][0]+dx, split_points[i]['end'][1]+dy # 平移后线段终点坐标
   
  cp0 = sx+(vx-sx)*k, sy+(vy-sy)*k # 控制点坐标
  cp1 = ex+(vx-ex)*k, ey+(vy-ey)*k # 控制点坐标
   
  if crt_points:
   crt_points[-1].insert(2, cp0)
  else:
   crt_points.append([mid_points[0]['start'], cp0, mid_points[0]['end']])
   
  if closed:
   if i < (len(mid_points)-1):
    crt_points.append([mid_points[i+1]['start'], cp1, mid_points[i+1]['end']])
   else:
    crt_points[0].insert(1, cp1)
  else:
   if i < (len(mid_points)-2):
    crt_points.append([mid_points[i+1]['start'], cp1, mid_points[i+1]['end']])
   else:
    crt_points.append([mid_points[i+1]['start'], cp1, mid_points[i+1]['end'], mid_points[i+1]['end']])
    crt_points[0].insert(1, mid_points[0]['start'])
  
 # 第4步：应用贝塞尔曲线方程插值
 out = list()
 for item in crt_points:
  group = bezier_curve(item[0], item[1], item[2], item[3], inserted)
  out.append(group[:-1])
  
 out.append(group[-1:])
 out = np.vstack(out)
  
 return out.T[0], out.T[1]

#计算两点之间的距离
def distance_two_point(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2)) 


#计算一下三点的曲率 应用二次方程 传入x[3]和y[3] 返回
def PJcurvature(x,y):
    
    x21 = x[1] - x[0]
    y21 = y[1] - y[0]
    x32 = x[2] - x[1]
    y32 = y[2] - y[1]
    # three colinear
    if (x21 * y32 - x32 * y21 == 0):
        return 9999999999999999
    xy21 = x[1] * x[1] - x[0] * x[0] + y[1] * y[1] - y[0] * y[0]
    xy32 = x[2] * x[2] - x[1] * x[1] + y[2] * y[2] - y[1] * y[1]
    y0 = (x32 * xy21 - x21 * xy32) / 2 * (y21 * x32 - y32 * x21)
    x0 = (xy21 - 2 * y0 * y21) / (2.0 * x21)
    R = ((x[0] - x0) ** 2 + (y[0] - y0) ** 2) ** 0.5
    
    #x0 y0 为圆心坐标
    
    #可以算出夹角 矢量积
    
    if ((x[2]-x[1])*(y0-y[1])-(x0-x[1])*(y[2]-y[1])) <0:
        R=-R
    
    return R

 

 
 
 
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    file=open("小车轨迹坐标.csv","wt+")
    file_result=open("凸轮设计结果.csv","wt+")
    
    #存放总周长的变量
    total_distance=0
    
    #存放邻近两点间距离
    neighbor_distance=0
    
    #用于计算绝对旋转角
    circle_num_total=0
    
    #文件标题
    file.writelines(str("X"+","+"Y"+","+"相邻点距离"+","+"相邻两点路径长度占总长度的比值"+","+"相邻三点的中心点曲率"+","+"对应凸轮的旋转角度(360)"+","+"摆头转动的角度"+","+"凸轮直径"+"\n"))
    file_result.writelines("对应凸轮的旋转角度(360)(绝对旋转角)"+","+"凸轮直径"+"\n")

    #轨迹坐标点
    y = np.array([275.0,275,550,900,1550,2050,2050,2050,2550,3200,3550,4026.3140,4375,4026.3140,3550,3200,2550,2050,2050,2050,1550,900 , 550,275 ,275])
    x = np.array([0    ,550,825,550,275 ,275 ,550 ,825 ,825 ,550 ,275 ,275      ,0   ,-275     ,-275,-550,-825,-825,-550,-275,-275,-550,-825,-550,0  ])
    
    #桩子的坐标
    y_pile=[550,0,550,1250,1550,1850,2250,2850,2550,3550,4100,2850,2250,1850,1250,3550,3550]
    x_pile=[0,0,550,550,0,550,550,550,0,0,0,-550,-550,-550,-550,550,-550]
    #绘制桩子
    plt.plot(x_pile,y_pile,'go')   
    #绘制所有轨迹点坐标
    plt.plot(x, y, 'ro')
    
    #测试一下曲率半径算法
    print(PJcurvature([0,1,2],[0,1,2]))
    
    #debug测试点百分比图
    distance_debug=0
    distance_debug_range=0.1
    
    #插值结果
    x_curve, y_curve = smoothing_base_bezier(x, y, k=0.001, closed=False, inserted=1000)
    
    #抢先悄悄计算一下总长度 下面要用
    for i in range(0,len(x_curve)):
        total_distance=total_distance+distance_two_point(x_curve[i],y_curve[i],x_curve[i-1],y_curve[i-1])
    
    #保存插值结果
    for i in range(0,len(x_curve)):
        
        #创建包含三个点的xy_k的数组 用于之后计算斜率
        if(i==len(x_curve)-1):
            x_k=[x_curve[i-1],x_curve[i],x_curve[0]]
            y_k=[y_curve[i-1],y_curve[i],y_curve[0]]
        #排除数组索引溢出的问题
        else:
            x_k=[x_curve[i-1],x_curve[i],x_curve[i+1]]
            y_k=[y_curve[i-1],y_curve[i],y_curve[i+1]]
        
        neighbor_distance=0
        #计算一下相邻两点的间距
        neighbor_distance=distance_two_point(x_curve[i],y_curve[i],x_curve[i-1],y_curve[i-1])
        #计算一下已经进行的行程
        distance_debug=neighbor_distance+distance_debug
        
        if distance_debug/total_distance > distance_debug_range:
            plt.plot(x_curve[i],y_curve[i],"bo")
            distance_debug_range=distance_debug_range+0.1

        
        #凸轮相对应的转动比值
        circle_num=neighbor_distance/total_distance
        #摆头的转角
        # up_cir=(180/3.1415926)*math.atan(265/PJcurvature(x_k,y_k))
        up_cir=(180/3.1415926)*math.atan(265/PJcurvature(x_k,y_k))
        
        if(up_cir>80):
            plt.plot(x_curve[i],y_curve[i],"bo")
        
        #写入文件中去
        file.writelines(str(x_curve[i])+","+str(y_curve[i])+","+str(neighbor_distance)+","+str(circle_num)+","+str(PJcurvature(x_k,y_k))+","+str(circle_num*360)+","+str(up_cir)+","+str(50+up_cir*3.1415926/6)+"\n")
        
        circle_num_total=circle_num_total+circle_num*360
        file_result.writelines(str(circle_num_total)+","+str(50+up_cir*3.1415926/6)+"\n")
        
        for s in range(0,len(x_pile)):
            # 计算每个散点与桩的距离 判断是否碰桩 阈值为135mm
            if(distance_two_point(x_curve[i],y_curve[i],x_pile[s],y_pile[s])<135):
                plt.plot(x_curve[i],y_curve[i])
                plt.text(x_curve[i],y_curve[i],"warning！")
    
    plt.plot(x_curve, y_curve, label='line')

    plt.legend(loc='best')
    
    #标出桩的坐标
    for i in range(0,len(x_pile)):
        plt.text(x_pile[i],y_pile[i],str(i))
    #输出总距离
    print("总距离"+str(total_distance)+"mm")
    #开始展示
    plt.show()
    file.close()
    file_result.close()
    
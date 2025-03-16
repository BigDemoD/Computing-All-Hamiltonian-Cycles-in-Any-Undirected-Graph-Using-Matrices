import numpy as np
import math
import datetime
import  xlwt
import random
import matplotlib.pyplot as plt

# 列合并运算
def hebingyunsuan(a,duijiao,juzhen):
    linshiliebiao = []
    for i in range(a):
        if i ==0:
            linshiliebiao.append(np.column_stack((duijiao,juzhen)))
            
        elif i == a-1:
            linshiliebiao.append(np.column_stack((juzhen[:,:a],duijiao)))
        else:
            linshiliebiao.append(np.column_stack((juzhen[:,:i],duijiao,juzhen[:,i:])))
    return tuple(linshiliebiao)

# 生成a个数的全排列
def quanpailie(a):
    # start = datetime.datetime.now()
    for i in range(1,a+1):
        if i == 1:
            juzhen = np.array([1])
        elif i ==2:
            duijiao = np.full((math.factorial(i-1),1),i)
            juzhen = np.row_stack((np.column_stack((duijiao,juzhen)),np.column_stack((juzhen,duijiao))))
        else:
            # 生成元素值为i的（i-1)！*1矩阵
            duijiao = np.full((math.factorial(i-1),1),i)
            juzhen = np.row_stack(hebingyunsuan(i,duijiao,juzhen))
    # end = datetime.datetime.now()
    # print(str(a)+'号用时: ',(end-start),' us')
    return juzhen

def graph(a,wb):
    ws=wb.add_sheet(str(a)+"个顶点结果")
    ws.write(0,0,'序号')
    ws.write(0,1,'顶点数')
    ws.write(0,2,'边集')
    ws.write(0,3,'递推算法判断')
    ws.write(0,4,'递推算法回路')

    r=9
    jiaodu = 360//a
    qishijiaodu=0
    zuobiao_x=[]
    zuobiao_y=[]
    for i in range(a):
        zuobiao_x.append(math.sin(math.radians(qishijiaodu))*r)
        zuobiao_y.append(math.cos(math.radians(qishijiaodu))*r)
        qishijiaodu+=jiaodu

    # 得到完全图的全哈密顿回路
    hangshu = int(math.factorial(a-1)/2)
    hamidunhuan = quanpailie(a-1)[0:hangshu,:]
    charujuzhen = np.full((hangshu,1),a)
    hamidunhuan = np.column_stack((charujuzhen,hamidunhuan))
    charujuzhen=[]

    # 每个顶点循环测试100次
    for r in range(100):
        #序号
        ws.write(r+1,0,r)
        #顶点数
        ws.write(r+1,1,a)
        flag=0

        #生成a个顶点的完全图的所有路径
        alllujin=[]
        for i in range(1,a):
            s=i+1
            for j in range(s,a+1):
                alllujin.append('{}-{}'.format(i,j)) 
        
        #随机生成a个顶点的图的路径
        lujinji=random.sample(alllujin,random.randint(a,len(alllujin)))
        #边集
        ws.write(r+1,2,str(lujinji))

        #如果边数小于顶点数，一定不存在哈密顿回路
        if len(lujinji) < a:
            # print('不存在哈密顿回路')
            flag = 1
        
        #某个顶点少于两条边一定不存在哈密顿回路
        s=[]
        for i in range(a):
            s.append(0)
        for i in lujinji:
            fuhao=i.index('-')
            s[int(i[:fuhao])-1]+=1
            s[int(i[fuhao+1:])-1]+=1
        
        dianji=[]
        # 某个顶点少于两条边一定不存在哈密顿回路
        for i in range(a):
            if s[i]<2:
                # print('不存在哈密顿回路')
                flag = 1
            elif s[i]<hangshu:
                dianji.append(i+1)
                

        if flag != 1:
            # # 得到完全图的全哈密顿回路
            # hangshu = int(math.factorial(a-1)/2)
            # hamidunhuan = quanpailie(a-1)[0:hangshu,:]
            # charujuzhen = np.full((hangshu,1),a)
            # hamidunhuan = np.column_stack((charujuzhen,hamidunhuan))
            # charujuzhen=[]

            # 判别随机无向图是否是完全图
            if len(alllujin)==len(lujinji):
                ws.write(r+1,4,str(hamidunhuan[0]))
                ws.write(r+1,3,'存在')
            else:
                # 生成对应顶点的过渡矩阵
                data_linshi=[]
                for j in dianji:
                    charujuzhen = np.full((hangshu,a),j)
                    data_linshi.append(np.multiply((hamidunhuan-charujuzhen).astype(bool),(np.column_stack((hamidunhuan[:,1:],hamidunhuan[:,0:1]))-charujuzhen).astype(bool)))
                    charujuzhen=[]

                # 生成缺失边对应哈密顿回路位置集
                queshilujin=list(set(alllujin)-set(lujinji))
                charujuzhen = np.full((1,hangshu),4)
                data_lujin=[]
                for i in queshilujin:
                    fuhao=i.index('-')
                    data_lujin.append(np.invert((np.sum(np.invert(np.multiply(data_linshi[dianji.index(int(i[:fuhao]))],data_linshi[dianji.index(int(i[fuhao+1:]))])).astype(int),axis=1)-charujuzhen).astype(bool)).astype(int))
                if len(data_lujin) != 1:
                    charujuzhen = np.full((1,hangshu),len(queshilujin))
                    data_lujin=np.invert((np.sum(np.row_stack(tuple(data_lujin)),axis=0)-charujuzhen).astype(bool)).astype(int)
                else:
                    data_lujin=data_lujin[0]
                charujuzhen = []
                
                # 判断是否存在哈密顿回路，有就输出结果
                weizhi = np.where(data_lujin[0]==1)
                if np.any(weizhi):
                    hamidunhuilu = hamidunhuan[weizhi[0][0]]
                    ws.write(r+1,3,'存在')
                    ws.write(r+1,4,str(hamidunhuilu))

                    # 绘制图像
                    for f in lujinji:
                        fuhao=f.index('-')
                        plt.plot([zuobiao_x[int(f[:fuhao])-1],zuobiao_x[int(f[fuhao+1:])-1]],[zuobiao_y[int(f[:fuhao])-1],zuobiao_y[int(f[fuhao+1:])-1]],'k')
                    for f in range(a):
                        if f == a-1:
                            plt.plot([zuobiao_x[hamidunhuilu[f]-1],zuobiao_x[hamidunhuilu[0]-1]],[zuobiao_y[hamidunhuilu[f]-1],zuobiao_y[hamidunhuilu[0]-1]],'r')
                        else:
                            plt.plot([zuobiao_x[hamidunhuilu[f]-1],zuobiao_x[hamidunhuilu[f+1]-1]],[zuobiao_y[hamidunhuilu[f]-1],zuobiao_y[hamidunhuilu[f+1]-1]],'r')
                    plt.savefig('dituihunlu/{}_{}.png'.format(a,r))
                    plt.clf()
                    
                else:
                    ws.write(r+1,3,'不存在')

        else:
            ws.write(r+1,3,'不存在')
            
if __name__ == "__main__":       
    start = datetime.datetime.now()  
    # 先获取一个图表
    fig = plt.figure()    
    # 设置x,y坐标轴的刻度显示范围
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    wb=xlwt.Workbook()
    #输出4到11个顶点的结果
    for i in range(4,12):
        graph(i,wb)
    wb.save("测试数据集.xls")
    end = datetime.datetime.now()
    print('用时: ',(end-start),' us')
'''
IP地址计算器2.0，增加划分子网功能
此代码用于实现IP地址计算和子网划分
@author：ChenTaiYang
@time：2022/1/11  第1次提交，实现IP地址计算
@time：2022/1/15  第2次提交,增加划分子网功能
'''
import ipaddress

#IP地址计算函数
def cal_ip(ip_net):
 try:
  net = ipaddress.ip_network(ip_net, strict=False)
  print('IP版本号： ' + str(net.version))
  print('是否是私有地址： ' + str(net.is_private))
  print('IP地址总数: ' + str(net.num_addresses))
  print('可用IP地址总数： ' + str(len([x for x in net.hosts()])))
  print('网络号： ' + str(net.network_address))
  print('起始可用IP地址： ' + str([x for x in net.hosts()][0]))
  print('最后可用IP地址： ' + str([x for x in net.hosts()][-1]))
  print('可用IP地址范围： ' + str([x for x in net.hosts()][0]) + ' —— ' + str([x for x in net.hosts()][-1]))
  print('掩码地址： ' + str(net.netmask))
  print('反掩码地址： ' + str(net.hostmask))
  print('广播地址： ' + str(net.broadcast_address))
 except ValueError:
  print('您输入格式有误，请检查！')


#划分子网函数
def divide_ip(str):
    try:
        '''切割网络号、子网掩码、子网数量'''
        temp = str.split('/')
        if len(temp) != 3 :
            # 输入不合法！
            raise AttributeError  #引发异常，该异常名不是对应的异常类型，只是为了except可以捕获到
         
        '''转换子网掩码、子网数量'''
        subnetMask = int(temp[1]) #子网掩码
        subnetNumber = int(temp[2]) #子网数量
        if (subnetMask<2) or (subnetNumber<2) :
            # 子网掩码、子网数量至少为2！
            raise EOFError  #引发异常，该异常名不是对应的异常类型，只是为了except可以捕获到
         
        '''切割、转换网络号到十进制'''
        temp2 = temp[0].split('.')
        if len(temp2) !=4 :
            # 网络号不合法！
            raise ImportError  #引发异常，该异常名不是对应的异常类型，只是为了except可以捕获到
         
        ip10=[0]*4 #初始化每一段IP地址，十进制
        for i in range(4) : #转为整形
            ip10[i]=int(temp2[i])
            if (ip10[i]<0) or (ip10[i]>255) :
                # 网络号不合法！
                raise ImportError  #引发异常，该异常名不是对应的异常类型，只是为了except可以捕获到
         
        '''转换网络号到二进制'''
        ip2=[0]*32 #初始化每一位IP地址，二进制
        flag=0 #flag标记是否停止计算网络前缀
        preNet=32 #preNet网络前缀个数(32-从后往前数，第一个不为0的数字)
        k=31
        for i in range(3,-1,-1) : #转为二进制，并保存到数组
            for j in range(8) :
                ip2[k] = ip10[i] >> j & 1 #>>运算，右移n位，高位补0
                k-=1
                if (flag==0) and (ip2[k+1]==0) : #计算网络前缀
                    preNet-=1
                else:
                    flag=1
         
        if subnetMask < preNet :
            #print("该网络号的子网掩码不合法！程序终止！")
            raise IndexError  #引发异常，该异常名不是对应的异常类型，只是为了except可以捕获到
            
        if (1 << (32 - subnetMask)) < subnetNumber : #子网数不可超过主机数量,<<运算，左移n位，相当于2的n次方
            #print("需求子网数超出最大主机数量！程序终止！")
            raise KeyError   #引发异常，该异常名不是对应的异常类型，只是为了except可以捕获到
         
        '''计算应当划分的子网数量和每个子网的最大主机数量'''
        realSubnetNumber = subnetNumber - 1 #假设输入的子网数量为2的幂次方,此处-1是避免是2的幂的情况，1是例外，但是上面已经排除
        power = 1 #应该为2的几次幂
        while (realSubnetNumber >> 1) != 0 : #相当于a=a/2,a/2!=0
            realSubnetNumber = realSubnetNumber >> 1
            power+=1
        realSubnetNumber = 1 << power
        maxHost = 1 << (32 - preNet - power) #每个子网的最大主机数量
         
        '''分配ip'''
        preIp=[[0 for col in range(4)] for row in range(realSubnetNumber)] #第一个ip
        sufIp=[[0 for col in range(4)] for row in range(realSubnetNumber)] #最后一个ip
        for i in range(realSubnetNumber) :
            '''设置子网号'''
            for j in range(power) : #子网号，递增
                ip2[subnetMask + power - j - 1] = i >> j & 1;
            '''设置第一个ip'''
            for j in range(subnetMask + power,32) :#填充0
                ip2[j]=0
            for j in range(4) : #计算每一段IP地址，十进制
                t=0 #计算数组对应的值
                for k in range(8) :
                    t += ip2[(j << 3) + k] << (7 - k)
                preIp[i][j] = t #第一个ip
            '''设置最后一个ip'''
            for j in range(subnetMask + power,32) :#填充1
                ip2[j]=1
            for j in range(4) :
                t=0
                for k in range(8) :
                    t += ip2[(j << 3) + k] << (7 - k)
                sufIp[i][j] = t #最后一个ip
         
        '''输出'''
        print(u"根IP地址为：" , temp[0] , u" 子网掩码位数为：" , subnetMask)
        print("需求子网数量为：" , subnetNumber , " 实际划分的子网数量为：" , realSubnetNumber)
        print("每个子网最大的主机数量为：" , maxHost)
        for i in range(realSubnetNumber) :
            print("第 " , i+1 , " 个子网可用地址：",\
            preIp[i][0] , "." , preIp[i][1] , "." , preIp[i][2] , "." , (preIp[i][3] + 1) , "---",\
            sufIp[i][0] , "." , sufIp[i][1] , "." , sufIp[i][2] , "." , (sufIp[i][3] - 1),\
            "\t网络地址：" , preIp[i][0] , "." , preIp[i][1] , "." , preIp[i][2] , "." , preIp[i][3],\
            "\t广播地址：" , sufIp[i][0] , "." , sufIp[i][1] , "." , sufIp[i][2] , "." , sufIp[i][3])

    except AttributeError:
            print("输入不合法！请检查！")
    except EOFError:
            print("子网掩码、子网数量至少为2！请检查！")
    except ImportError:
            print("网络号不合法！请检查！")
    except IndexError:
            print("该网络号的子网掩码不合法！请检查！")
    except KeyError :
            print("需求子网数超出最大主机数量！请检查！")


#调用函数
while True:
    try:
        print("************************** IP地址计算器 **************************")
        print("-------------------------- 1.计算IP地址 --------------------------")
        print("-------------------------- 2.划分子网 ----------------------------")
        print("-------------------------- 3.退出系统 ----------------------------")
        print("************************** IP地址计算器 **************************")
        action = int(input("请输入对应数字进行操作："))
        print("-" * 60)  # 分隔线

        if action == 1:
            ip_net = input("请输入IP地址（格式：192.168.1.0/24）：")
            cal_ip(ip_net)
            print("\n")
            flag=input("是否继续（继续输入 y，退出输入其他任意字母）：")
            print("\n")
            if flag != 'y':
                break
        elif action == 2:
            str = input("请输入网络号（格式:192.168.1.0/24/8，24为子网掩码，8为需求子网数量）：") #初始化网络号、子网掩码、需求子网数量
            divide_ip(str)
            print("\n")
            flag=input("是否继续（继续输入 y，退出输入其他任意字母）：")
            print("\n")
            if flag != 'y':
                break
        elif action == 3:
            break;
        else:
            print("【ERROR】：输入有误，请重新输入！")
    except ValueError:
        print("输入有误！请重新输入！\n")

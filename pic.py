_                   =  (
                    255,
                   lambda
                V    ,B,c
               :c  and Y(V*V+B,B, c
                -1)if(abs(V)<6)else
        (       2+c-4*abs(V)**-0.4)/i
         ) ;v,   x=1500,1000;C=range(v*x
         );import struct;P=struct.pack;M,\
      j ='<QIIHHHH',open('M.bmp','wb').write
for X in j('BM'+P(M,v*x*3+26,26,12,v,x,1,24))or C:
      i ,Y=_;j(P('BBB',*(lambda T:(T*80+T**9
         *i-950*T **99,T*70-880*T**18+701*
         T **9   ,T*i**(1-T**45*2)))(sum(
        [       Y(0,(A%3/3.+X%v+(X/v+
                A/3/3.-x/2)/1j)*2.5
               /x  -2.7,i)**2 for \
                A    in C
                   [:9]])
                    /9)
                    )  )
#解析
_=(255,lambda V,B,c:c and Y(V*V+B,B, c-1)if(abs(V)<6) else(2+c-4*abs(V)**-0.4)/i)#相当于函数，需要两个参数255和lambda
v,x=1500,1000
C=range(v*x)
import struct
P=struct.pack
M,j ='<QIIHHHH',open('M.bmp','wb').write
for X in j('BM'+P(M,v*x*3+26,26,12,v,x,1,24))or C:
    i ,Y=_  #调用_函数，i是255，Y是lambda其参数有三个V,B,c
    j(P('BBB',*(lambda T:(T*80+T**9*i-950*T**99,T*70-880*T**18+701*T**9,T*i**(1-T**45*2)))(sum([Y(0,(A%3/3.+X%v+(X/v+A/3/3.-x/2)/1j)*2.5/x-2.7,i)**2 for A in C[:9]])/9)))
        #后面的sum表达式是给前面的lambda表达式赋值的，即将sum的值赋给T，得出的结果是(),(),()三个值，然后让struck.pack进行打包存入j里面
    
    

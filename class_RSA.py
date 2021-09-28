from random import randint
from math import sqrt


class rsa():
    def __init__(self):
        self.create()

    def change(self, p, q, e):
        try:
            assert p * q > 255 and self.isprime(p) and self.isprime(q)  # n应该大于255
            assert e>1
            #注：因为一个字符串使转二进制时得到的01串共16位，
            # 一个字符串分割成两个8位的01串，所以m应小于2^8
            self.p = p
            self.q = q
            self.n = p * q
            self.fn = (p - 1) * (q - 1)  # 欧拉函数
            self.e = e
            self.d,tem,tem= self.Euler(e, self.fn)
            while self.d<0:
                self.d = self.d+self.fn
            return True
        except Exception as e:
            print(e)
            return False

    def create(self):
        self.numList = []
        n = 100  # 100内选素数
        self.getprimelist(n)
        num1 = len(self.numList) / 2 - 1
        self.n = 0
        while self.n <= 255:
            self.p = self.numList[randint(0, int(num1))]
            self.q = self.numList[randint(0, int(num1)) + int(len(self.numList) / 2)]
            self.n = self.p * self.q
        self.fn = (self.p - 1) * (self.q - 1)#欧拉函数
        self.e, self.d = self.returnED(self.fn)
    # 明文字符串转二进制
    def isprime(self,num):
        if  num > 1:
            for i in range(2, int(sqrt(num))+1):
                if num % i == 0:
                    return False
            return True
        else:
            print('变量有误，请输入大于1的整数。')
    def get_p_bin(self, Texts):
        """字符串转二进制
        Text：字符串
        return 字符串对应的二进制的编码
        """
        Text_bin = ''
        for text in Texts:
            s = ord(text)
            s_bin = '{:016b}'.format(s)
            Text_bin = Text_bin + s_bin
        return Text_bin

    # 密文字符串转二进制
    def get_c_bin(self, Texts):
        """字符串转二进制
        Text：字符串
        return 字符串对应的二进制的编码
        """
        Text_bin = ''
        for text in Texts:
            s = ord(text)
            s_bin = '{:08b}'.format(s)
            Text_bin = Text_bin + s_bin
        return Text_bin

    # 二进制转字符函数
    def bin_str(self, s):
        '''获取16位的01串，返回对应的汉字'''
        try:
            return chr(int(s, 2))
        except:
            return -1
    #求最大公约数
    def gcd(self, a, b):
        """求最大公约数"""
        c = a % b
        while c != 0:  # 辗转相除法
            a = b
            b = c
            c = a % b
        # 当余数为0时，循环结束
        return b
    #展示
    def disp(self):
        return self.n, self.e, self.p, self.q, self.d, self.fn
    #获取素数表
    def getprimelist(self, n):
        """生成小于n的素数表"""
        primelist = n * [1]  # 全1矩阵
        primelist[:2] = [0, 0]  # 0和1不是素数
        for i in range(2, int(sqrt(n))):  # 只需要筛选到最大数的平方根即可，比最大数小的合数必然存在比最大数的平方根小的数
            if primelist[i] == 1:  # 确认除数是素数
                for j in range(i * 2, n, i):
                    primelist[j] = 0  # 倍数肯定不是素数
        for i in range(n):
            if primelist[i] == 1:
                self.numList.append(i)
    #欧拉法求模逆元
    def Euler(self, e, fn):
        '''
        e为d的系数，fn为k的系数ed=1(modfn)
        '''
        if fn == 0:
            return 1, 0, e
        else:
            x, y, q = self.Euler(fn, e % fn)
            x, y = y, (x - (e // fn) * y)
        return x, y, q
    #返回公钥e和密钥d
    def returnED(self, fn):
        e = randint(10, fn - 1)
        while self.gcd(e, self.fn) != 1:
            e = randint(10, fn - 1)
        d, x, y = self.Euler(e, fn)
        while d < 0:
            d = d + fn
        # print(f'e,d={e},{d}')
        return e, d
    #模幂算法
    def powmod(self,v, u, c):
        """v:底数
        u:指数
        c:模
        """
        w = 1
        while u != 0:
            if u % 2 == 0:
                u = u / 2
                v = (v * v) % c
            u = u - 1
            w = (w * v) % c
        return w

    #二进制字符串分割函数
    def distribute(self, m):
        """"给二进制字符串分组"""
        mL = []
        mlen = len(m)
        i = 0
        while 8 * (i + 1) <= mlen:
            # print(f'm[{i*8}:{(i+1)*8}]:',m[i*8:(i+1)*8])
            mL.append(int(m[i * 8:(i + 1) * 8], 2))
            i += 1
        return mL
    #加密函数
    def encryption(self, text):
        m = self.get_p_bin(text)  # 明文
        mL = self.distribute(m)#8位为一组
        self.__plaintext = mL
        c = ''
        for m in mL:
            c = c + str(self.powmod(m, self.e, self.n)) + ' '  # 密文,m的e次方幂
        #print("已完成c运算, c=", c)
        self.__ciphertext = c
        return self.__ciphertext
    #解密函数
    def dencryption(self, texts, flag):
        '''flag=0字符串
            flag=2二进制
            flag=10十进制
            flag=16十六进制
        '''
        assert flag !=None
        cL = []
        if flag == 0:
            for text in texts:
                cL.append(int(self.get_c_bin(text),2))
        elif flag == 2:
            texts = list(texts.split(' ')[:-1])
            for text in texts:
                cL.append(int(text, 2))
        elif flag == 10:
            cL = texts.split(' ')[:-1]
        elif flag == 16:
            texts = list(texts.split(' ')[:-1])
            for text in texts:
                cL.append(int(text, 16))
        m = []
        for c in cL:
            m.append(str(self.powmod(int(c), self.d, self.n)))
        #print("已完成m运算, m=", m)
        self.__plaintext = m
        return self.__plaintext

    # 以数字形式展示
    def showc_in_num(self, n):
        ''''n代表进制，目前仅支持2进制和16进制'''
        assert n != None
        cstr = ''
        s_hex = ''
        s_bin = ''
        c = self.__ciphertext
        if n == 2:
            for i in c.split(' ')[:-1]:
                s_bin = s_bin + '{:b}'.format(int(i)) + ' '
            return s_bin
        elif n == 16:
            s_hex = ''
            for i in c.split(' ')[:-1]:
                s_hex = s_hex + '{:x}'.format(int(i)) + ' '
            return s_hex
        elif n == 10:
            return c
        else:
            return '请期待后续版本，感谢您的信赖'

    # 明文以文字形式展示
    def show_mtext(self):
        '''明文'''
        M = self.__plaintext
        m_text = ''
        for i in range(len(M)//2):
            mystr = '{:08b}{:08b}'.format(int(M[2*i]),int(M[2*i+1]))
            m_text = m_text+self.bin_str(mystr)
        return m_text
    # 密文以文字形式展示
    def show_ctext(self):
        '''密文'''
        C = self.__ciphertext
        C = C.split(' ')[:-1]
        c_text = ''
        for i in range(len(C)):
            mystr= '{:016b}'.format(int(C[i]))
            c_text = c_text + self.bin_str(mystr)
        return c_text

if __name__ == '__main__':
    R = rsa()
    text = '面朝大海，春暖花开！！'
    R.change(11,47,39)#epqd
    R.encryption(text)
    c = R.show_ctext()
    print('c = ',c)
    R.dencryption(c, 0)
    print('m = ',R.show_mtext())
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:34:07 2020

@author: HP1
"""
import os
from tkinter import Label,LabelFrame,Frame,Entry,Canvas,Button,IntVar,Radiobutton,E,W,NSEW,INSERT,Tk
from tkinter import scrolledtext as sclt #滚动窗口所需函数库
from tkinter import filedialog#, dialog
from tkinter.messagebox import askyesno
from class_DES import des
from class_RSA import rsa
from file_operation import readfile,savefile


class Window():
    def __init__(self,master):

        self.window = master
        
        width = 850 #主窗口宽度
        height = 640 #主窗口高度

        screenwidth = self.window.winfo_screenwidth() #获取屏幕宽度
        screenheight = self.window.winfo_screenheight() #获取屏幕高度
        
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2) #主窗口出现位置
        
        self.window.title('数据加密工具（2020.12.14）') #框架名称
        
        self.window.geometry(alignstr) #显示窗口

        self.window.resizable(width=True, height=True)#窗口长宽高可变(True)
        
        self.window.columnconfigure(0,weight=1)
        self.window.rowconfigure(0,weight=1) 

        DES(self.window)#调用下面的类
        
        
class DES():
    def __init__(self,master):
        d = des()
        self.master = master
 
        self.DES = Frame(self.master)
        self.DES.grid(row=0,column=0,sticky=NSEW)
        
        self.DES.columnconfigure(0,weight=1) #定义DES窗口第零列的权重为1，即只有一列
        self.DES.rowconfigure(0,weight=1) #定义DES窗口第零行的权重为1，即只有一行
        
        '''labfrm'''
        self.DES_labfrm = LabelFrame(self.DES,text="DES加密工具",font=('微软雅黑',20))
        self.DES_labfrm.grid(row=0,column=0,stick=NSEW,padx=1)
        
        '''顶/底部labfrm'''
        self.DES_labfrm.columnconfigure(0,weight=1)
        self.DES_labfrm.rowconfigure(0,weight=100)
        self.DES_labfrm.rowconfigure(1,weight=2)
        s = [['T','字符串加密'],['D','文件加密']]
        for i in range(2):
            exec('self.DES_%slabfrm = LabelFrame(self.DES_labfrm,text="%s",font=("微软雅黑",13))'%(s[i][0],s[i][1]))
            eval('self.DES_%slabfrm'%s[i][0]).grid(row=i,column=0,stick=NSEW,padx=4,pady=2)
            eval('self.DES_%slabfrm'%s[i][0]).columnconfigure(0,weight=1)
            
        '''在字符串加密labfrm创建frm0，frm1，frm2，frm3'''        
        w = [1,1,2,100] 
        for i in range(4):
            self.DES_Tlabfrm.rowconfigure(i,weight=w[i]) #i行权重
            exec('self.DES_Tlabfrm%s = Frame(self.DES_Tlabfrm)'%i)#,relief=RIDGE,bd=1
            eval('self.DES_Tlabfrm%s'%i).grid(row=i,column=0,stick=NSEW)

        '''Tlabfrm中的frm0框'''
        for i in range(14):
            self.DES_Tlabfrm0.columnconfigure(i,weight=1)
        self.DES_Tlabfrm0.rowconfigure(0,weight=1)
        self.DES_slab = Label(self.DES_Tlabfrm0,text="密钥：", font=('微软雅黑',13))
        self.DES_slab.grid(row=0,column=0,padx=1,stick=E)
        self.DES_se = Entry(self.DES_Tlabfrm0)
        self.DES_se.grid(row=0,column=1,padx=1,stick=W)
        
        '''Tlabfrm中的frm1框'''
        self.DES_Tlabfrm1.rowconfigure(0,weight=1)
        def radCall():
            global flag
            flag=-1
            radSel = v.get()
            if radSel == 1:
                flag=16
            elif radSel == 2:
                flag=2
            elif radSel == 3:
                flag=0
        v = IntVar()
        s = ['十六进制','二进制','原始字符']
        for i in range(3):
            self.DES_Tlabfrm1.columnconfigure(i,weight=1)    
            exec('self.DES_r%i = Radiobutton(self.DES_Tlabfrm1,text="密文以%s显示",variable=v,font=(10),value=%s,command=radCall)'%(i,s[i],i+1))
            eval('self.DES_r%i'%i).grid(row=0,column=i)        
        
        '''Tlabfrm中的frm2框'''
        self.DES_Tlabfrm2.rowconfigure(0,weight=1)
        
        '''Tlabfrm中的frm3框'''
        self.DES_Tlabfrm3.rowconfigure(0,weight=1)
        s = ['明文','密文']
        for i in range(2):
            self.DES_Tlabfrm3.columnconfigure(i,weight=1)
            exec('self.DES_Tlabfrm3%s = LabelFrame(self.DES_Tlabfrm3,text="%s",font=("微软雅黑",10))'%(i,s[i]))
            eval('self.DES_Tlabfrm3%s'%i).grid(row=0,column=i,stick=NSEW,padx=5,pady=5)
            eval('self.DES_Tlabfrm3%s'%i).rowconfigure(0,weight=1)
            eval('self.DES_Tlabfrm3%s'%i).columnconfigure(0,weight=1)
            exec('self.DES_Tlabfrm3%s_s%s = sclt.ScrolledText(self.DES_Tlabfrm3%s,font=("隶书",15))'%(i,i,i))
            eval('self.DES_Tlabfrm3%s_s%s'%(i,i)).grid(row=0,column=0,stick=NSEW,padx=5,pady=5)        
        
        '''在文件加密labfrm创建frm0，frm1''' 
        for i in range(2):
            self.DES_Dlabfrm.rowconfigure(i,weight=1) #行权重
            exec('self.DES_Dlabfrm%s = Frame(self.DES_Dlabfrm)'%i)
            eval('self.DES_Dlabfrm%s'%i).grid(row=i,column=0,stick=NSEW)
         
        '''Dlabfrm中的frm0框'''
        for i in range(4):
            self.DES_Dlabfrm0.columnconfigure(i,weight=1)
        self.DES_Dlabfrm0.rowconfigure(0,weight=1)
        self.DES_flab = Label(self.DES_Dlabfrm0,text="文件名称：", font=('微软雅黑',13))
        self.DES_flab.grid(row=0,column=0,padx=1,stick=E)
        self.DES_fe = Entry(self.DES_Dlabfrm0,width=100)
        self.DES_fe.grid(row=0,column=1,padx=1,stick=W)        
        
        '''Dlabfrm中的frm1框'''
        self.DES_Dlabfrm1.rowconfigure(0,weight=2)
        
        '''按钮分布（Tlanfrm2与Dlabfrm1）'''
        def encrypt():
            self.DES_Tlabfrm31_s1.delete(0.0,'end')
            text = self.DES_se.get()#获取密钥
            if text != '':
                d.get_sk(text)
            else:
                askyesno(title='提示', message='未获取密钥')
            m = self.DES_Tlabfrm30_s0.get(0.0,'end')[:-1]#获取明文
            d.encryption(m)
            if flag == 0:
                self.DES_Tlabfrm31_s1.insert(INSERT, ('%s' % d.show_ctext()))
            else:
                self.DES_Tlabfrm31_s1.insert(INSERT, ('%s' % d.showc_in_num(flag)))
            
        def decrypt():
            text = self.DES_se.get()  # 获取密钥
            if text != '':
                d.get_sk(text)
            else:
                askyesno(title='提示', message='未获取密钥')
            self.DES_Tlabfrm30_s0.delete(0.0,'end')#清空密文框
            c = self.DES_Tlabfrm31_s1.get(0.0,'end')[:-1]
            d.dencryption(c, flag)
            self.DES_Tlabfrm30_s0.insert(INSERT,('%s'%d.show_mtext()))
            
        def clear_1():
            self.DES_Tlabfrm30_s0.delete(0.0,'end')#清空明文
        def clear_2():
            self.DES_Tlabfrm31_s1.delete(0.0,'end')#清空密文

        def open_mfile():
            global file_path
            global file_text
            try:
                file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(':/')))
                if file_path !="":
                    text = self.DES_se.get()  # 获取密钥
                    if text != '':
                        d.get_sk(text)
                    else:
                        askyesno(title='提示', message='未获取密钥')
                    window = Tk()
                    window.title('加密')
                    width = 500
                    height = 70
                    smwinwidth = window.winfo_screenwidth()
                    smwinhight = window.winfo_screenheight()
                    alignstr = '%dx%d+%d+%d'%(width,height,(smwinwidth-width)/2,(smwinhight-height)/2)
                    window.geometry(alignstr)
                    window.rowconfigure(0,weight=1)
                    window.columnconfigure(0,weight=1)
                    window.columnconfigure(1,weight=5)
                    # 设置进度条
                    Label(window, text='加密中', ).grid(row=0,column=0,stick=E)
                    canvas = Canvas(window, width=400, height=22, bg="white")
                    canvas.grid(row=0,column=1)
                    filename, file_text = readfile(file_path)
                    self.DES_Tlabfrm30_s0.delete(0.0, 'end')
                    self.DES_Tlabfrm30_s0.insert(INSERT, ('%s' % file_text))
                    self.DES_fe.delete(0,"end")
                    self.DES_fe.insert(INSERT, ('%s' % filename))

                    c = ''

                    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
                    x = len(file_text)//4 + 1
                    n = 500 / x  # 500是矩形填充满的次数
                    if flag == 0:
                        i = -1
                        for i in range(x-1):
                            d.encryption(file_text[4*i:4*(i+1)])
                            n = n + 465 / x
                            canvas.coords(fill_line, (0, 0, n, 60))
                            window.update()
                            c = c + d.show_ctext()
                        #fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
                        if len(file_text[4 * (i + 1):])>0:
                            d.encryption(file_text[4 * (i + 1):])
                            c = c + d.show_ctext()
                    else:
                        i = -1
                        for i in range(x - 1):
                            d.encryption(file_text[4*i:4 * (i + 1)])
                            n = n + 465 / x
                            canvas.coords(fill_line, (0, 0, n, 60))
                            window.update()
                            c = c + d.showc_in_num(flag)
                        # fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
                        if len(file_text[4 * (i + 1):]) > 0:
                            d.encryption(file_text[4 * (i + 1):])
                            c = c + d.showc_in_num(flag)

                    self.DES_Tlabfrm31_s1.delete(0.0, 'end')
                    self.DES_Tlabfrm31_s1.insert(INSERT, ('%s' % c))
            except:
                askyesno(title='提示', message='请选择文本显示形式')
            finally:
                window.destroy()

        def open_cfile():
            try:
                global file_path
                global file_text
                file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(':/')))
                if file_path != "":
                    text = self.DES_se.get()  # 获取密钥
                    if text != '':
                        d.get_sk(text)
                    else:
                        askyesno(title='提示', message='未获取密钥')
                    #进度条
                    window = Tk()
                    window.title('加密')
                    width = 500
                    height = 70
                    smwinwidth = window.winfo_screenwidth()
                    smwinhight = window.winfo_screenheight()
                    alignstr = '%dx%d+%d+%d'%(width,height,(smwinwidth-width)/2,(smwinhight-height)/2)
                    window.geometry(alignstr)
                    window.rowconfigure(0,weight=1)
                    window.columnconfigure(0,weight=1)
                    window.columnconfigure(1,weight=5)
                    # 设置下载进度条
                    Label(window, text='解密中', ).grid(row=0,column=0,stick=E)
                    canvas = Canvas(window, width=400, height=22, bg="white")
                    canvas.grid(row=0,column=1)
                    filename, file_text = readfile(file_path)
                    self.DES_Tlabfrm31_s1.delete(0.0, 'end')
                    self.DES_Tlabfrm31_s1.insert(INSERT, ('%s' % file_text))
                    self.DES_fe.delete(0, "end")
                    self.DES_fe.insert(INSERT, ('%s' % filename))
                    m = ''

                    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
                    x = len(file_text) // 8 + 1
                    n = 500 / x  # 500是矩形填充满的次数
                    if flag == 0:
                        i = -1
                        for i in range(x - 1):
                            d.dencryption(file_text[8 * i:8 * (i + 1)],0)
                            n = n + 465 / x
                            canvas.coords(fill_line, (0, 0, n, 60))
                            window.update()
                            m = m + d.show_mtext()
                        if len(file_text[8 * (i + 1):])>0:
                            d.dencryption(file_text[8 * (i + 1):],0)
                            m = m + d.show_mtext()
                    else:#当不是字符串加密时执行一下语句
                        filename,file_text = readfile(file_path)
                        #文件名框输出文件名
                        self.DES_fe.delete(0, "end")
                        self.DES_fe.insert(INSERT, ('%s' % filename))
                        #密文框输入密文
                        self.DES_Tlabfrm31_s1.delete(0.0, 'end')
                        self.DES_Tlabfrm31_s1.insert(INSERT, ('%s' % file_text))
                        #直接加密
                        d.dencryption(file_text,flag)
                        m = d.show_mtext()
                    self.DES_Tlabfrm30_s0.delete(0.0, 'end')
                    self.DES_Tlabfrm30_s0.insert(INSERT, ('%s' %m))
            except Exception as e:
                #print('错误为：',e)
                if flag == None:
                    askyesno(title='提示', message='请选择文本显示形式')

            finally:
                if window:
                    window.destroy()

        def save_cfile():
            file_path = filedialog.asksaveasfilename(title=u'保存文件', defaultextension='.txt', filetypes=[("文本文件txt", ".txt"),("word格式",".docx"),("所有格式","*")])
            file_text = self.DES_Tlabfrm31_s1.get('0.0', 'end')[:-1]
            if file_path != '' :
                if savefile(file_path,file_text) == 0:#保存成功执行以下语句
                    askyesno(title='提示', message='密文保存完成')
                else:
                    askyesno(title='提示', message='密文保存失败')
            else:
                askyesno(title='提示', message='未保存')

        def destroy():
            window.destroy()
        s = [['加密','encrypt'],['解密','decrypt'],['清空明文','clear_1'],['清空密文','clear_2'],['切换RSA','self.change_RSA'],\
             ['加密明文文件','open_mfile'],['解密密文文件','open_cfile'],['保存密文','save_cfile'],['退出','destroy']]
        x = ['self.DES_Tlabfrm2','self.DES_Dlabfrm1']
        for i in range(9):
            eval('%s'%x[0 if i<5 else 1]).columnconfigure([0,1,2,3,4,0,1,2,3][i],weight=1)
            exec('self.DES_b%s = Button(%s,text="%s",width=13,font=(10),command=%s)'%(i,x[0 if i<5 else 1],s[i][0],s[i][1]))
            eval('self.DES_b%s'%i).grid(row=0,column=[0,1,2,3,4,0,1,2,3][i],pady=5,ipady=3)            
        
        
    def change_RSA(self,):
        self.DES.destroy()
        global flag
        flag = None
        RSA(self.master)
        
        
class RSA():
    def __init__(self,master):
        r = rsa()
        self.master = master
        
        self.RSA = Frame(self.master)
        self.RSA.grid(row=0,column=0,stick=NSEW)
        
        self.RSA.columnconfigure(0,weight=1)
        self.RSA.rowconfigure(0,weight=1)
        
        '''labfrm'''
        self.RSA_labfrm = LabelFrame(self.RSA,text="RSA加密工具",font=('微软雅黑',20))
        self.RSA_labfrm.grid(row=0,column=0,stick=NSEW,padx=1)
        
        '''顶/底部labfrm'''
        self.RSA_labfrm.columnconfigure(0,weight=1)
        self.RSA_labfrm.rowconfigure(0,weight=100)
        self.RSA_labfrm.rowconfigure(1,weight=2)        
        s = [['T','字符串加密'],['D','文件加密']]
        for i in range(2):
            exec('self.RSA_%slabfrm = LabelFrame(self.RSA_labfrm,text="%s",font=("微软雅黑",13))'%(s[i][0],s[i][1]))
            eval('self.RSA_%slabfrm'%s[i][0]).grid(row=i,column=0,stick=NSEW)
            eval('self.RSA_%slabfrm'%s[i][0]).columnconfigure(0,weight=1)

        '''在字符串加密labfrm创建labfrm0，frm1''' 
        self.RSA_Tlabfrm.rowconfigure(0,weight=1)
        self.RSA_Tlabfrm.rowconfigure(1,weight=100)
        
        self.RSA_Tlabfrm0 = LabelFrame(self.RSA_Tlabfrm,text='功能区',font=('微软雅黑',13))
        self.RSA_Tlabfrm0.grid(row=0,column=0,stick=NSEW,padx=10)
        
        self.RSA_Tlabfrm1 = Frame(self.RSA_Tlabfrm)
        self.RSA_Tlabfrm1.grid(row=1,column=0,stick=NSEW)
        
        '''在Tlabfrm0中创建frm0 frm1 frm2'''
        self.RSA_Tlabfrm0.columnconfigure(0,weight=1)
        for i in range(3):
            self.RSA_Tlabfrm0.rowconfigure(i,weight=1)
            exec('self.RSA_Tlabfrm0%s = Frame(self.RSA_Tlabfrm0)'%i)
            eval('self.RSA_Tlabfrm0%s'%i).grid(row=i,column=0,stick=NSEW)
            eval('self.RSA_Tlabfrm0%s'%i).rowconfigure(0,weight=1)
            
        '''frm0'''

            
        '''frm1'''
        def radCall(): #选键功能函数
            global flag
            flag=-1
            radSel = v.get()
            if radSel == 1:
                flag=16
            elif radSel == 2:
                flag=10
            elif radSel == 3:
                flag=2
            elif radSel == 4:
                flag=0
        v = IntVar()
        s = ['十六进制','十进制','二进制','原始字符']
        for i in range(4):
            self.RSA_Tlabfrm01.columnconfigure(i,weight=1)    
            exec('self.RSA_Tlabfrm01_r%i = Radiobutton(self.RSA_Tlabfrm01,text="密文以%s显示",variable=v,font=(10),value=%s,command=radCall)'%(i,s[i],i+1))
            eval('self.RSA_Tlabfrm01_r%i'%i).grid(row=0,column=i,pady=5,ipadx=10)      
        
        '''frm2'''
        
        
        '''Tlabfrm1中'''
        self.RSA_Tlabfrm1.rowconfigure(0,weight=1)
        s = ['明文','密文']
        for i in range(2):
            self.RSA_Tlabfrm1.columnconfigure(i,weight=1)
            exec('self.RSA_Tlabfrm1%s = LabelFrame(self.RSA_Tlabfrm1,text="%s",font=("微软雅黑",10))'%(i,s[i]))
            eval('self.RSA_Tlabfrm1%s'%i).grid(row=0,column=i,stick=NSEW,padx=5,pady=5)
            eval('self.RSA_Tlabfrm1%s'%i).rowconfigure(0,weight=1)
            eval('self.RSA_Tlabfrm1%s'%i).columnconfigure(0,weight=1)
            exec('self.RSA_Tlabfrm1%s_s%s = sclt.ScrolledText(self.RSA_Tlabfrm1%s,font=("隶书",15))'%(i,i,i))
            eval('self.RSA_Tlabfrm1%s_s%s'%(i,i)).grid(row=0,column=0,padx=5,pady=5,stick=NSEW)

            
        '''在文件加密labfrm创建frm0，frm1''' 
        self.RSA_Dlabfrm.columnconfigure(0,weight=1) #列权重
        for i in range(2):
            self.RSA_Dlabfrm.rowconfigure(i,weight=1) #行权重
            exec('self.RSA_Dlabfrm%s = Frame(self.RSA_Dlabfrm)'%i)
            eval('self.RSA_Dlabfrm%s'%i).grid(row=i,column=0,stick=NSEW)
            eval('self.RSA_Dlabfrm%s'%i).rowconfigure(i,weight=1)
        
        '''Dlabfrm中的frm0框'''
        for i in range(4):
            self.RSA_Dlabfrm0.columnconfigure(i,weight=1)
        self.RSA_flab = Label(self.RSA_Dlabfrm0,text="文件名称：", font=('微软雅黑',13))
        self.RSA_flab.grid(row=0,column=0,padx=1,stick=E)
        self.RSA_fe = Entry(self.RSA_Dlabfrm0,width=100)
        self.RSA_fe.grid(row=0,column=1,padx=1,stick=W)        
        
        '''Dlabfrm中的frm1框'''

            
        def initialize(): #小窗口函数
            m = r.disp()
            small_window = Tk(className='公钥与秘钥')
            width = 380
            height = 250
            smwinwidth = small_window.winfo_screenwidth()
            smwinhight = small_window.winfo_screenheight()
            alignstr = '%dx%d+%d+%d'%(width,height,(smwinwidth-width)/2,(smwinhight-height)/2)
            small_window.geometry(alignstr)
            small_window.resizable(width=0, height=0) #窗口长宽高可变(1)
           
            small_window.columnconfigure(0,weight=1)
            for i in range(3):
                small_window.rowconfigure(i,weight=1)
            
            '''框内标签'''
            labfrm0 = LabelFrame(small_window, text = '公钥',font=(10))
            labfrm0.grid(row=0,column=0,padx=5,pady=5,stick=NSEW,ipadx=5,ipady=5)
            labfrm1 = LabelFrame(small_window, text = '密钥',font=(10))
            labfrm1.grid(row=1,column=0,padx=5,pady=5,stick=NSEW,ipadx=5,ipady=5)  
            
            '''公钥'''
            labfrm0.rowconfigure(0,weight=1)
            for i in range(4):
                labfrm0.columnconfigure(i,weight=(1 if i%2==0 else 4))
            s = ['n','e']
            for i in range(2):
                exec('l%s = Label(labfrm0, text="%s"+":")'%(i,s[i]))
                eval('l%s'%i).grid(row=0,column=i+i%2)
                exec('e%s = Entry(labfrm0)'%i)
                eval('e%s'%i).grid(row=0,column=i+2**i)
            
            '''秘钥'''
            for i in range(2):
                labfrm1.rowconfigure(i,weight=1) #行权重
            for i in range(4):
                labfrm1.columnconfigure(i,weight=(1 if i%2==0 else 4)) #列权重
            s = ['p','q','d','φ(n)']
            e2 = Entry(labfrm1,show="*")
            e3 = Entry(labfrm1,show="*")
            e4 = Entry(labfrm1,show="*")
            e5 = Entry(labfrm1,show="*")
            for i in range(2,6):
                exec('l%s = Label(labfrm1, text="%s"+":")'%(i,s[i-2]))
                eval('l%s'%i).grid(row=(0 if i%2==0 else 1),column=(i-2 if i%2==0 else i-3))
                #exec('e%s = Entry(labfrm1,show="*")'%i)
                eval('e%s'%i).grid(row=(0 if i%2==0 else 1),column=(i-1 if i%2==0 else i-2))
            

            '''将公钥 密钥显示'''
            for i in range(6):
                eval('e%s'%i).insert(INSERT,('%s'%m[i]))
       
            frm = Frame(small_window)
            frm.grid(row=2,column=0,stick=NSEW)
            frm.rowconfigure(0,weight=1)
            frm.columnconfigure(0,weight=1)
            
            frm0 = Frame(frm)
            frm1 = Frame(frm)
            f = [frm0,frm1]
            for i in range(2):
                f[i].grid(row=i,column=0,stick=NSEW)
                f[i].rowconfigure(0,weight=1)
                frm0.columnconfigure(i,weight=1)
            frm1.columnconfigure(0,weight=1)


            '''查看，输入，返回主题窗口的按钮'''
            def check():#查看
                x = [e2,e3,e4,e5]
                for i in range(2,6):
                    x[i-2].destroy()
                    x[i-2] = Entry(labfrm1)
                    x[i-2].grid(row=(0 if i%2==0 else 1),column=(i-1 if i%2==0 else i-2))
                    x[i-2].insert(INSERT,('%s'%m[i]))
                
                def hide(): #隐藏'p','q','d','φ(n)'
                    b.destroy()
                    x = [e2,e3,e4,e5]
                    for i in range(2,6):
                        x[i-2].destroy()
                        x[i-2] = Entry(labfrm1,show="*")
                        x[i-2].grid(row=(0 if i%2==0 else 1),column=(i-1 if i%2==0 else i-2))
                        x[i-2].insert(INSERT,('%s'%m[i]))
                b = Button(frm0,text="隐藏",width=10,command=hide)
                b.grid(row=0,column=0,pady=5)
                    
            def entring():#输入
                labfrm0.destroy()
                labfrm1.destroy()
                frm.destroy()
                small_window.title('输入p q e')
                width = 220
                height = 125
                smwinwidth = small_window.winfo_screenwidth()
                smwinhight = small_window.winfo_screenheight()
                alignstr = '%dx%d+%d+%d'%(width,height,(smwinwidth-width)/2,(smwinhight-height)/2)
                small_window.geometry(alignstr)
                
                for i in range(2):
                    small_window.rowconfigure(i,weight=1)
                small_window.columnconfigure(0,weight=1)
                
                frm0 = Frame(small_window)
                frm1 = Frame(small_window)
                f = [frm0,frm1]
                for i in range(2):
                    f[i].grid(row=i,column=0,stick=NSEW)
                    frm0.rowconfigure(i,weight=1)
                    frm0.columnconfigure(i,weight=1)
                    frm1.columnconfigure(i,weight=1)
                frm0.rowconfigure(2,weight=1)
                frm1.rowconfigure(0,weight=1)
                
                def right():#确定
                    try:
                        p = int(ce0.get())
                        q = int(ce1.get())
                        e = int(ce2.get())
                        if r.change(p,q,e):
                            pass
                        else:
                            askyesno(title='提示', message=f'n={p}x{q}={p*q},e={e}为非法输入（255<n<10000且e>1）')
                    except:
                        askyesno(title='提示', message='请输入有效字符')
                    small_window.destroy()    
                    initialize()
                def cancel():#取消
                    small_window.destroy()
                    initialize()
                    
                s = ['p','q','e']
                x = [['确定','right'],['取消','cancel']]
                ce0 = Entry(frm0)
                ce1 = Entry(frm0)
                ce2 = Entry(frm0)
                for i in range(3):
                    exec('l%s = Label(frm0, text="%s"+":")'%(i,s[i]))
                    eval('l%s'%i).grid(row=i,column=0,stick=E,padx=2,pady=2)
                    #exec('ce%s = Entry(frm0)'%i)
                    eval('ce%s'%i).grid(row=i,column=1,stick=W,padx=2,pady=2)
                for i in range(2):
                    exec('b%s = Button(frm1,text="%s",width=10,height=1,command=%s)'%(i,x[i][0],x[i][1]))
                    eval('b%s'%i).grid(row=0,column=i)
                
            def cancel():#返回上一个界面
                small_window.destroy()
            s = [['查看','check'],['输入','entring'],['返回上一个界面','cancel']]
            f = ['frm0','frm1']
            for i in range(3):
                exec('bt%s = Button(%s, text="%s", width=[10,10,15][i], height=1, command=%s)'%(i,f[[0,0,1][i]],s[i][0],s[i][1]))
                eval('bt%s'%i).grid(row=0,column=[0,1,0][i],pady=5)
            
            small_window.mainloop()  

        def encrypt():#加密
            self.RSA_Tlabfrm11_s1.delete(0.0,'end')
            m = self.RSA_Tlabfrm10_s0.get(0.0,'end')[:-1]
            r.encryption(m)
            if flag == 0:
                self.RSA_Tlabfrm11_s1.insert(INSERT,('%s'%r.show_ctext()))
            else:
                self.RSA_Tlabfrm11_s1.insert(INSERT,('%s'%r.showc_in_num(flag)))
        
        def decrypt():#解密
            self.RSA_Tlabfrm10_s0.delete(0.0,'end')
            c = self.RSA_Tlabfrm11_s1.get(0.0,'end')[:-1]
            r.dencryption(c, flag)
            self.RSA_Tlabfrm10_s0.insert(INSERT,('%s'%r.show_mtext()))

        def clear_1(): #清空明文
            self.RSA_Tlabfrm10_s0.delete(0.0,'end')
            
        def clear_2(): #清空密文
            self.RSA_Tlabfrm11_s1.delete(0.0,'end')

        def open_mfile():
            global file_path
            global file_text
            try:
                file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('H:/')))
                if file_path !="":
                    filename, file_text = readfile(file_path)
                    #插入文件名
                    self.RSA_fe.delete(0,"end")
                    self.RSA_fe.insert(INSERT, ('%s' % filename))
                    #插入文件内容
                    self.RSA_Tlabfrm10_s0.delete(0.0, 'end')
                    self.RSA_Tlabfrm10_s0.insert(INSERT, ('%s' % file_text))

                    window = Tk()
                    window.title('加密')
                    width = 500
                    height = 70
                    smwinwidth = window.winfo_screenwidth()
                    smwinhight = window.winfo_screenheight()
                    alignstr = '%dx%d+%d+%d'%(width,height,(smwinwidth-width)/2,(smwinhight-height)/2)
                    window.geometry(alignstr)
                    window.rowconfigure(0,weight=1)
                    window.columnconfigure(0,weight=1)
                    window.columnconfigure(1,weight=5)                     
                    # 设置下载进度条
                    Label(window, text='加密中', ).grid(row=0,column=0,stick=E)
                    canvas = Canvas(window, width=400, height=22, bg="white")
                    canvas.grid(row=0,column=1)
                    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
                    x = len(file_text)//4 + 1
                    n = 500 / x  # 500是矩形填充满的次数
                    c = ''
                    if flag == 0:
                        i = -1
                        for i in range(x-1):
                            r.encryption(file_text[4*i:4*(i+1)])
                            n = n + 465 / x
                            canvas.coords(fill_line, (0, 0, n, 60))
                            window.update()
                            c = c + r.show_ctext()
                        if len(file_text[4 * (i + 1):])>0:
                            r.encryption(file_text[4 * (i + 1):])
                            c = c + r.show_ctext()
                    else:
                        i = -1
                        for i in range(x - 1):
                            r.encryption(file_text[4*i:4 * (i + 1)])
                            n = n + 465 / x
                            canvas.coords(fill_line, (0, 0, n, 60))
                            window.update()
                            c = c + r.showc_in_num(flag)
                        if len(file_text[4 * (i + 1):])>0:
                            r.encryption(file_text[4 * (i + 1):])
                            c = c + r.showc_in_num(flag)

                    self.RSA_Tlabfrm11_s1.delete(0.0, 'end')
                    self.RSA_Tlabfrm11_s1.insert(INSERT, ('%s' % c))
            except:
                if flag == None:
                    askyesno(title='提示', message='请选择文本显示形式')
            finally:#最终清除进度条窗口
                window.destroy()
        def open_cfile():
            global file_path
            global file_text
            try:
                file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('H:/')))
                if file_path !="":
                    filename,file_text=readfile(file_path)
                    window = Tk()
                    window.title('加密')
                    width = 500
                    height = 70
                    smwinwidth = window.winfo_screenwidth()
                    smwinhight = window.winfo_screenheight()
                    alignstr = '%dx%d+%d+%d'%(width,height,(smwinwidth-width)/2,(smwinhight-height)/2)
                    window.geometry(alignstr)
                    window.rowconfigure(0,weight=1)
                    window.columnconfigure(0,weight=1)
                    window.columnconfigure(1,weight=5)                     
                    # 设置进度条
                    Label(window, text='解密中', ).grid(row=0,column=0,stick=E)
                    canvas = Canvas(window, width=400, height=22, bg="white")
                    canvas.grid(row=0,column=1)
                    self.RSA_fe.delete(0,"end")
                    self.RSA_fe.insert(INSERT, ('%s' % filename))
                    self.RSA_Tlabfrm11_s1.delete(0.0, 'end')
                    self.RSA_Tlabfrm11_s1.insert(INSERT, ('%s' % file_text))
                    m = ''

                    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
                    x = len(file_text) // 8 + 1
                    n = 500 / x  # 500是矩形填充满的次数
                    if flag == 0:
                        i = -1
                        for i in range(x - 1):
                            r.dencryption(file_text[8 * i:8 * (i + 1)], 0)
                            n = n + 465 / x
                            canvas.coords(fill_line, (0, 0, n, 60))
                            window.update()
                            m = m + r.show_mtext()
                        r.dencryption(file_text[8 * (i + 1):], 0)
                        m = m + r.show_mtext()
                    else:
                        filename, file_text = readfile(file_path)
                        self.RSA_fe.delete(0, "end")
                        self.RSA_fe.insert(INSERT, ('%s' % filename))
                        self.RSA_Tlabfrm11_s1.delete(0.0, 'end')
                        self.RSA_Tlabfrm11_s1.insert(INSERT, ('%s' % file_text))
                        r.dencryption(file_text, flag)
                        m = r.show_mtext()
                    self.RSA_Tlabfrm10_s0.delete(0.0, 'end')
                    self.RSA_Tlabfrm10_s0.insert(INSERT, ('%s' % m))
            except Exception as e:
                if flag == None :
                    askyesno(title='提示', message='请选择文本显示形式')
                else:
                    askyesno(title='提示', message='解密失败（公钥是否正确？文本显示形式是否选择正确？）')
            finally:#最终清除进度条窗口
                window.destroy()

        def save_cfile():
            file_path = filedialog.asksaveasfilename(title=u'保存文件', defaultextension='.txt', filetypes=[("文本文件txt", ".txt"),("word格式",".docx"),("所有格式","*")])
            file_text = self.RSA_Tlabfrm11_s1.get('0.0', 'end')[:-1]

            if file_path != '':
                if savefile(file_path,file_text) == 0:
                    askyesno(title='提示', message='密文保存完成')
                else:
                    askyesno(title='提示', message='密文保存失败')
            else:
                askyesno(title='提示', message='未保存')

        def destroy():
            window.destroy()
        '''按钮分布'''
        s = [['查看公钥/密钥','initialize'],['切换成DES','self.change_DES'],\
             ['加密','encrypt'],['解密','decrypt'],['清空明文','clear_1'],['清空密文','clear_2'],\
             ['加密明文文件','open_mfile'],['解密密文文件','open_cfile'],['保存密文','save_cfile'],['退出','destroy']]
        x = ['self.RSA_Tlabfrm00','self.RSA_Tlabfrm02','self.RSA_Dlabfrm1']
        for i in range(10):
            eval('%s'%x[[0,0,1,1,1,1,2,2,2,2][i]]).columnconfigure([0,1,0,1,2,3,0,1,2,3][i],weight=1)
            exec('self.RSA_b%s = Button(%s,text="%s",width=13,font=(10),command=%s)'%(i,x[[0,0,1,1,1,1,2,2,2,2][i]],s[i][0],s[i][1]))
            eval('self.RSA_b%s'%i).grid(row=0,column=[0,1,0,1,2,3,0,1,2,3][i],pady=10,ipady=2)
        

    def change_DES(self,):
        self.RSA.destroy()
        global flag
        flag = None
        DES(self.master)

        
if __name__=='__main__':
    window = Tk()
    Window(window)
    window.mainloop()
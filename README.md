# Encryption
      本软件完善于2020.12.3，因为本软件涉及读取文件的操作，可能会有一些杀毒软件会认为在进行高风险操作。
      数据加密器可以实现DES加密和RSA加密。
      
一、DES
       密钥：需要输入四个字作为密钥。
       密文：①目前可以选择三种格式（十六进制，二进制，原始字符串）输出；
	 ②密文在解密时应当选择好使用的密文的格式，否者无法解密成功。
       明文：支持直接读取文件或文本框输入。
       文件操作：①目前仅支持文本文档形式。


二、RSA
       密钥：①因为默认使用的是随机生成密钥，为了方便使用，公钥和密钥一并给出（每次打开软件均会随机生成公钥密钥）；
	 ②若自行输入密钥应当p*q比255大（因为一个字符串使转二进制时得到的
01串共16位，一个字符串分割成两个8位的01串，所以m应小于2^8）；
	 ③受限于计算机算力，p和q均需小于100。
       密文：①目前可以选择四种格式（十六进制，十进制，二进制，原始字符串）输出；
	 ②密文在解密时应当选择好使用的密文的格式，否者无法解密成功。
       明文：支持直接读取文件或文本框输入。
       文件操作：①目前仅支持文本文档形式。


      数据加密器DES及RSA使用源码已在个人csdn账户（https://blog.csdn.net/weixin_44849854?spm=1010.2135.3001.5113）
公开。目前作者水平有限，目前仅支持文本文档类型的文件操作，且仅在window10系统内测试过，建议用win10系统打开本软件。
日后可能会在个人博客中更新。

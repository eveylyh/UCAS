# UCAS
UCAS-sep文献自动下载
2023.7.26:
该代码用于国科大学生使用sep账号/密码自动访问文献下载库的文献并下载，目前实现的库有  
          86: "ACS",  
          100: "Elsevier-SD",    
          64: "SpringerLink全文电子期刊",  
          3: "ACM Digital Library全文数据库(国际)",  
          51: "RSC（英国皇家化学学会）电子期刊及数据库(国际)",  
          38: "IEEE/IET Electronic library(IEL全文数据库)",  
          31: "EI Compendex（美国工程索引）"  
          
使用代码需要安装chrome浏览器和对应版本的chromedriver，文件里自带的chromedriver是115.0.5790.110win 64，需要替换成自己电脑chrome版本的  ，使用前需要手动在gui_outside.py USERNAME和PASSWORD填入自己的sep账号 

万事俱备运行gui_outside.py即可 

            "使用指南:\n"  
            "1.输入doi后选择对应的数据库，点击猫头下载\n"  
            "2.点击下载后网页会自动运行到pdf浏览页面，无需手动点击\n"  
            "3.运行过程中如果遇到网页更新缓慢可手动刷新当前页面\n"  
            "4.代码运行到pdf浏览页面时需要手动点击chrome下载键，"  
            "如果显示下载失败可点击打印图标选择另存为pdf\n"  
            "5.登录时如果需要输入验证码，在运行终端输入后回车键提交即可\n"  
            "6.首次登陆会自动保存cookies文件在本地\n"  
            "7.EI数据库下载pdf无需手动点击，会自动下载到DEFAULT_DOWNLOAD_PATH\n"  
            "8.同一时间只能下载一篇文献，点击关闭浏览器/手动关闭浏览器后可以继续使用gui页面下载另一篇"  
gui页面如图所示
![image](https://github.com/eveylyh/UCAS/assets/39935896/64465fe5-efc1-4037-a895-5d64c5ff3044)


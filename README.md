# phantom-tank
幻影图，双重图自动生成
使用方法：

1.将py文件下载到本地
2.创建new，in，out三个文件夹
3.把要当做表层的图片按顺序放入out，里层放入in
4.运行
5.程序会根据图片最后访问时间排序，把两个文件夹里排名相同的合成一张幻影图

plus：程序会自动调整输入图片大小，格式，最后输出png格式

我是在ubuntu调试的，windows可能需要一些调整，方法如下：

进程池中是不会报错的，先改为下图，debug后改回来

![图片](https://user-images.githubusercontent.com/67435618/112637323-fbffd800-8e78-11eb-8675-5e99126792f4.png)

通常可能是37行的函数在windows下读取到的目录格式不同造成的，可修改第37行为
![2021-03-26 21-40-18 的屏幕截图](https://user-images.githubusercontent.com/67435618/112640043-ec35c300-8e7b-11eb-9e96-48bd5d8890aa.png)

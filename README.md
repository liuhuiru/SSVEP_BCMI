# SSVEP_BCMI
我的毕业工作：这是一个基于SSVEP-BCI的脑机音乐接口系统，可以让用户使用眼睛注视选择音符，再由AI拓展生成音乐。

自采数据集地址：https://github.com/liuhuiru/mySSVEPDatasets



### SSVEP信号分类

主要参考的两篇文献（这两篇文章都公开了代码）：

- https://ieeexplore.ieee.org/document/9594841
- https://iopscience.iop.org/article/10.1088/1741-2552/ab6a67

两个公开数据集：

- [1] Nakanishi M, Wang Y, Wang Y T, et al. A comparison study of canonical correlation analysis based methods for detecting steady-state visual evoked potentials[J]. PloS one, 2015, 10(10): e0140703.https://github.com/mnakanishi/12JFPM_SSVEP/tree/master/data

- [1] Wang Y, Chen X, Gao X, et al. A benchmark dataset for SSVEP-based brain–computer interfaces[J]. IEEE Transactions on Neural Systems and Rehabilitation Engineering, 2016, 25(10): 1746-1752.链接：https://pan.baidu.com/s/1kwrAW08kV9uFhuM8PpXfnA 
  提取码：g87l

  

### SSVEP-BCI

offline.py：用于离线采集程序

online.py：用于在线准确率测试

online_with_AImusic.py：用户根据引导选择音符

online_with_AImusic_withoutcue：用户自主选择音符

EEGModel文件夹：model文件夹中因存放你自己训练好的深度模型分类器

music文件夹：存放音乐相关，包括生成读取midi音乐，系统发声使用的是pretty_midi和pygame库，需要事先安装



### AI音乐生成参考

github（上面有详细的代码）：https://github.com/haryoa/note_music_generator

博客（需要用科学上网打开）：https://towardsdatascience.com/generate-piano-instrumental-music-by-using-deep-learning-80ac35cdbd2e

文献（见文件夹selfAttention_BiGRU）：Deep Learning for Music.pdf

kaggle（可以在这个网站上建立一个自己的项目训练网络，如果自己的电脑上没有gpu的话训练网络会很慢，这个网站可以白嫖gpu，推荐使用）：https://www.kaggle.com/code/huiruliu/music-generator



ps：

一篇很好的博客（可以帮助了解AI生成音乐）：https://eurychen.me/post/music/ai-compose-music/

music/model文件夹中存放了两个已经训练好的模型，一个迭代了50次，一个迭代了100次

资料是后期整理的，所以运行的时候报错很有可能是文件路径错误，可以自己检查一下

## App Review Analysis

### 目标(站在一个产品生产者的角度), 有产品
- 目的是 改进自家产品, 监控竞争产品
- 找到有意义的评论, 对改进产品有价值
- 看看大家怎么看待App内的某个功能
- 找到产品的缺点
  - crash/闪退: freezes,stop,trouble,lose,lost,reset,shut,shuts
  - ad: ad,ads,adds,add
  - 
- 用户提的建议/新需求
- 用户对功能的建议/表扬/批评/抱怨
- 脏数据过滤:
    - 无意义好评
    - 垃圾广告
    - 
- 如何处理表情包
- 差评
- 发现bug: work,problem,bug,crushes


### 统计分析;
- 贷款类:
  - 目的: 揭示网贷的阴暗面:
    - 既然刷评这么多, 与其识别他们过滤他们, 不如根据关键词挑重点的出来看
    - 害人不浅: 上岸, 后悔, 威胁, 催收, 催债, 谩骂
  - 字数分布
  - 评分分布
  - tf-idf 词云图
  - 客服回复率
  
- 摄影类
- 

### 目标(站在产品方向的定位角度), 未有产品
- 研究这种类型的App 口碑怎样, 有没有价值开发
- 

### 目标(站在要下载/购买的用户的立场)
- 用户不可能对比大量评论, 再选择购买/下载mobile app
- 而且应用商店的排序和筛选都过于粗糙
- 如何快速地帮用户定位到, 别人对用户感兴趣的功能做的评价
- 比如视频剪辑app 这么多, 哪款的功能最适合劳资

### 文本情感分析
- 根据文本和 label(stars), 训练一个 app review sentiment analysis model
- 第一次贷款的心情 -> 从此贷款深似海

### 文本聚合
- 将具有相似语义的文本聚合, 方便分析
- 

### 自动生成文本内容
- 生成积极评论


### 方法论
- 特征关键词
  - 广告相关
  - 差评
  - 
- 如何特征处理:
    - 重要的词: tf-idf
- 

### 他山之石
- Review Data -> FCA(Feature Extraction) -> Sentiment Analysis -> Recommendation (Tree Similarity) -> Report


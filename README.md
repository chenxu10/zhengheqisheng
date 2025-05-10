# 正合奇胜

> 以二敌一，则一术为正，一术为奇 曹操

该软件旨在解决一个问题：如何对幂律支配下的尾部期权进行相对定价？

交易员一旦聆听到当时当日市场的锚定价格，就可以用回测模拟得出的alpha尾部指数和相对定价公式，对OTM期权进行定价。

例子：如果输入SPX ATM的Call Price, Strike Price,Spot和尾部指数alpha就可以计算出任意的价外期权的call的价格。

## 参考文献
1. Taleb, N. N., Yarckin, B., Mann, C., Delic, D., & Spitznagel, M. (2019). Tail option pricing under power laws. arXiv:1908.02347. arXiv 

## (TODO)
- (TODO) Add input interface
- (TODO) Build automatic build using github action
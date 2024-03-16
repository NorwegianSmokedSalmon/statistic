# statistic

### Robocup 数据统计，包括射门次数、控球率、传球次数等

### 开发环境：

python3.8 + kivy2.3.0，建议用anaconda管理环境，创建虚拟环境运行

### 使用方式：
比赛开始时进行数据统计，在终端运行： \\
python3 statistic.py \\
按下*ctrl+c*停止运行会向data.txt写入数据 \\
之后在终端输入: \\
python3 TechnicalBoard.py \\
激活图形化界面，可以查看我方和敌方的总体数据和我方单个机器人的数据
### 图形化界面
![截图 2024-03-16 14-48-13](https://github.com/NorwegianSmokedSalmon/statistic/assets/131785818/f0762354-07dd-411e-8ffd-8d91978aed32)
![截图 2024-03-16 14-47-57](https://github.com/NorwegianSmokedSalmon/statistic/assets/131785818/c96ff588-5296-4b8a-b629-27b92df27033)
![截图 2024-03-16 14-47-26](https://github.com/NorwegianSmokedSalmon/statistic/assets/131785818/e92a6677-2e66-4bb5-9482-414db9638ed0)
### 优化方向
* 优化图形化界面
* 射门传球数据统计更精确

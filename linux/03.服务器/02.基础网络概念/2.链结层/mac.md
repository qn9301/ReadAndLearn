



#### 为什么资料量最小要46最大为1500 btyes呢？

若要侦测碰撞，则讯框总数据量最小得要有64 bytes，那再扣除目的地址、来源地址、检查码（前导码不算）后，就可得到数据量最小得要有46 bytes。

64 - 46 = 18 = 目的地址6 + 来源地址6 + 资料栏位通信2 + 检查码4

硬件地址00:00:00:00:00:00到FF:FF:FF:FF:FF:FF这6 bytes。前 3 bytes为厂商的代码，后 3 bytes则是该厂商自行设定的装置码。
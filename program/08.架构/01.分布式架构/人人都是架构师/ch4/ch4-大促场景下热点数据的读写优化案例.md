

# 第4章 大促场景下热点数据的读/写优化案例

## 4.1 缓存技术简介

* 缓存
  * 静态资源数据缓存在CDN
  * 反向代理服务器缓存状态更新不频繁的静态资源数据
  * 缓存从数据库等存储系统中的数据

### 4.1.1 使用Ehcache实现数据缓存

* Ehcache本地缓存
  * maxElementsInMemory指定缓存的最大个数
  * eternal缓存是否永久有效
  * timeToLiveSeconds指定缓存数据的失效时间
  * overflowToDisk指定缓存数量超过maxElementsInMemory阈值时，是否固化到磁盘
  * memoryStoreEvictionPolcy指定缓存的回收策略，默认为LRU最近最少，FIFO先进先出，LFU较少使用

### 4.1.3 神秘的off-heap技术

* off-heap堆外内存
  * TaobaoVM使用GCIH(GC invisible heap)，生命周期较长的Java对象从heap中移至heap外，GC不能管理GCIH中的对象，降低GC频率
  * ByteBuffer.allocateDirect()操作实际的物理内存资源
  * DirectByteBUffer对象存储在heap空间，GC回收DirectByteBuffer，其背后的堆外内存也会被释放 

## 4.2 高性能分布式缓存Redis简介

### 4.2.1 使用Jedis客户端操作Redis

### 4.2.2 使用Redis集群实现数据水平化存储

## 4.3 同一热卖商品高并发读需求

### 4.3.1 Redis集群多写多读方案

* 多写多读
  * 多写实现数据的冗余存储
  * 将之前的单写改为多写
* 问题
  * 保证多写过程中数据的一致性
  * 集群动态扩容，Key需重新进行计算

### 4.3.2 保障多写时的数据一致性

* ZooKeeper
  * Znode发生改变，所有的客户端全量更新本地持有的Key
* 多写失败的情况
  * 网络环境发生抖动
  * Master/Slave切换
  * Master/Slave全部宕机，集群环境重新分配Slot区间

### 4.3.3 LocalCache结合Redis集群的多级Cache方案

* 缓存
  * 访问热度不高的商品直接访问分布式缓存
  * 本地缓存存储访问热度较高的热卖商品
  * 本地缓存两类数据：商品详情和商品库存

### 4.3.4 实时热点自动发现方案

* 热点
  * HotKey配置在集中式资源配置中心内
  * 实时热点自动发现机制来进行热点保护

## 4.4 同一热卖商品高并发写需求

* 热卖
  * 多级Cache
  * 将热卖商品库存的扣减操作转移到关系型数据库外
  * 合理控制并发写的流量

### 4.4.1 InnoDB行锁引起数据库TPS下降

* InnoDB行锁
  * 大量针对数据库同一行记录的并发更新操作
  * InnoDB默认会对同一行数据记录加锁
  * 乐观锁
  * SELECT * FROM information schema.INNODB_TRX WHERE trx_state='LOCK WAIT';

### 4.4.2 在Redis中扣减热卖商品库存方案

* Redis
  * 数据库中存储的商品库存可以被理解为实际库存
  * Redis中存储的商品库存则为实时库存
* 分布式锁
  * Redisson
  * lock()在某一个获取到锁的线程未释放锁之前，其他线程只能等待
  * tryLock
  * 系统获取到分布式锁并成功扣减Redis中的实时库存后，将消息写入消息队列，由消费者负责实际库存的扣减

### 4.4.3 热卖商品库存扣减优化方案

* 优化
  * 批量提交扣减商品库存
  * 当前端发起库存扣减请求后，先进行收集，达到阈值后再做合并处理，一次性提交
  * 当商品库存不足扣减时，一批库存扣减操作都将失败
* Watch命令实现乐观锁
  * Watch命令对目标Key进行标记
  * 事务提交后，监控到目标Key发生改变，版本号发生改变，本次事务提交操作就需要回滚

### 4.4.4 控制单机并发写流量方案

* 单机并发
  * 单机排队串行写
  * 抢购限流
* 单机串行
  * 将库存扣减操作设置队列串行执行，降低同一热卖商品并发写的流量
  * 控制并发写的流量，降低数据库的负载压力

### 4.4.5 使用阿里开源的AliSQL数据库提升秒杀场景性能

* AliSQL
  * 批量提交扣减商品库存
  * 先收集库存扣减请求，达到阈值后做合并处理，最后批量进行提交
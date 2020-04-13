## Solution

### 1. 设计思路
流程:
- 编写测试用例`class BestChargeTest`;
- 初始化数据, 用`namedtuple`模拟数据Model, 构造 DataLoader, 以便加载数据;
- 定义类BestCharge, 封装折扣的计算过程;
- 定义函数`parse_input()`处理原始输入, 并在 处理过程中打印菜品明细;
- 分别定义函数`reward_charge()` 和 `discount_charge()` 实现满减和指定商品半价的计算, 并保存计算过程的信息, 以便之后选出最佳啊优惠方式后打印;
- 对输入分别计算 所有的优惠方式, 然后排序取出最佳优惠方式和最低价格, 以便拓展更多的优惠方式;
- 根据最佳优惠方式, 打印计算信息

### 2. 运行方法
- `python best_charge.py`
- 执行测试: `python test.py`

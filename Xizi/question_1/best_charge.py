from collections import OrderedDict

from data import data_loader

LINE_LENGTH = 35


class PromotionType(object):
    Reward = 1
    Discount = 2


promotion2template = {
    PromotionType.Reward: """使用优惠:\n满{threshold}减{reward}元，省{delta}元""",
    PromotionType.Discount: """使用优惠:\n指定菜品半价({items})，省{delta}元"""
}


def print_line(num, sign='-'):
    print(sign*num)


class BestCharge(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.item_count_map = self.parse_input()
        self.message = {}  # 一个地方存储计算过程
        self.origin_price = sum([item.price * count for item, count in self.item_count_map])
        self.promotion2func = OrderedDict({
            PromotionType.Reward: self.reward_charge,
            PromotionType.Discount: self.discount_charge
        })

    def parse_input(self):
        """
        :return: list of tuple (Item, Int)
        """
        outputs = list()
        print("============= 订餐明细 =============")
        for token in self.tokens:
            item_id, count = token.split('x')
            count = int(count.strip())
            item = data_loader.get_item_by_id(item_id.strip())
            if not item:
                raise Exception("Invalid Item ID: {}, Please Check your input: {}".format(item_id, self.tokens))
            print("{} x {} = {}元".format(item.name, count, item.price * count))
            outputs.append((item, count))
        print_line(LINE_LENGTH)
        return outputs

    def reward_charge(self):
        """
        满减的计算方式
        :return: total price
        """
        template = promotion2template.get(PromotionType.Reward)
        promotion = data_loader.get_active_reward_promotion()
        price = self.origin_price if self.origin_price < promotion.threshold else \
            (self.origin_price - promotion.reward)
        delta = self.origin_price - price
        if delta:
            self.message[PromotionType.Reward] = template.format(
                delta=delta, threshold=promotion.threshold, reward=promotion.reward)
        return price

    def discount_charge(self):
        """
        约束 输入输出: 策略模式
        指定商品打折的计算方式
        :return: total price
        """
        price = 0
        template = promotion2template.get(PromotionType.Discount)
        for item, count in self.item_count_map:
            price += item.discount * item.price * count
        delta = self.origin_price - price
        names = ", ".join([item.name for item, count in self.item_count_map])
        if delta:
            self.message[PromotionType.Discount] = template.format(delta=delta, items=names)
        return price

    def print_charge_detail(self, promotion_type):
        if self.message.get(promotion_type):
            print(self.message[promotion_type])
            print_line(LINE_LENGTH)

    def best_charge(self):
        prom2price = [(pt, func()) for pt, func in self.promotion2func.items()]
        best_promotion, lowest_price = sorted(prom2price, key=lambda x: x[1])[0]
        self.print_charge_detail(best_promotion)
        print("总计：{}元".format(lowest_price))
        print_line(LINE_LENGTH, '=')
        return lowest_price


if __name__ == '__main__':
    tokens = ["ITEM0013 x 4"]
    BestCharge(tokens).best_charge()
    tokens = ["ITEM0013 x 4", "ITEM0022 x 1"]
    BestCharge(tokens).best_charge()
    tokens = ["ITEM0001 x 1", "ITEM0013 x 2", "ITEM0022 x 1"]
    BestCharge(tokens).best_charge()

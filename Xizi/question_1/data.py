from collections import namedtuple

Item = namedtuple('Item', ['id', 'name', 'price', 'discount'])
RewardPromotion = namedtuple('RewardPromotion', ['id', 'threshold', 'reward', 'effective_date', 'expiration_date'])


class DataLoader(object):

    @property
    def items(self):
        items = [
            Item('ITEM0001', '黄焖鸡', 18, 0.5),
            Item('ITEM0013', '肉夹馍', 6, 1),
            Item('ITEM0022', '凉皮', 8, 0.5),
        ]
        return items

    @property
    def reward_promotions(self):
        reward_promotions = [
            RewardPromotion(1, 30, 6, '2020-03-17', None)
        ]
        return reward_promotions

    def get_item_by_id(self, item_id):
        filtered = list(filter(lambda x: x.id == item_id, self.items))
        if filtered:
            return filtered[0]

    def get_active_reward_promotion(self):
        promotions = list(filter(lambda x: x.expiration_date is None, self.reward_promotions))
        if promotions:
            return promotions[0]


data_loader = DataLoader()

import random


class Generator(object):
    def __init__(self):
        self.ID = 0
        self.timeout = 0

        self.params = {
            'ID': self.ID,
            'Timeout': self.timeout
        }


class SequenceGenerator(Generator):
    def __init__(self, count, start=1, step=1):
        self.start = start
        self.stop = count+1
        self.step = step
        super().__init__()

    def __iter__(self):
        for n in range(self.start, self.stop, self.step):
            self.params['ID'] = n
            yield self.params


class ListGenerator(Generator):
    def __init__(self, lst):
        self.lst = lst
        super().__init__()

    def __iter__(self):
        for n in self.lst:
            self.params['ID'] += 1
            yield self.params


class AllocationSequenceGenerator(SequenceGenerator):
    def __iter__(self):
        for params in super().__iter__():
            self.params['Side'] = 'Sell'
            yield params

            self.params['Side'] = 'Buy'
            yield params


class SendBroadcastGenerator(SequenceGenerator):
    def __init__(self, count, commodity=None, sell=None, buy=None, qty=0, price=0, max_order=9999):
        self.commodity = commodity
        self.sell = sell
        self.buy = buy
        self.price = price
        self.qty = qty
        self.max_order = max_order
        self.partition = 1

        super().__init__(count)

    def __iter__(self):
        for params in super().__iter__():
            # zID
            self.params['zID'] = str(self.params['ID']).zfill(4)

            # Commodity
            if type(self.commodity) is list:
                current_commodity = self.params['ID'] % len(self.commodity) - 1
                self.params['Commodity'] = self.commodity[current_commodity]
            else:
                self.params['Commodity'] = self.commodity

            # Price
            if self.price == 0:
                params['Price'] = random.randrange(3, 100)
            else:
                params['Price'] = self.price

            # Qty
            if self.qty == 0:
                params['Qty'] = random.randrange(3, 50)
            else:
                params['Qty'] = self.qty

            # Partition
            if params['ID'] % self.max_order == 0:
                params['Partition'] += 1

            #
            # Buy Side
            #
            if type(self.buy) is list:
                params['Participant'] = random.choice(self.buy)
            else:
                params['Participant'] = self.buy
            params['Side'] = 'Buy'
            yield params

            #
            # Sell Side
            #
            if type(self.sell) is list:
                params['Participant'] = random.choice(self.sell)
            else:
                params['Participant'] = self.sell
            params['Side'] = 'Sell'
            yield params

# for x in AllocationSequenceGenerator(10):
#     print(x)

for x in SendBroadcastGenerator(10, commodity='@{Instr.Static}', sell='05', buy='03'):
    print(x)

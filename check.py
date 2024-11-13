import json

class InvStrategy:
    def __init__(self) -> None:
        self.underlying_assert = None
        self.derivative = "autocall"
        self.investment_size = None
        self.fx_risk = None
        self.expected_return = None
        self.horisont = None
        self.capital_risk = None
        self.payout = None

    def is_all_not_none(self):
        return all(value is not None for value in vars(self).values())

    def get_none(self):
        return [key for key, value in vars(self).items() if value is not None]
    
    def get_not_none(self):
        return [key for key, value in vars(self).items() if value is not None]

    def get_all_pairs(self):
        return [f"{key} : {value}" for key, value in vars(self).items() if value is not None]

    def update_by_json(self, json):
        for key, value in json.items():
            if hasattr(self, key) and ((getattr(self, key) == None) or (getattr(self, key) == 'Not matter')) and (value != None):
                setattr(self, key, value)
    
 
json_ = '{"underlying_assert": "equities", "derivative": null, "investment_size": 10000, "fx_risk": null, "expected_return": null, "horisont": null, "capital_risk": null, "payout": null}'

json_ = json.loads(json_)
strategy = InvStrategy()
print([(key, value) for key, value in json_.items()])
for key, value in json_.items():
    print(key, value)
    print(hasattr(strategy, key))
    print(getattr(strategy, key))

strategy.update_by_json(json_)
print(strategy.get_all_pairs())

print(strategy.capital_risk, strategy.expected_return, strategy.investment_size)
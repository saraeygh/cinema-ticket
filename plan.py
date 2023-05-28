from human import User

class plan():
    def __init__(self) -> None:
        pass

    def active():
        pass

    def deactive():
        pass

    def current_state():
        pass


plan = {
    username: {
        "current_plan": "silver",
        "count": 2
    }
}


class silver(plan):
    def active():
        count = 3
    
    def deactive():
        User.current_plan = "Bronze"

    def current_state():
        count -= 1
        if count = 0
        silver.deactive()
        return count
    
    def __str__(self):
        return f"remanied count: {self.count}"

class gold(plan):
    def active():
        datetime = datetime.now()
    
    def deactive():
        User.current_plan = "Bronze"

    def current_state():
        now = datetime.now() - datetime
        gold.deactive()
        

    def __str__(self):
        return f"remanied count: {self.count}"


obj1 = gold()
print(obj)

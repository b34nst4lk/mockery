from objects import *

r"(^[a-zA-Z0-9_.+-]+@\.)"
# Email
username = "^[a-zA-Z0-9_.+-]{3,10}"
domain = "[a-zA-Z0-9-]{3,6}"
tld = "[A-Za-z]{3}"
email = "".join(["(", username, "@", domain, "\.", tld, ")"])
Email = PrimitiveStr(pattern=email, formatter=str.lower)

Sex = PrimitiveEnum(["Male", "Female"])

URL = PrimitiveStr(pattern="www\.[A-Za-z]{1,10}\.com")

# Phone Numbers
SG_Landline = PrimitiveStr(pattern="6[0-9]{7}")
SG_Mobile = PrimitiveStr(pattern="[8-9][0-9]{7}")

User = {
    "user_name": PrimitiveStr(),
    "password":PrimitiveStr(),
    "email": Email,
    "points": PrimitiveInt(lower=0, upper=100),
    "website": URL,
    "home_phone": SG_Landline,
    "mobile": SG_Mobile,
    "Sex": Sex
}

SubscriptionPlan = {
    "type": "subscription_plan",
    "is_trial": PrimitiveBoolean(),
    "user": Collection(PrimitiveStr()),
    "password": PrimitiveStr()
}

GrandChild = {
    "lost_track": Collection(PrimitiveInt())
}

Child = {
    "grandchild": Collection(GrandChild)
}

Parent = {
    "child": GrandChild
}

Queue = {
    "QueueNo": PrimitiveInt(lower=1000, upper=9999),
    "Status": PrimitiveEnum(["Waiting", "Calling", "Missed"])
}

def main():
    print(dict_to_object(User))

if __name__ == "__main__":
    main()

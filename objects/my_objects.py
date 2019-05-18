from .primitives import Int, Str, Enum, Boolean, List, Set

r"(^[a-zA-Z0-9_.+-]+@\.)"
# Email
username = "^[a-zA-Z0-9_.+-]{3,10}"
domain = "[a-zA-Z0-9-]{3,6}"
tld = "[A-Za-z]{3}"
email = "".join(["(", username, "@", domain, r"\.", tld, ")"])
Email = Str(pattern=email, formatter=str.lower)

Sex = Enum(["Male", "Female"])

URL = Str(pattern=r"www\.[A-Za-z]{1,10}\.com")

# Phone Numbers
SG_Landline = Str(pattern="6[0-9]{7}")
SG_Mobile = Str(pattern="[8-9][0-9]{7}")

User = {
    "user_name": Str(pattern=username),
    "password": Str(),
    "email": Email,
    "points": Int(lower=0, upper=100),
    "website": URL,
    "home_phone": SG_Landline,
    "mobile": SG_Mobile,
    "Sex": Sex
}

SubscriptionPlan = {
    "type": "subscription_plan",
    "is_trial": Boolean(),
    "user": List(Str()),
    "password": Str()
}

GrandChild = {
    "lost_track": List(Int())
}

Child = {
    "grandchild": List(GrandChild)
}

Parent = {
    "child": GrandChild
}

Queue = {
    "QueueNo": Int(lower=1000, upper=9999),
    "Status": Enum(["Waiting", "Calling", "Missed"])
}

import random
import pandas as pd
from faker import Faker

fake = Faker()

num_records = random.randint(3600, 4000)

circumstances = [
    "Third Party", "Insured Vehicle changing lanes", "Third Party Hit Insured",
    "Third Party Vehicle changing lanes", "Insured opening door", "Third Party opening door",
    "Insured Vehicle reversing", "Third Party Vehicle reversing",
    "Insured Vehicle Emerging from minor road", "Third Party Emerging from minor road"
]

org_notified_by = ["TP", "Broker", "Self", "Nameddriver", "Employee", "Others"]
method_of_notification = ["Phone", "Email", "Others"]
ncd_indicator = ["Yes", "No"]
liability_group = ["Fully_Liable", "Not_Liable", "Split_Liable"]

def generate_notification_delay():
    if random.random() < 0.8:
        return random.randint(0, 50)
    elif random.random() < 0.15:
        return random.randint(51, 120)
    else:
        return random.randint(121, 350)

data = []
for i in range(1, num_records + 1):
    insured_age = random.randint(18, 75)

    if insured_age < 30 and random.random() < 0.6:
        liability = "Fully_Liable"
    elif random.random() < 0.2:
        liability = "Split_Liable"
    else:
        liability = "Not_Liable"

    row = {
        "Claim_Number": f"CLM{i:05d}",
        "Excess": random.randint(0, 5000),
        "Circumstance": random.choice(circumstances),
        "OrganizationNotifiedBy": random.choice(org_notified_by),
        "MethodofNotification": random.choice(method_of_notification),
        "NCD_Indicator": random.choice(ncd_indicator),
        "Notification_Delay": generate_notification_delay(),
        "Injury": random.choice([0, 1]),
        "ThirdPartyVehicleDamage": random.choice([0, 1]),
        "InsuredVehicleDamage": random.choice([0, 1]),
        "Insured_age": insured_age,
        "EstimatedVehicleValue": random.randint(2000, 50000),
        "Liability_group": liability
    }
    data.append(row)

df = pd.DataFrame(data)

df.to_csv("fake_data.csv", index=False)
print(df.head())

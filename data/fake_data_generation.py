import pandas as pd
import numpy as np
from faker import Faker
import random
import os


fake = Faker()
n = 3800  

save_path = "data"
os.makedirs(save_path, exist_ok=True)
file_path = os.path.join(save_path, "fake_data.csv")

circumstances = [
    "Insured Vehicle Hit Third Party",
    "Insured Vehicle changing lanes",
    "Third Party Hit Insured",
    "Third Party Vehicle changing lanes",
    "Insured opening door",
    "Third Party opening door",
    "Insured Vehicle reversing",
    "Third Party Vehicle reversing",
    "Insured Vehicle Emerging from minor road",
    "Third Party Emerging from minor road"
]

org_notified_by = ["TP", "Broker", "Self", "Nameddriver", "Employee", "Others"]
method_notification = ["Phone", "Email", "Others"]
ncd_indicator = ["Yes", "No"]
liability_group = ["Fully_Liable", "Not_Liable", "Split_Liable"]

def weighted_choice(options, weights):
    return np.random.choice(options, p=weights)

data = []
for i in range(n):
    claim_number = f"CLM{100000+i}"

    circ = np.random.choice(circumstances, p=[0.14,0.11,0.10,0.10,0.10,0.08,0.10,0.08,0.10,0.09])
    org = np.random.choice(org_notified_by, p=[0.20,0.20,0.20,0.15,0.15,0.10])
    method = np.random.choice(method_notification, p=[0.50,0.35,0.15])
    ncd = np.random.choice(ncd_indicator, p=[0.50,0.50])

    notif_delay = np.random.normal(loc=40, scale=30)  
    notif_delay = max(0, min(int(notif_delay), 300))  

    excess = np.random.lognormal(mean=np.log(600), sigma=0.8)
    if random.random() < 0.01:  
        excess *= 5
    excess = round(min(excess, 20000), 2)

    injury = np.random.choice([0, 1], p=[0.55, 0.45])
    tp_damage = np.random.choice([0, 1], p=[0.40, 0.60])
    insured_damage = np.random.choice([0, 1], p=[0.10, 0.90])

    age = int(np.random.normal(35, 12))
    age = max(18, min(age, 75))

    vehicle_value = np.random.lognormal(mean=np.log(15000), sigma=0.7)
    if random.random() < 0.01:
        vehicle_value *= 4
    vehicle_value = min(vehicle_value, 150000)
    vehicle_value = int(vehicle_value)

    if tp_damage == 1 and injury == 1:
        liability = weighted_choice(liability_group, [0.50, 0.25, 0.25])
    elif tp_damage == 1:
        liability = weighted_choice(liability_group, [0.45, 0.28, 0.27])
    elif injury == 1:
        liability = weighted_choice(liability_group, [0.40, 0.30, 0.30])
    else:
        liability = weighted_choice(liability_group, [0.35, 0.33, 0.32])

    if age < 25 and random.random() < 0.3:
        liability = "Fully_Liable"

    if random.random() < 0.08:
        liability = np.random.choice(liability_group)

    if random.random() < 0.04:
        notif_delay = None
    if random.random() < 0.03:
        vehicle_value = None

    data.append([
        claim_number,
        excess,
        circ,
        org,
        method,
        ncd,
        notif_delay,
        injury,
        tp_damage,
        insured_damage,
        age,
        vehicle_value,
        liability
    ])

df = pd.DataFrame(data, columns=[
    "Claim_Number","Excess","Circumstance","OrganizationNotifiedBy",
    "MethodofNotification","NCD_Indicator","Notification_Delay","Injury",
    "ThirdPartyVehicleDamage","InsuredVehicleDamage","Insured_age",
    "EstimatedVehicleValue","Liability_group"
])

df = df.sample(frac=1).reset_index(drop=True)

df.to_csv(file_path, index=False)
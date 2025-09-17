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

    circ = np.random.choice(circumstances, p=[0.18,0.13,0.12,0.12,0.07,0.06,0.09,0.06,0.09,0.08])
    org = np.random.choice(org_notified_by, p=[0.25,0.20,0.25,0.10,0.10,0.10])
    method = np.random.choice(method_notification, p=[0.55,0.30,0.15])
    ncd = np.random.choice(ncd_indicator, p=[0.45,0.55])

    if random.random() < 0.8:
        notif_delay = np.random.randint(0, 50)  
    elif random.random() < 0.15:
        notif_delay = np.random.normal(100, 10)  
    else:
        notif_delay = np.random.randint(150, 350) 
    notif_delay = max(0, int(notif_delay))

    excess = np.random.exponential(scale=700)
    if random.random() < 0.02:
        excess *= 10  
    excess = round(min(excess, 20000), 2)

    injury = np.random.choice([0, 1], p=[0.55, 0.45])
    tp_damage = np.random.choice([0, 1], p=[0.35, 0.65])
    insured_damage = np.random.choice([0, 1], p=[0.08, 0.92])

    age = int(np.random.normal(35, 12))
    if age < 18: age = 18
    if age > 75: age = 75

    vehicle_value = np.random.lognormal(mean=np.log(14000), sigma=0.6)
    if random.random() < 0.02:
        vehicle_value *= 5 
    if vehicle_value > 150000:
        vehicle_value = 150000
    vehicle_value = int(vehicle_value)

    if tp_damage == 1:
        liability = weighted_choice(liability_group, [0.55, 0.23, 0.22])
    elif injury == 1:
        liability = weighted_choice(liability_group, [0.45, 0.25, 0.30])
    else:
        liability = weighted_choice(liability_group, [0.40, 0.20, 0.40])

    if age < 25 and random.random() < 0.4:
        liability = "Fully_Liable"

    if random.random() < 0.03:
        notif_delay = None
    if random.random() < 0.02:
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
print(f"Synthetic motor insurance data generated and saved to {file_path}")
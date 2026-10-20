import os
import random
import pandas as pd
from datetime import datetime, timedelta


def create_raw_saas_ledger():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, 'SaaS_Raw_Ledger.xlsx')

    # Configuration profiles
    currencies = ['USD', 'EUR', 'KES']
    plans = ['Basic_Monthly', 'Pro_Monthly', 'Enterprise_Annual']
    statuses = ['Success', 'Failed', 'Refunded', None]  # None introduces missing data anomalies

    records = []
    start_date = datetime(2026, 1, 1)

    print("🚀 Simulating 500 global e-commerce transaction lines...")
    for i in range(1001, 1501):
        tx_id = f"TXN-{i}"
        date_val = start_date + timedelta(days=random.randint(0, 280), hours=random.randint(0, 23))
        cust_id = f"CUST-{random.randint(5000, 9999)}"
        plan = random.choice(plans)
        currency = random.choice(currencies)
        status = random.choices(statuses, weights=[85, 8, 4, 3], k=1)[0]

        # Assign values based on subscription plans
        if 'Basic' in plan:
            amount = 29.0
        elif 'Pro' in plan:
            amount = 99.0
        else:  # Enterprise Annual
            amount = 1200.0

        # Add deliberate text formatting inconsistencies for normalization testing
        if random.random() < 0.15:
            currency = currency.lower()  # e.g., 'usd' instead of 'USD'

        records.append({
            'Transaction_ID': tx_id,
            'Timestamp': date_val.strftime('%Y-%m-%d %H:%M:%S') if random.random() > 0.05 else date_val.strftime(
                '%d/%m/%Y'),
            'Customer_ID': cust_id,
            'Plan_Type': plan,
            'Raw_Amount': amount if random.random() > 0.03 else None,  # Introduce missing financial figures
            'Currency': currency,
            'Payment_Status': status
        })

    df = pd.DataFrame(records)

    # Save directly out as a workbook to act as our Data_Master template source
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data_Master', index=False)

    print(f"🎉 Raw pipeline source file successfully compiled at: {output_path}")


if __name__ == '__main__':
    create_raw_saas_ledger()

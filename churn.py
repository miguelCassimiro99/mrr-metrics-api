import pandas as pd
import csv
import io
from datetime import datetime
  
def date_converter(data_str):
    try:
        # Tenta converter usando o formato do arquivo XLSX
        return datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            # Tenta converter usando o formato do arquivo CSV
            return datetime.strptime(data_str, '%m/%d/%y %H:%M')
        except ValueError:
            # Se nenhum dos formatos for correspondido, levanta um ValueError
            raise ValueError(f"Formato de data não suportado: {data_str}")


def calculate_churn_rate(data):
  inactive_subscribers = 0
  annual_subscriptions_canceled = 0
  monthly_subscriptions_canceled = 0
  monthly_billing_canceled = 0
  annual_billing_canceled = 0

  csv_reader = csv.DictReader(data)

  for row in csv_reader:
    initial_date = date_converter(row['data início'])

    if row['status'] == 'Cancelada' and datetime.strptime(row['data cancelamento'], '%m/%d/%y %H:%M') > initial_date:
      inactive_subscribers += 1
      value = float(row['valor'].replace(',', '.'))

      if row['periodicidade'] == 'Anual':
        annual_billing_canceled += value
        annual_subscriptions_canceled += 1
      
      if row['periodicidade'] == 'Mensal':
        monthly_billing_canceled += value
        monthly_subscriptions_canceled += 1

  total_churn_rate = annual_billing_canceled + monthly_billing_canceled
  
  return {
    "inactive_subscribers": inactive_subscribers,
    "annual_subscriptions_canceled": annual_subscriptions_canceled,
    "monthly_subscriptions_canceled": monthly_subscriptions_canceled,
    "monthly_billing_canceled": round(monthly_billing_canceled, 2),
    "annual_billing_canceled": round(annual_billing_canceled, 2),
    "total_churn_rate": round(total_churn_rate, 2),
  };

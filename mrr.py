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


def calculate_simple_mrr(data):
  active_subscribers = 0
  annual_subscriptions = 0
  monthly_subscriptions = 0
  monthly_billing = 0
  annual_billing = 0

  csv_reader = csv.DictReader(data)

  for row in csv_reader:
    initial_date = date_converter(row['data início'])

    if row['status'] == 'Ativa' and (row['data cancelamento'] == '' or datetime.strptime(row['data cancelamento'], '%m/%d/%y %H:%M') > initial_date):
      active_subscribers += 1
      value = float(row['valor'].replace(',', '.'))

      if row['periodicidade'] == 'Anual':
        annual_billing += value
        annual_subscriptions += 1
      
      if row['periodicidade'] == 'Mensal':
        monthly_billing += value
        monthly_subscriptions += 1

  total_mrr = annual_billing + monthly_billing
  
  return {
    "active_subscribers": active_subscribers,
    "annual_subcriptions": annual_subscriptions,
    "monthly_subscriptions": monthly_subscriptions,
    "monthly_billing": round(monthly_billing, 2),
    "annual_billing": round(annual_billing, 2),
    "total_mrr": round(total_mrr, 2),
  };

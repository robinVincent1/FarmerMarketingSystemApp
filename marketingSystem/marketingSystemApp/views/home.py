from django.shortcuts import render
from ..models import Transaction
from django.db.models import Sum
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import matplotlib
import seaborn as sns

# Use the Agg backend for Matplotlib
matplotlib.use('Agg')

def homePage(request):
    """
    View to render the home page with various sales and revenue graphs.
    """
    # Prepare the data
    transactions = Transaction.objects.all().values('transaction_date', 'id_request__id_product__product_name', 'volume', 'total_price')
    df = pd.DataFrame(transactions)

    # Convert necessary columns to appropriate types
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month'] = df['transaction_date'].dt.month
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
    df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')

    # Sales by date graph
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='transaction_date', y='volume', hue='id_request__id_product__product_name', marker='o')
    plt.title('Product Sales by Date')
    plt.xlabel('Date')
    plt.ylabel('Sales Volume')
    plt.legend(title='Product')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    sales_per_date_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # Sales by month graph
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='month', y='volume', hue='id_request__id_product__product_name', marker='o')
    plt.title('Product Sales by Month')
    plt.xlabel('Month')
    plt.ylabel('Sales Volume')
    plt.xticks(range(1, 13))  # Set x-axis ticks from 1 to 12
    plt.legend(title='Product')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    sales_per_month_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # Quantity of products sold by month graph
    product_month_data = df.groupby(['id_request__id_product__product_name', 'month']).agg({'volume': 'sum'}).reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(data=product_month_data, x='month', y='volume', hue='id_request__id_product__product_name')
    plt.title('Quantity of Products Sold by Month')
    plt.xlabel('Month')
    plt.ylabel('Quantity Sold')
    plt.xticks(range(1, 13))  # Set x-axis ticks from 1 to 12
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    quantity_per_month_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # Revenue by month graph
    plt.figure(figsize=(10, 5))
    revenue_data = df.groupby('month').agg({'total_price': 'sum'}).reset_index()
    sns.lineplot(data=revenue_data, x='month', y='total_price', marker='o')
    plt.title('Revenue by Month')
    plt.xlabel('Month')
    plt.ylabel('Total Revenue')
    plt.xticks(range(1, 13))  # Set x-axis ticks from 1 to 12
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    revenue_per_month_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return render(request, 'home.html', {
        'sales_per_date_graph': sales_per_date_graph,
        'sales_per_month_graph': sales_per_month_graph,
        'quantity_per_month_graph': quantity_per_month_graph,
        'revenue_per_month_graph': revenue_per_month_graph,
    })

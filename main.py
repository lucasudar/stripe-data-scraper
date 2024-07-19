import os
import stripe
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your Stripe secret key here
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def fetch_customers_with_subscriptions():
    customers = []
    for customer in stripe.Customer.list(limit=100).auto_paging_iter():
        # Check if the customer has an active subscription
        subscriptions = stripe.Subscription.list(customer=customer.id, limit=1)
        if subscriptions['data']:
            subscription = subscriptions['data'][0]
            customers.append({
                'customer_id': customer.id,
                'email': customer.email,
                'name': customer.name,
                'subscription_status': subscription['status'],
                'subscription_amount': subscription['items']['data'][0]['plan']['amount'] / 100,  # Convert amount from cents to dollars
                'subscription_currency': subscription['items']['data'][0]['plan']['currency']
            })
    return customers

def fetch_customers_with_one_time_purchases():
    customers = []
    for charge in stripe.Charge.list(limit=100).auto_paging_iter():
        if charge.customer:  # Check if the charge has an associated customer
            customer = charge.customer
            customer_details = stripe.Customer.retrieve(customer)
            customers.append({
                'customer_id': customer,
                'email': customer_details.email,
                'name': customer_details.name,
                'amount': charge.amount / 100,  # Convert amount from cents to dollars
                'currency': charge.currency,
                'created': datetime.fromtimestamp(charge.created).strftime('%Y-%m-%d %H:%M:%S'),  # Convert Unix timestamp to readable date
                'description': charge.description,
                'payment_status': charge.status
            })
    return customers

def fetch_all_payments_for_customers():
    payments = []
    for customer in stripe.Customer.list(limit=100).auto_paging_iter():
        for charge in stripe.Charge.list(customer=customer.id, limit=100).auto_paging_iter():
            payments.append({
                'customer_id': customer.id,
                'email': customer.email,
                'name': customer.name,
                'amount': charge.amount / 100,  # Convert amount from cents to dollars
                'currency': charge.currency,
                'created': datetime.fromtimestamp(charge.created).strftime('%Y-%m-%d %H:%M:%S'),  # Convert Unix timestamp to readable date
                'description': charge.description,
                'payment_status': charge.status
            })
    return payments

if __name__ == '__main__':
    # Fetch customers with subscriptions
    subscription_customers = fetch_customers_with_subscriptions()
    df_subscriptions = pd.DataFrame(subscription_customers)
    df_subscriptions.to_csv('subscription_customers.csv', index=False)
    print("Subscription customers data saved to subscription_customers.csv")

    # Fetch customers with one-time purchases
    one_time_customers = fetch_customers_with_one_time_purchases()
    df_one_time = pd.DataFrame(one_time_customers)
    df_one_time.to_csv('one_time_customers.csv', index=False)
    print("One-time purchase customers data saved to one_time_customers.csv")

    # Fetch all payments for customers
    all_payments = fetch_all_payments_for_customers()
    df_payments = pd.DataFrame(all_payments)
    df_payments.to_csv('all_payments.csv', index=False)
    print("All payment data saved to all_payments.csv")
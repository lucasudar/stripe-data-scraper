# Stripe Data Scraper

This project fetches customer data from Stripe, including subscription details and one-time purchases, and saves the data to CSV files. The script also converts Unix timestamps to human-readable date formats.

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/lucasudar/stripe-data-scraper
    cd stripe-bot
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your environment variables**:
    Create a `.env` file in the root of your project and add your Discord bot token:
    ```env
    STRIPE_SECRET_KEY=stripe_token
    ```

5. **Run the bot**:
    ```bash
    ./venv/bin/python3 main.py
    ```

## How It Works

1. **Initialization**:
    - The script initializes the Stripe API using the secret key from the `.env` file.

2. **Fetching Subscriptions**:
    - The script fetches a list of customers.
    - For each customer, it checks if they have an active subscription.
    - The details of customers with active subscriptions are collected and saved to `subscription_customers.csv`.

3. **Fetching One-Time Purchases**:
    - The script fetches a list of charges.
    - For each charge, it retrieves the associated customer’s details.
    - The details of customers with one-time purchases are collected and saved to `one_time_customers.csv`.

4. **Fetching All Payments**:
    - The script fetches a list of charges and payment intents.
    - It combines this data to include all payments (both subscription and one-time) for each customer.
    - The combined payment data is saved to `all_payments.csv`.

## Notes

- Ensure that your Stripe API key is kept secure and not exposed in your source code or public repositories.
- The script uses pagination to handle large datasets, ensuring that it can process all available data from Stripe.
- The `created` field in the payment data is converted from a Unix timestamp to a human-readable date format.
- If you encounter any rate limits from the Stripe API, consider adding delays between requests or reducing the request rate.
- The data saved includes customer details, subscription statuses, one-time purchase details, and all payments history for comprehensive analysis.

### Output Files

- `subscription_customers.csv`: Contains data of customers with active subscriptions.
- `one_time_customers.csv`: Contains data of customers with one-time purchases.
- `all_payments.csv`: Contains all payment data for customers.
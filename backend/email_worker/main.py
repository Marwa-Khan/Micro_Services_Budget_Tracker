import pika
import json
import sendgrid
from sendgrid.helpers.mail import Mail

# RabbitMQ and SendGrid configuration
RABBITMQ_HOST = "192.168.0.100"  # Update this for deployment


def send_email(user_id, description, amount, category,Remail):
    """Send an email notification via SendGrid."""
    print("email aaai ???", Remail)
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    message = Mail(
        from_email="marwakhan1st@gmail.com",
        to_emails=Remail,  # Replace with dynamic recipient's email if available
        subject="Expense Alert",
        html_content=f"""
            <p>User ID: {user_id}</p>
            <p>Expense Description: {description}</p>
            <p>Amount: ${amount}</p>
            <p>Category: {category}</p>
        """,
    )
    response = sg.send(message)
    print(f"Email sent: {response.status_code}")

def callback(ch, method, properties, body):
    """Process messages from RabbitMQ."""
    expense_data = json.loads(body)
    print(f"Received message: {expense_data}")
    send_email(
        expense_data['user_id'],
        expense_data['description'],
        expense_data['amount'],
        expense_data['category'],
        expense_data['email']
    )

def start_worker():
    """Start the RabbitMQ consumer."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='expense_notifications')

    # Set up the consumer
    channel.basic_consume(queue='expense_notifications', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages...")
    channel.start_consuming()

if __name__ == "_main_":
    start_worker()
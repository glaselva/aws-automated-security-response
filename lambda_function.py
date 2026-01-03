import json
import boto3

# Configurazione SNS Topic ARN (ARN finto)
SNS_TOPIC_ARN = "arn:aws:sns:eu-south-1:123456789012:SecurityAlertsTopic"

def lambda_handler(event, context):
    # 1. Parsing dell'evento ricevuto da EventBridge
    print("Evento ricevuto:", json.dumps(event))
    
    # Estrarre dettagli chiave dal JSON di GuardDuty
    detail = event.get('detail', {})
    severity = detail.get('severity', 0)
    title = detail.get('title', 'Unknown Threat')
    description = detail.get('description', 'No description provided')
    
    # 2. Logica di Business: Solo se la minaccia è Media o Alta (> 4)
    if severity > 4:
        message = f"""
        🚨 SECURITY ALERT: {title}
        ------------------------------------------
        Severity: {severity}
        Description: {description}
        Account: {event.get('account')}
        Region: {event.get('region')}
        
        Action Taken: Notification sent to Security Team.
        """
        
        # 3. Invia notifica via SNS
        sns = boto3.client('sns')
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=f"AWS GuardDuty Alert: Severity {severity}"
        )
        print(f"Email inviata! Message ID: {response['MessageId']}")
        return {
            'statusCode': 200,
            'body': json.dumps('Alert sent successfully')
        }
    
    else:
        print(f"Minaccia rilevata ma di bassa gravità ({severity}). Nessuna email inviata.")
        return {
            'statusCode': 200,
            'body': json.dumps('Low severity, no action taken')
        }

# Intervision Support Desk Contact Center

## Overview
This Intervision Support Desk Contact Center is a sample solution designed to streamline customer support operations using AWS Cloud services, specifically leveraging Amazon Connect. The project encompasses a custom contact flow, AWS Lambda functions for backend logic, DynamoDB tables for Managing user information and managing prompts dynamically as well as Leveraging Amazon Lex, AWS Pinpoint and SES for Email communication integration and integration with other AWS services to facilitate a simple, fast and secure customer support system.

## Use Case
The solution is designed to provide technical support to Intervision employees, such as a self-service online password reset system. The caller is required to provide their employee ID, and the system authenticates them against a DynamoDB table. On successful authentication, the system sends an email with a verification code to the employee's email address. The employee confirms this verification code, and a temporary password is generated and read out to the employee to complete their password reset.

### Assumptions Made
- **User Management**: For the purpose of this demonstration, a DynamoDB table was utilized for user management to simulate the storage and retrieval of user credentials and statuses. This choice was made to showcase the ability to integrate AWS services for a seamless authentication process. However, in real-world production environments, it is common for companies to integrate a CRM platform, such as Salesforce, for comprehensive user management.

- **Email Communication**: The project exclusively uses email communication for sending verification codes and notifications as part of the password reset process. This method was chosen for its simplicity and ease of implementation within the scope of this demonstration. While SMS communication could offer a more immediate and user-friendly option for notifications, obtaining a registered number and setting up SMS services could extend the timeline of this project.

## Support Flow
![Intervision Support Flow](https://raw.githubusercontent.com/leslyndam/InterVision-Use-Case/main/Intervision%20Support%20Flow.png)


## Major Components
- **Amazon Connect Contact Flow**: A detailed setup that guides the interaction with customers, from greeting messages to authentication and routing based on customer input.

- **AWS Lambda Functions**:
  - `employee_authentication_code_hook`: Manages the employee id verfication process.
  - `get-prompts`: Manages dynamic retrieval of prompts based on customer input or context.
  - `generateTempPassword`: Manages the generation of a temporal password assigned to an employee.

- **Amazon Lex Bots**:
  - `help-desk-menu`: Voice and DTMF support bot with intents for handling the primary menu.
  - `employee-authentication-bot`: Detailed Lex bot making use of advanced features to manage employee authentication and code verification in a single session.

## Testing Instructions
To test the Intervision Support Desk Contact Center:
1. Call the test phone number [1-800-694-5605](tel:1-800-694-5605).
2. Navigate through the IVR prompts as a customer would, testing each pathway for accuracy and performance. When prompted for authentication, you can use "1234567" as a sample employee ID to test the authentication process.

## Author
The Intervision Support Desk Contact Center was developed by ***Lesly Ndam***. This project is for Intervision Systems.

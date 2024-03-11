
# Design Document: Chatly

## Overview
The Calendly Chatbot is an interactive chat interface that allows users to interact with their Calendly account directly through text commands. The chatbot provides functionalities such as listing scheduled events, creating new event and canceling events using the Calendly API. The chatbot utilizes Langchain's function calling feature to integrate with the Calendly API seamlessly.

## Getting Started 

### Running backend 

```bash
# Moving to backend directory
cd backend  

# Installing the requirements from requirements.txt
pip install -r requirements.txt 

# Activating the virtual environment 
source venv/bin/activate 

# Moving to src directory
cd src  

# Running the backend
python main.py 
```

### Running the frontend 

```bash
# Moving the frontend 
cd frontend 

# Installing the dependencies 
npm install . 

# Running the frontend  
npm run start 
```

### Running the test

```bash
# Moving to src directory
cd backend/src 

pytest
```

## Requirements
### Functional Requirements
- **List Scheduled Events:** Users can request to see their scheduled events by issuing a command like "show me the scheduled events".

- **Cancel Event:** Users can cancel a specific event by providing details such as time and date in their command, for example, "cancel my event at 3pm today".

- **Create Event:** Users can create a specific event by providing details such as time, date, meeting name, and its duration in their command, for example, "create an event on 17 feb 2025 , make it a 100 mins event and the name of the event-- discussion with Tanmesh".

### Non-Functional Requirements
- **User-Friendly Interface:** The chatbot should provide a user-friendly interface for interacting with Calendly, either through a web interface or REST API.

- **Security:** Ensure secure communication between the chatbot and Calendly API by implementing proper authentication mechanisms.


## Architecture
The architecture of the Calendly Integration Chatbot consists of the following components:

1. **Entry Point: `main.py`**
    - This serves as the entry point for the application and handles incoming requests from users.

2. **Handler Layer**
    - The handler layer is responsible for handling incoming requests, performing input validation, and creating user objects from access tokens.

3. **Services Layer**
    - The services layer contains the business logic of the application, including interacting with the Calendly API to perform actions such as listing events, canceling events, and creating events.

4. **User Management**
    - The application supports user signup and login functionalities. Each user is associated with a unique Calendly token.

5. **Data Storage**
    - For simplicity, the application initially uses in-memory storage for holding user objects. However, an extension plan includes using a durable database for storing user data.

6. **Error Handling**
    - Error handling is implemented to handle various scenarios, including incorrect request arguments and transient network errors. Retry logic with exponential backoff and jitter is used to handle transient errors.

## Code Design Principles
The codebase follows the following design principles:

1. **Modularization**
    - The codebase is organized into modular components such as handlers, services, and data storage for better maintainability and scalability.

2. **Clean Code**
    - Constants are defined appropriately, and necessary logs are added for debugging and error handling purposes.

3. **Error Handling**
    - Error handling is implemented to handle various scenarios, including incorrect request arguments and transient network errors.

4. **Followed MVCS Pattern**
    - The codebase follows the Model-View-Controller-Service (MVCS) pattern for separation of concerns and better code organization.

## Extension Plans
The following extension plans are identified for future development:

1. **Redis Cache Integration**
    - Integrate Redis cache for session management instead of in-memory cache.

2. **Durable Database Integration**
    - Integrate a durable database for storing user objects and other application data.

3. **Deployment on AWS with CI/CD**
    - Deploy the application on AWS infrastructure and implement Continuous Integration/Continuous Deployment (CI/CD) pipelines for automated deployment.

## Conclusion
The Calendly Chatbot provides a convenient and intuitive interface for users to interact with their Calendly account. By leveraging OpenAI's function calling feature and proper API integration, the chatbot seamlessly integrates with the Calendly API to provide scheduling and event management functionalities. With potential future enhancements, the chatbot can further streamline the scheduling process and provide a more personalized user experience.
# Language Learning Assistant

## Introduction
Language Learning Assistant is a Django-based web application designed to aid language learners. This app features translation, chat, and conversation editing capabilities, powered by ChatGPT and an integrated text-to-voice converter. It supports Google account login for user authentication and is fully dockerized for easy setup and deployment. The user interface is enhanced using HTMX, providing a dynamic and responsive experience.

## Features
- **Translation**: Translate text into different languages.
- **Chat Interface**: Engage in conversations with a ChatGPT-powered bot.
- **Conversation Editing**: Edit and refine conversations for learning purposes.
- **Text-to-Voice Conversion**: Convert translations to audio for auditory learning.
- **Google Account Integration**: Secure and convenient login using Google accounts.
- **Dynamic User Interface**: Enhanced with HTMX for a responsive and interactive experience.
- **Dockerized Environment**: Easy setup and deployment with Docker and Docker Compose.

## Technology Stack
- **Backend**: Django
- **Frontend**: HTMX for dynamic UI, [other frontend technologies]
- **AI and NLP**: ChatGPT
- **Text-to-Voice**: Text-to-voice conversion API
- **Authentication**: Google OAuth
- **Cache and Sessions**: Redis
- **Containerization**: Docker and Docker Compose
- **Database**: [Database used, e.g., PostgreSQL]

## Installation

### Prerequisites
- Docker and Docker Compose

### Setup
1. Clone the repository:
   ```
   git clone [repository URL]
   cd [repository name]
   ```
2. Create a `variables.env` file in the project root with the necessary environment variables:
   ```
   # Example content of variables.env
   POSTGRES_USER=youruser
   POSTGRES_PASSWORD=yourpassword
   REDIS_URL=redis://redis:6379/0
   GOOGLE_CLIENT_ID=yourgoogleclientid
   GOOGLE_CLIENT_SECRET=yourgoogleclientsecret
   ```

3. Run the application using Docker Compose:
   ```
   docker-compose up -d
   ```

## Usage
- Access the application at `http://localhost:[port]` (replace `[port]` with the port you've configured, default is usually 8000).

## Contributing
Contributions to the Language Learning Assistant are welcome! Here's how to contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b my-new-feature`.
3. Make your changes and commit: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin my-new-feature`.
5. Submit a pull request.

## License
Apache License Version 2.0

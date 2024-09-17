# Medixify - AI for Healthcare

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
- [Contributions](#contributions)
- [Tech Stack](#TechStack)

## Overview

Medixify is an advanced healthcare platform integrating hospitals, medicine distributors, and testing labs under one unified system. Utilizing AI, OCR, and blockchain, it eliminates paper-based processes by digitizing prescriptions and medical records, ensuring data security and integrity. Features include real-time inventory management, automated lab reporting, personalized patient portals, and role-based dashboards. Medixify enhances operational efficiency, patient care, and overall hospital management through cutting-edge technology.

## Features

- **Visual Representation**: The ER model diagram provides a visual representation of the hospital's database structure.
- **Comprehensive**: Includes all major entities such as Patients, Doctors, Departments, and Appointments.
- **Scalable**: Can be extended to include more entities as per the hospital's requirements.

## Usage

How to run the code:

1. Clone the repository:

   ```bash
   git clone https://github.com/aryanDevAK/minor-project.git
   ```
2. Creating Virtual Enviornment:
   Delete the pulled virtual env file and create new.
   ````bash
   cd backend
   python -m venv venv
   ```   ```
4. Activating Virtual Enviornement:
   ```bash
   env\Scripts\Activate.ps1
   ```
5. Installing required Libraries:
   ```bash
   pip install -r requirements.txt
   ```
6. Running the Server :
   Make sure you are in the folder "./minor-project/backend".
   ```bash
   python app.py
   ```
   The python server should run on the server "localhost:5000".\n
   Now keep the terminal as it is and let the server run.\n
   Open another command line for the frontend.
   
8. Running the Frontend :
   Switch the directory using
   ```bash
   cd frontend
   ```
   Make sure now you are in the folder "./minor-project/frontend".
9. Install Node js modules
   ```bash
   npm install
   ```
10. Run the server
    ```bash
    npm run dev
    ```
    The node server must run on the "localhost:5173".

## Contributinons

## TechStack
   1.Backend:
   ```
Framework: Python Flask
Database: SQLite (for development), PostgreSQL (for production)
ORM: SQLAlchemy
Authentication: Flask-Login, OAuth
API: RESTful API using Flask-RESTful
```
   2.Frontend:
   ```
Framework: React
State Management: Redux
Styling: CSS Modules, Sass
UI Components: Material-UI or Ant Design
Routing: React Router
```
   3.AI and NLP:
   ```
OCR: Tesseract OCR
NLP: spaCy, NLTK
Machine Learning: Scikit-learn, TensorFlow, PyTorch
```
   4.Blockchain:
   ```
Platform: Ethereum
Smart Contracts: Solidity
Integration: Web3.js or ethers.js
```
   5.DevOps:
   ```
Containerization: Docker
CI/CD: GitHub Actions, Jenkins
Deployment: AWS (EC2, RDS, S3), Heroku
```
   6.Security:
   ```
Encryption: TLS/SSL, bcrypt for password hashing
Vulnerability Scanning: OWASP ZAP, Snyk
```
   7.Additional Tools:
   ```
Version Control: Git
Project Management: Jira
```

# Medixify - AI for Healthcare

## Overview

This repository contains the Entity-Relationship (ER) model diagram for the Hospital Management System. The diagram provides a comprehensive view of the relationships between different entities within the hospital system, including patients, doctors, departments, and appointments.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

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
   The python server should run on the server "localhost:5000"
   Now keep the terminal as it is and let the server run.
   Open another command line for the frontend
   
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
    The node server must run on the "localhost:5173"

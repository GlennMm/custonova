## Custonova

### Intro

- This project consist of two type of applications a django application and an angular application. 
- This implies that the backend project and the frontend must be running for you to be able to use your system.

This repository contains the code for a customer churn project using KMeans clustering and logosticregreasion to predict the probability of a customer to stay loyal to the shop or not . 

### The project uses the following technologies:

- Python - The programming language used to develop the project.
- Sklearn - A machine learning library used to train the AI model.
- Django - A web framework used to create the REST API.
- Angular - A web framework used to create the frontend UI.

The project is divided into the following three parts:

- Model training - This part of the project uses Sklearn and TensorFlow to train the AI model. The model is trained on a dataset of fraudulent and non-fraudulent transactions.
- REST API - This part of the project uses Django to create a REST API that exposes the AI model. The REST API can be used to get predictions from the AI model.
- Frontend UI - This part of the project uses Angular to create a frontend UI that consumes the REST API. The frontend UI allows users to input transaction data and get predictions from the AI model.

#### Backend

- Activate anaconda environment
- Run the following commands sequentially.

`
    cd custonova &&
    pip install -r requirements.txt &&
    python manage.py makemigrations &&
    python manage.py migrate &&
    python manage.py createsuperuser && 
    python manage.py runserver
`

#### Frontend

- run the following commands sequentially.

`bash
    npm i -g @angular/cli or yarn global add @angular/cli
    cd front
    npm install or yarn
    ng serve -o --hmr
`
- enjoy 


# **Simple Weather API**

## **Overview**

This project is a Django-based application utilizing Django Rest Framework (DRF) to create a basic weather API that interacts with a SQL database to store and retrieve weather data. The API allows users to add new weather data and retrieve weather data for a specific city.

## **Prerequisites**

- `Python 3.11.3`
- `Django 5.0.7`
- `Django Rest Framework (DRF) 3.15.2`
- `SQLite or any other preferred database`


## **Installation**
Clone the Repository


git clone https://github.com/GbolahanAlaba/sokosq-technical-assessment

cd sokosq-technical-assessment


## **Create Virtual Environment**

It's recommended to use a virtual environment to manage dependencies:


`python -m venv venv`

## **Activate Virtual Environment**

MAC `source venv/bin/activate`

Windows `venv\Scripts\activate`

## **Install Dependencies**

Install the required dependencies using pip:

`pip install -r requirements.txt`


## **Run Migrations**

Apply the migrations to set up your database schema:

`python manage.py makemigrations`

`python manage.py migrate`


## **Run the Development Server**
Start the development server to verify everything is set up correctly:

`python manage.py runserver`
You should now be able to access the application at http://127.0.0.1:8000/.

## **API Endpoints**

- `POST /weather`: Add new weather data.
- `GET /weather/{city}`: Retrieve weather data for a specific city.

## **API Implementation**

#### POST /weather

- **Request Body**:

  ```json
  {
      "city": "CityName",
      "date": "YYYY-MM-DD",
      "temperature": 23.5,
      "description": "Clear sky"
  }

- **Response**:

`201 Created` on success.

`400 Bad Request` on validation error.


#### GET /weather/{city}

- **Response**:

  ```json
  {
      "city": "CityName",
      "date": "YYYY-MM-DD",
      "temperature": 23.5,
      "description": "Clear sky"
  }


- `200 OK` with weather data on success.

- `404 Not Found` if no data is available for the city.

## **Testing**
Run a tests to ensure the API endpoints work as expected.

`py manage.py test`
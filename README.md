# Resupply Forecast App

A Python-based web application for forecasting product resupply needs using Facebook Prophet.

## Features

- Excel data processing for sales and forecast data
- Time series forecasting using Facebook Prophet
- RESTful API for accessing forecast data
- Interactive frontend for visualizing forecasts

## Project Structure

```
Resupply-forecast-app/
├── backend/               # FastAPI backend
│   ├── app/               # Application code
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── db/            # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── main.py        # FastAPI application
│   └── requirements.txt   # Backend dependencies
├── data/                  # Data directory
│   └── cleaned_data.csv   # Processed data
├── frontend/              # Frontend code
│   └── src/               # Source code
├── data_loader.py         # Excel data processing script
├── prophet_forecast.py    # Prophet forecasting script
└── README.md              # Project documentation
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/safwanesalihi/Resupply-forecast-app.git
   cd Resupply-forecast-app
   ```

2. Install backend dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

4. Process the Excel data:
   ```
   python data_loader.py
   ```

5. Generate the initial forecast:
   ```
   python prophet_forecast.py
   ```

## Running the Application

1. Start the backend server:
   ```
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

3. Access the application at `http://localhost:5173`

## API Endpoints

- `GET /api/v1/forecasts/prophet/forecast`: Get the Prophet forecast data

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, Prophet
- **Frontend**: React, Recharts, Shadcn UI
- **Data Processing**: Pandas, Openpyxl
- **Forecasting**: Facebook Prophet

## License

This project is licensed under the MIT License.


# dashboard

dashboard is a Streamlit application that serves as the visual interface for fitness-app. It queries data-sync for workout history and statistics, queries ai-service to generate workout plans, and provides a manual sync trigger. Access to the entire application is gated behind a shared password.

<br>

# Project Structure
- `app.py`: The application entry point. Renders the landing page and the sidebar's manual sync trigger.
- `pages/1_Overview.py`: Displays session counts and duration statistics across all sports, filterable by time range.
- `pages/2_Climbing.py`: Displays climbing-specific statistics, including grade progression over time, filterable by gym.
- `pages/3_Strength.py`: Displays strength session statistics.
- `pages/4_Running.py`: Displays running session statistics.
- `pages/5_Yoga.py`: Displays yoga session statistics.
- `pages/6_Diving.py`: Displays diving session statistics.
- `pages/7_Generate_Plan.py`: Provides a form to request either a full weekly plan or a single ad-hoc session from ai-service, and renders the result.
- `utils/api_client.py`: Contains the shared functions used by every page to call data-sync and ai-service.
- `utils/auth.py`: Contains `require_auth`, the shared password gate called at the top of `app.py` and every page. Every page must call this individually, since Streamlit's sidebar navigation runs the selected page script directly rather than re-running `app.py` first.

<br>

# Environment Variables
The following variables must be defined in a `.env` file in this directory:
- `DATA_SYNC_URL`: The base URL of the data-sync service.
- `AI_SERVICE_URL`: The base URL of the ai-service.
- `DASHBOARD_PASSWORD`: The shared password required to access the dashboard. This must also be set as an environment variable on the deployed Railway service, using a production value rather than the local development value.

<br>

# Virtual Environment
Creating the virtual environment:
- Change directory into the dashboard folder: `cd dashboard`
- Create a virtual environment: `python3 -m venv venv`

Activating the virtual environment:
- Activate the virtual environment:
    - `source venv/bin/activate` (macOS/Linux)
    - `venv\Scripts\activate` (Windows)
- Install dependencies (only required the first time, or after `requirements.txt` changes): `pip install -r requirements.txt`

<br>

# Local Development
- Ensure data-sync and ai-service are already running locally, since every page queries them on load. See [../data-sync/README.md](../data-sync/README.md) and [../ai-service/README.md](../ai-service/README.md).
- Activate the virtual environment under the dashboard directory: `source venv/bin/activate`.
- Start the application: `streamlit run app.py`.
- On first load, enter the value configured in `DASHBOARD_PASSWORD` to access the dashboard.

<br>

# Known Issues
- On `pages/7_Generate_Plan.py`, the exercise breakdown table for weekly plan sessions never renders, because `session.get("exercises")` is always empty for weekly plans. This is caused by a schema issue in ai-service, not in this service; see the Known Issues section of [../ai-service/README.md](../ai-service/README.md) for the underlying cause.

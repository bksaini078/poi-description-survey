# POI Survey Application

A web-based survey instrument for evaluating the effectiveness of AI-personalized Point of Interest (POI) descriptions compared to original human-written descriptions. This application was developed as part of a collaborative research study between **Fraunhofer IAO, Stuttgart** and **KU Leuven, Belgium**, investigating whether LLM-generated, user-profile-adapted tourism descriptions can match or exceed the quality of manually authored content in terms of trust, clarity, engagement, and visit motivation.

## Research Context

The study employs a within-subjects experimental design where participants evaluate 10 POIs across 5 tourism categories (Accommodation, Natural Attractions, Entertainment, Cultural & Historical Sites, and Commercial & Shopping). For each POI, the system generates a personalized description using Azure OpenAI GPT-4o, subtly tailored to the participant's demographic profile and travel preferences. Participants then perform a blinded A/B comparison - the presentation order of original vs. AI-generated descriptions is randomized - and rate each version on multiple assessment dimensions.

## Survey Flow

1. **Consent** - Informed consent with study purpose and data handling information.
2. **User Profiling** - Collection of demographics (age, gender, nationality, profession, etc.) and travel preferences (interests, hobbies, travel style, experience level).
3. **POI Comparison** (×10) - Side-by-side blinded comparison of original and AI-generated title + description for each POI, with per-version ratings (significance, trust, clarity).
4. **Final Survey** - Overall experience rating, perception of automated adaptation, comfort with AI-generated content, and open-ended feedback.

## Technical Stack

| Component             | Technology                                               |
| --------------------- | -------------------------------------------------------- |
| Frontend / UI         | Streamlit 1.40+                                          |
| AI Content Generation | Azure OpenAI (GPT-4o, `2024-08-06`)                      |
| Data Models           | Pydantic v2                                              |
| Data Storage          | CSV (survey responses), JSON (POI data, temp AI content) |
| Language              | Python ≥ 3.11                                            |
| Package Manager       | uv (or pip)                                              |

## Project Structure

```
PoI_survey/
├── app.py                              # Application entry point; manages survey page flow
├── pyproject.toml                      # Project metadata and core dependencies
├── requirements.txt                    # Pinned dependency versions for reproducibility
├── .python-version                     # Python version specification (3.13)
│
├── app/                                # Main application package
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── survey_model.py             # Pydantic data models (POIResponse, UserData,
│   │                                   #   SurveyResponse, FinalSurveyResponse, POIData,
│   │                                   #   POICategory)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── survey_routes.py            # UI route handlers: consent page, user details form,
│   │                                   #   POI comparison display, assessment forms,
│   │                                   #   navigation logic, response validation, thank-you page
│   ├── services/
│   │   ├── __init__.py
│   │   └── survey_service.py           # Business logic services:
│   │                                   #   - POIService: loads and flattens POI data from JSON
│   │                                   #   - AIService: Azure OpenAI client init, prompt
│   │                                   #     construction, personalized content generation
│   │                                   #   - SurveyResponseService: saves per-POI and final
│   │                                   #     responses to timestamped CSV files
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                  # Utility functions: page config, custom CSS injection,
│                                       #   session state initialization, image-to-base64
│                                       #   conversion, imprint link
│
├── config/
│   └── constants.py                    # Application constants: form options (nationalities,
│                                       #   professions, hobbies, travel styles, interests),
│                                       #   rating scales (Likert, trust, clarity), custom CSS
│
├── data/
│   └── pois.json                       # POI dataset: 10 POIs across 5 categories, each with
│                                       #   id, coordinates, title, description, image path,
│                                       #   and source URL
│
├── assets/
│   ├── images/                         # POI images in JPEG, PNG, and WebP formats
│   │   ├── Cafe-Central.*
│   │   ├── Hassler_Roma.*
│   │   ├── Mercedes.*
│   │   ├── Volksfest.*
│   │   ├── Wilhelma.*
│   │   ├── colone_carnival.*
│   │   ├── colosseo.*
│   │   ├── jungfrau.*
│   │   ├── louvre.*
│   │   ├── neuschwanstein.*
│   │   ├── savoylondon.*
│   │   └── via_del_corso.*
│   └── scroll.html                     # JavaScript snippet for auto-scrolling to page top
│
├── logo/
│   ├── fraunhofer_logo.png             # Fraunhofer IAO logo displayed in the app header
│   ├── fraunhofer_logo.svg
│   ├── icon.ico                        # Browser tab favicon
│   └── icon.svg
│
├── utils/
│   ├── __init__.py
│   └── scroll_utils.py                 # Streamlit component wrapper for scroll-to-top JS
│
├── survey_results/                     # [Auto-created] Stores timestamped CSV response files
├── temp_data/                          # [Auto-created] Stores per-user AI-generated content JSON
│
├── .streamlit/
│   └── secrets.toml                    # Streamlit secrets (Azure OpenAI credentials)
│
└── .gitignore                          # Git ignore rules
```

## File Descriptions

### Core Application

| File               | Description                                                                                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app.py`           | Entry point. Initializes Streamlit page config, injects custom CSS, manages session state, and orchestrates the multi-page survey flow (consent → user details → POI comparisons → final survey). |
| `pyproject.toml`   | Project metadata (name, version, Python version requirement) and core dependency specifications.                                                                                                  |
| `requirements.txt` | Pinned versions of all Python dependencies for exact reproducibility.                                                                                                                             |

### `app/models/survey_model.py`

Defines Pydantic v2 data models used across the application:

- **`POIResponse`** - Structured output format for Azure OpenAI (title + description).
- **`UserData`** - Participant demographic and preference profile.
- **`SurveyResponse`** - Per-POI comparison response with all rating fields.
- **`FinalSurveyResponse`** - End-of-survey feedback and optional lottery email.
- **`POIData`** / **`POICategory`** - Schema for the POI dataset.

### `app/routes/survey_routes.py`

Implements all Streamlit UI pages:

- **`show_consent_page()`** - Renders informed consent text and captures agreement.
- **`show_user_details_form()`** - Multi-column form collecting demographics, accessibility needs, profession, hobbies, travel interests/style/experience. Enforces minimum-selection validation.
- **`show_poi_comparison()`** - Displays two randomized versions (A/B) side-by-side with images, titles, and descriptions. Renders per-version assessment scales and comparative preference questions.
- **`show_thank_you()`** - Final survey page with overall experience, adaptation perception, AI comfort ratings, and optional lottery email entry.

### `app/services/survey_service.py`

Contains business logic organized into three service classes:

- **`POIService`** - Loads `data/pois.json`, flattens category-grouped POIs into a single list.
- **`AIService`** - Initializes Azure OpenAI client via Streamlit secrets, constructs system + user prompts incorporating visitor profile for emphasis guidance, enforces character-length constraints matching original descriptions, uses GPT-4o structured output parsing.
- **`SurveyResponseService`** - Persists per-POI and final survey responses to timestamped CSV files in `survey_results/`.

### `app/utils/helpers.py`

Utility functions: Streamlit page configuration, custom CSS injection from `config/constants.py`, session state initialization (page tracking, user data, AI content cache, UUID-based user ID), image-to-base64 encoding for inline display, and Fraunhofer imprint link rendering.

### `config/constants.py`

Centralizes all form options (nationalities, professions, hobbies, travel styles, travel interests, experience levels, gender, marital status), rating scales (5-point Likert, trust, clarity), and the application's custom CSS theme (color `#189c7d`, button styles, progress bar, typography, content boxes).

### `data/pois.json`

Dataset of 10 Points of Interest across 5 categories:

| Category                    | POIs                                    |
| --------------------------- | --------------------------------------- |
| Accommodation               | Hotel Hassler Roma, The Savoy (London)  |
| Natural Attractions         | Jungfraujoch, Neuschwanstein Castle     |
| Entertainment               | Cologne Carnival, Cannstatter Volksfest |
| Cultural & Historical Sites | Colosseum, Louvre Museum                |
| Commercial & Shopping       | Via del Corso, Café Central (Vienna)    |

Each POI entry contains: `id`, geographic `position`, `title`, `description` (sourced from official/review sites), `imagesrc`, and `source` URL.

## Setup and Installation

### Prerequisites

- **Python 3.13+** (as specified in `.python-version`)
- **Azure OpenAI API access** with a deployed `gpt-4o-2024-08-06` model
- [**uv**](https://docs.astral.sh/uv/) (recommended) or **pip** as the package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/bksaini078/PoI_survey.git
cd PoI_survey
```

### Step 2: Create a Virtual Environment and Install Dependencies

**Using uv (recommended):**

```bash
uv venv
source .venv/bin/activate    # macOS / Linux
# .venv\Scripts\activate     # Windows
uv sync
```

**Using pip:**

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
# .venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Step 3: Configure Azure OpenAI Credentials

Create a `.streamlit/secrets.toml` file with your Azure OpenAI credentials:

```toml
[secrets]
AZURE_OPENAI_API_VERSION = "2024-08-01-preview"
AZURE_OPENAI_API_KEY = "<your-azure-openai-api-key>"
AZURE_OPENAI_ENDPOINT = "<your-azure-openai-endpoint>"
```

> **Note:** The deployed model name must be `gpt-4o-2024-08-06`. If your deployment uses a different name, update the `model` parameter in `app/services/survey_service.py` (line 128).

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will launch in your default browser at `http://localhost:8501`.

## Output Data

Survey responses are automatically saved to the `survey_results/` directory:

| File Pattern                       | Content                                                                                                                                                   |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `survey_responses_<timestamp>.csv` | Per-POI comparison ratings and preferences for all 10 POIs, including user demographics, presentation order (`is_manual_first`), and response timestamps. |
| `final_responses_<timestamp>.csv`  | Final survey feedback: overall experience rating, adaptation perception, AI comfort level, open-ended comments, and optional lottery email.               |

Temporary AI-generated content is cached per user session in `temp_data/temp_poi_content_<user_id>.json`.

## Data Security and Ethics

- **Anonymity**: Participants are identified solely by auto-generated UUIDs; no personally identifying information is stored in survey response files.
- **Informed Consent**: Participation requires explicit consent on the first page.
- **Credential Security**: API keys are stored in `.streamlit/secrets.toml`, which is excluded from version control via `.gitignore`.
- **Local Storage**: All response data is stored locally on the server running the application.

## Citation

If you use this tool or dataset in your research, please cite:

```
@misc{poi_survey_2026,
  title={POI Survey: A Tool for Evaluating AI-Personalized Point of Interest Descriptions},
  author={Fraunhofer IAO and KU Leuven},
  year={2026},
  url={https://github.com/bksaini078/PoI_survey}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

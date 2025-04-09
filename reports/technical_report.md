# Technical Report: LinkedIn Profile Scraper (Mock)

## Approach
This project simulates a LinkedIn scraping tool using synthetic data generation to demonstrate lead generation capabilities while avoiding actual web scraping. The system:

1. **Generates Mock Profiles**: Creates realistic but fake LinkedIn profiles using randomized data patterns
2. **Implements Search Filters**: Allows filtering by job title, company, location, and industry
3. **Scores Leads**: Uses a rule-based scoring system to prioritize high-value prospects
4. **Exports Data**: Provides multiple export formats for CRM integration

## Model Selection
**Data Generation Model**:
- Built using Python's random data generation techniques
- No machine learning model used (as this is a mock demonstration)
- Future production version would use:
  - LinkedIn API (official)
  - Or trained NER model for profile analysis

**Scoring Algorithm**:
```python
def calculate_score(profile):
    score = 0
    # Title-based scoring
    if any(word in profile['title'].lower() 
           for word in ['ceo','cto','vp','director']):
        score += 25
    # Company-based scoring
    if any(keyword in profile['company'].lower() 
           for keyword in ['tech','software','ai']):
        score += 15
    return min(100, score)  # Cap at 100%
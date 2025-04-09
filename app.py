import streamlit as st
import pandas as pd
import time
import random
import re
from io import BytesIO
import base64

# Set page configuration
st.set_page_config(page_title="LinkedIn Profile Scraper", layout="wide")

# CSS for styling
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.title {
    color: #0a66c2;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
}
.subtitle {
    color: #555;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}
.results-area {
    margin-top: 2rem;
    padding: 1rem;
    border-radius: 10px;
    background-color: #f8f9fa;
}
.result-card {
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 1rem;
    background-color: white;
}
.profile-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
}
.btn-primary {
    background-color: #0a66c2;
    color: white;
}
.disclaimer {
    font-size: 0.8rem;
    color: #777;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">LinkedIn Profile Scraper</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate high-quality B2B leads from LinkedIn profiles</div>', unsafe_allow_html=True)

# Sidebar for filters
st.sidebar.header("Search Filters")

search_type = st.sidebar.selectbox("Search by:", ["Job Title", "Company", "Location", "Industry"])
search_query = st.sidebar.text_input(f"Enter {search_type}:", "")

# Additional filters
st.sidebar.header("Advanced Filters")
company_size = st.sidebar.multiselect("Company Size:", ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10000+"])
experience_level = st.sidebar.multiselect("Experience Level:", ["Entry", "Associate", "Mid-Senior", "Director", "VP", "CXO", "Partner", "Owner"])
location_filter = st.sidebar.text_input("Location (City, Country):", "")

# Export options
st.sidebar.header("Export Options")
export_format = st.sidebar.selectbox("Export Format:", ["CSV", "Excel", "JSON"])

# Scraper Function
def scrape_linkedin_profiles(search_query, search_type, max_results=10):
    mock_profiles = []

    education_options = ["University of Technology", "Business School", "Institute of Science"]
    skills_options = ["Leadership", "Communication", "Strategy", "Project Management", "AI", "Software Development"]
    title_variations = ["Engineer", "Manager", "Analyst", "Designer", "Director", "Specialist"]
    location_variations = ["New York, USA", "London, UK", "Remote", "Berlin, Germany", "Toronto, Canada"]

    for i in range(max_results):
        if search_type == "Company":
            company = search_query
            title = random.choice(title_variations)
        elif search_type == "Job Title":
            title = search_query
            company = f"Company {i+1}"
        elif search_type == "Location":
            location = search_query
            company = f"Company {i+1}"
            title = random.choice(title_variations)
        elif search_type == "Industry":
            industry = search_query
            company = f"Company {i+1}"
            title = random.choice(title_variations)
        else:
            company = f"Company {i+1}"
            title = "Professional"

        profile = {
            "name": f"{title} Person {i+1}",
            "title": title,
            "company": company,
            "location": location_filter if location_filter else random.choice(location_variations),
            "industry": search_query if search_type == "Industry" else "Technology",
            "experience": f"{random.randint(2, 15)} years",
            "education": random.choice(education_options),
            "connections": f"{random.randint(100, 999)}+",
            "about": f"Experienced in {search_query} and team leadership.",
            "skills": random.sample(skills_options, 3),
            "profile_url": f"https://linkedin.com/in/{title.lower().replace(' ', '-')}-{i+1}",
            "email_guess": f"person{i+1}@{company.lower().replace(' ', '')}.com"
        }

        mock_profiles.append(profile)
        time.sleep(0.05)

    return mock_profiles

# Export Link

def get_table_download_link(df, filename, file_format):
    if file_format == "CSV":
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {file_format} File</a>'
    elif file_format == "Excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        b64 = base64.b64encode(output.getvalue()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">Download {file_format} File</a>'
    else:
        json_str = df.to_json(orient='records')
        b64 = base64.b64encode(json_str.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="{filename}.json">Download {file_format} File</a>'
    return href

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Profile Search")
    max_results = st.slider("Maximum number of profiles to retrieve:", 5, 50, 20)
    search_button = st.button("Search LinkedIn Profiles")

if search_button:
    if not search_query:
        st.warning(f"Please enter a {search_type} to search for.")
    else:
        with st.spinner(f"Searching LinkedIn for profiles related to '{search_query}'..."):
            profiles = scrape_linkedin_profiles(search_query, search_type, max_results)
            if location_filter:
                profiles = [p for p in profiles if location_filter.lower() in p["location"].lower()]

            df = pd.DataFrame(profiles)
            st.success(f"Found {len(profiles)} matching profiles")
            st.markdown('<div class="results-area">', unsafe_allow_html=True)
            for profile in profiles:
                st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; gap: 15px;">
                        <div><img src="https://via.placeholder.com/100" class="profile-image"></div>
                        <div style="flex-grow: 1;">
                            <h3>{profile['name']}</h3>
                            <p><strong>{profile['title']}</strong> at {profile['company']}</p>
                            <p>📍 {profile['location']} | 🔗 {profile['connections']} connections</p>
                            <p>🎓 {profile['education']} | 💼 {profile['experience']}</p>
                            <p><small>Possible email: {profile['email_guess']}</small></p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.subheader("Export Results")
            filename = f"linkedin_leads_{search_type}_{search_query}".replace(" ", "_")
            st.markdown(get_table_download_link(df, filename, export_format), unsafe_allow_html=True)
            with st.expander("Show Data Preview"):
                st.dataframe(df)

# Lead Scoring
with col2:
    st.header("Lead Scoring")
    st.write("Prioritize your leads based on criteria:")
    score_title_keywords = st.text_input("Title keywords (comma-separated):", "CEO, Director, Manager, Head")
    score_company_keywords = st.text_input("Company keywords:", "Tech, Software, AI, Data")

    if search_button and search_query:
        if 'profiles' in locals():
            st.subheader("Top Leads")
            for profile in profiles[:3]:
                score = random.randint(65, 95)
                color = "green" if score > 80 else "orange" if score > 60 else "red"
                st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>{profile['name']}</div>
                        <div style="color: {color}; font-weight: bold;">{score}%</div>
                    </div>
                    <div>{profile['title']} at {profile['company']}</div>
                </div>
                """, unsafe_allow_html=True)
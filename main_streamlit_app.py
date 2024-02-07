import streamlit as st
import os
from supabase_client import insert_job_details,store_job_details
from rapidapi_extraction import extract_linkedin_profile_details
from google_api_search import search_linkedin_profiles


def analyze_job_description(token,job_description,profile,years_of_experience,skills,location):
    if job_description is not None:
        url = "https://api.replicate.ai/v1/model/llama-2/generate"
        headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
        }
        prompt = f"This is the {job_description} for the {profile} the employer is looking for the ideal candidate 
        kindly get the required search parameter from the job description . ideal candidate should have 
         from 0 - {years_of_experience} and this {skills} are mandatory and near to this {location} or 
         ready to relocate to this {location} "
        # Make API call to Llama LLM model
        data = {
            "prompt": job_description,
            "length": 50,
            "prompt_key": "key_parameter",
            "prompt": prompt
        }
        search_parameter = requests.post(url, headers=headers, data=json.dumps(data))
        print("Replicate API is intiated...")
        if search_parameter is not None:
            return search_parameter
        else:
            return None
    else:
        print("Job Description is not entered properly")
    

# Streamlit Application
def main():
    search_parameters = None
    try:
        st.title("Job Specification Input")
        # User input for job specifications
        profile = st.text_input("Profile:")
        years_of_experience = st.slider("Years of Experience", min_value=0, max_value=15, value=5)
        skills = st.text_area("Skills (Enter multiple skills separated by commas):")
        location = st.text_input("Location:")
        job_description  = st.text_input("Enter the Job Description for Ideal Candidate")
        token = os.environ["replicate_token"]
        if token is not None:
            if st.button("Submit"):
                search_parameters = analyze_job_description(token,job_description,
                                                            profile, years_of_experience, skills, location)
                #     # Store job details in Superbase
                job_id = insert_job_details(job_description,profile, experience, skills, location)

                if search_parameters is not None and job_id is not None:
                    linkedin_profiles = search_linkedin_profiles(search_parameters, location)
                
                    #     # Extract detailed profile information using RapidAPI
                    for profile_url in linkedin_profiles:
                        profile_info = extract_linkedin_profile_details(profile_url)
                        # Store profile data in Supabase linked to the respective job entry
                        store_job_details(profile_info, job_id)
                        
                else:
                    print("job_id is not created")

        else:
            print("Token is not fetch from Replicate API")

    except Exception as e:
        print(traceback.format_exc())



if __name__ == "__main__":
    main()

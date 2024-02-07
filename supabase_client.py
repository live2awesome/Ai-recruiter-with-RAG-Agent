import os
from supabase import create_client, Client
import uuid
import dotenv

dotenv.load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_job_details(job_description,profile, experience, skills, location):
    table_name = 'job_details'
    job_id = generate_unique_job_id()
    print(f"Generated job ID: {job_id}")
    data = {'job_id':job_id,'name': name, 'experience': experience, 'skills': skills, 'location': location}
    try:
        result = sb.table(table_name).insert(data).execute()
        st.success('Job details inserted successfully in supabase')
        return job_id
    except PostgrestError as e:
        st.error(f'Error inserting job details: {e}')

def store_job_details(profile_info, job_id):
    table_name = 'job_details'
    data = {
        'job_id': job_id,
        'profile_info': profile_info
    }
    result, error = supabase_client.table(table_name).insert(data).execute()

    if error:
        print(f"Error storing Linkedin Profiles: {error}")
    else:
        print(f"Linkedin Profiles stored successfully: {result}")

def generate_unique_job_id():
  return str(uuid.uuid4())


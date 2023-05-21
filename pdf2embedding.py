import os
import dotenv
import openai
from supabase import create_client
import pdfplumber
from typing import List

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_ANON_KEY
)

# Path to the directory containing your PDF files
dirPath = 'FULL-PATH-TO-PDF-FILE-DIR-HERE'

try:
    files: List[str] = os.listdir(dirPath)
except OSError as e:
    print(f'Error reading directory: {str(e)}')
    exit(1)

for file in files:
    if file.endswith('.pdf'):  # Ensure we're reading only PDF files
        filePath = os.path.join(dirPath, file)
        try:
            with pdfplumber.open(filePath) as pdf:
                body = ""
                for page in pdf.pages:
                    body += page.extract_text()
        except Exception as e:
            print(f'Error reading file {filePath}: {str(e)}')
            continue

        # Create an embedding using OpenAI
        try:
            response = openai.Embedding.create(
                input=body,
                model="text-embedding-ada-002"
            )
            embeddings = response['data'][0]['embedding']
        except Exception as e:
            print(f'Error creating embeddings: {str(e)}')
            continue

        # Store the text and embedding in Supabase
        try:
            response = supabase.table('supabase-table-name-here').insert({
                'title': 'column-title-here',
                'body': 'column-body-title-here',
                'content': body,
                'embedding': embeddings
            }).execute()
        except Exception as e:
            print(f'Error inserting to Supabase: {str(e)}')
            continue

        if hasattr(response, 'error') and response.error:
            print(f'Error inserting to Supabase: {response.error.message}')
        else:
            print(f'Inserted: {response.data}')

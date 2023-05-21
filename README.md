# BLoC
Takes txt files/pdf files, converts them to embeddings with openai and upserts them to Supabase. Code could likely be changed to alternative databases with minimal edits.

# update .env file with your information

OPENAI_API_KEY=YOUR OPENAI-API-KEY-HERE
SUPABASE_URL=YOUR-SUPABASE-HOST-URL-HERE
SUPABASE_ANON_KEY=YOUR-SUPABASE-ANON-KEY-HERE

# install dependencies:

pip install -r requirements.txt

# run program:

python pdf2embedding.py
python text2embed.py

# Check supabase for updated data to confirm working.

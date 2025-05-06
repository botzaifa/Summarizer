# import re
# import nltk
# from nltk.corpus import stopwords
# import string

# # Download NLTK data on first run
# nltk.download("stopwords")

# def clean_text(text: str) -> str:
#     """
#     Cleans and normalizes input text for better summarization.
#     """
#     # Lowercase
#     text = text.lower()

#     # Remove URLs
#     text = re.sub(r'http\S+|www.\S+', '', text)

#     # Remove HTML tags
#     text = re.sub(r'<.*?>', '', text)

#     # Remove punctuation
#     text = text.translate(str.maketrans('', '', string.punctuation))

#     # Remove extra whitespace
#     text = re.sub(r'\s+', ' ', text).strip()

#     # Remove stopwords (optional)
#     stop_words = set(stopwords.words('english'))
#     text = ' '.join([word for word in text.split() if word not in stop_words])

#     return text

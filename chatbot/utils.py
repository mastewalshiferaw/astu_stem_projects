import fuzzywuzzy.process as fuzzy # You might need: pip install fuzzywuzzy python-Levenshtein
from .models import FAQ

def get_astu_ai_response(user_query):
    faqs = FAQ.objects.all()
    if not faqs.exists():
        return "I'm still learning about ASTU. Please submit a ticket for manual help."

    # Logic: Find the most similar question in our database
    questions = [q.question for q in faqs]
    # Simple similarity matching 
    best_match, score = fuzzy.extractOne(user_query, questions)

    if score > 70:
        faq_item = FAQ.objects.get(question=best_match)
        return f"I found a solution: {faq_item.answer}"
    
    return "I'm not 100% sure about that. Would you like me to help you create a formal support ticket?"
import fuzzywuzzy.process as fuzzy
from .models import FAQ

def get_astu_ai_response(user_query):
    # 1. Check if we have any data
    faqs = FAQ.objects.all()
    if not faqs.exists():
        return "I'm still learning about ASTU. (Hint: Visit Admin Analytics to seed data)"

    # 2. Get all questions from the DB
    questions = [q.question for q in faqs]
    
    # 3. Match user query against DB questions
    # fuzzy.extractOne returns (string, score)
    match_result = fuzzy.extractOne(user_query, questions)
    
    if match_result:
        best_match, score = match_result
        if score > 60: # Lowered threshold slightly for better matching
            faq_item = FAQ.objects.get(question=best_match)
            return f"Found a solution: {faq_item.answer}"
    
    return "I'm not sure about that. Try asking about 'WiFi' or 'Internet'."
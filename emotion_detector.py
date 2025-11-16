# emotion_detector.py
from transformers import pipeline

# Using the zero-shot model to determine the user's core intent.
intent_classifier = pipeline(
    "zero-shot-classification", 
    model="facebook/bart-large-mnli"
)

def get_user_intent(text):
    """
    Analyzes the user's text to determine the most likely viewing intent.
    
    Args:
        text (str): The user's input text.
        
    Returns:
        tuple: A tuple containing the best-matching descriptive phrase (str) 
               and the model's confidence score (float).
    """
    if not text or not text.strip():
        return "general", 0.0
    
    # These phrases describe movie plots and themes, not just emotions.
    candidate_intents = [
        'a romantic love story',
        'a lighthearted and funny comedy',
        'an exciting action-packed adventure',
        'a serious and emotional drama',
        'a scary and suspenseful thriller',
        'a futuristic science fiction story'
    ]
    
    try:
        result = intent_classifier(text, candidate_intents)
        
        top_intent = result['labels'][0]
        top_score = result['scores'][0]
            
        return top_intent, top_score
        
    except Exception as e:
        print(f"Error during intent detection: {e}")
        return "general", 0.0
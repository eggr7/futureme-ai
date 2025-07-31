import json
import os
from typing import Dict, Any

def load_majors_data() -> Dict[str, Any]:
    """Load majors data from JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "majors.json")
    
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_response(user_message: str) -> str:
    """
    Generate a response based on user message.
    This is a placeholder implementation that can be enhanced with AI later.
    """
    message_lower = user_message.lower()
    majors_data = load_majors_data()
    
    # Simple keyword-based responses
    if any(word in message_lower for word in ["code", "programming", "computer", "tech", "software"]):
        return "Based on your interest in technology, you might enjoy Computer Science! It involves problem-solving through code and building innovative solutions."
    
    elif any(word in message_lower for word in ["people", "help", "psychology", "mind", "behavior"]):
        return "It sounds like you're interested in understanding people! Psychology could be a great fit - it's the study of behavior and the mind."
    
    elif any(word in message_lower for word in ["business", "leadership", "money", "management", "entrepreneur"]):
        return "Your interest in leadership suggests Business might be perfect for you! It focuses on decision-making and organizational leadership."
    
    elif any(word in message_lower for word in ["art", "creative", "design", "draw", "paint"]):
        return "Your creative interests point toward Fine Arts! It's all about expressing creativity and developing artistic skills."
    
    elif any(word in message_lower for word in ["science", "research", "experiment", "biology", "chemistry"]):
        return "You seem drawn to scientific inquiry! Consider Biology or Chemistry - both involve research and understanding the natural world."
    
    else:
        # Default response with general guidance
        available_majors = list(majors_data.keys()) if majors_data else ["Computer Science", "Psychology", "Business"]
        majors_list = ", ".join(available_majors[:3])
        return f"That's interesting! Based on what you've shared, you might want to explore majors like {majors_list}. Tell me more about your specific interests - do you enjoy working with people, solving technical problems, or being creative?"
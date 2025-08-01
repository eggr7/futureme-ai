import json
import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LLMConfig:
    """Configuration for LLM integration"""
    use_llm: bool = False
    api_key: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7
    timeout: int = 30

def load_llm_config() -> LLMConfig:
    """Load LLM configuration from environment variables"""
    return LLMConfig(
        use_llm=os.getenv("USE_LLM", "false").lower() == "true",
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "500")),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
        timeout=int(os.getenv("LLM_TIMEOUT", "30"))
    )

def generate_llm_response(message: str) -> str:
    """
    Generate response using OpenAI's LLM API
    
    Args:
        message: User's input message
        
    Returns:
        LLM-generated response string
        
    Raises:
        Exception: For API errors, timeouts, or configuration issues
    """
    config = load_llm_config()
    
    if not config.api_key:
        raise ValueError("OpenAI API key not configured")
    
    try:
        import openai
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=config.api_key)
        
        # Create system prompt for career guidance
        system_prompt = """You are FutureMe AI, a helpful career guidance counselor for high school students. 
        Your role is to help students discover college majors that align with their interests, skills, and career goals.
        
        Guidelines:
        - Ask thoughtful questions about their interests, hobbies, and strengths
        - Provide specific major recommendations with clear explanations
        - Include information about career paths, required skills, and what to expect
        - Be encouraging and supportive
        - Keep responses concise but informative (under 200 words)
        - Focus on practical advice and actionable next steps
        
        Remember: You're helping shape their future, so be thoughtful and inspiring!"""
        
        # Make API call with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=config.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    timeout=config.timeout
                )
                
                return response.choices[0].message.content.strip()
                
            except openai.RateLimitError as e:
                logger.warning(f"Rate limit hit (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise Exception("Rate limit exceeded. Please try again later.")
                    
            except openai.APITimeoutError as e:
                logger.warning(f"API timeout (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    raise Exception("Request timed out. Please try again.")
                    
            except openai.AuthenticationError as e:
                logger.error(f"Authentication error: {e}")
                raise Exception("Invalid API key. Please check your configuration.")
                
            except openai.APIError as e:
                logger.error(f"OpenAI API error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    raise Exception("AI service temporarily unavailable. Please try again.")
                    
    except ImportError:
        logger.error("OpenAI library not installed")
        raise Exception("LLM integration not available. Please install required dependencies.")
        
    except Exception as e:
        logger.error(f"Unexpected error in LLM generation: {e}")
        raise Exception("Unable to generate AI response. Please try again.")

def load_majors_data() -> Dict[str, Any]:
    """Load majors data from JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "majors.json")
    
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Majors data file not found")
        return {}
    except json.JSONDecodeError:
        logger.error("Invalid JSON in majors data file")
        return {}

def get_static_response(user_message: str) -> str:
    """
    Generate a static response based on keyword matching.
    This is the fallback when LLM is not available.
    """
    message_lower = user_message.lower()
    majors_data = load_majors_data()
    
    # Enhanced keyword-based responses
    if any(word in message_lower for word in ["code", "programming", "computer", "tech", "software", "app", "website"]):
        return """Based on your interest in technology, **Computer Science** could be perfect for you! 🖥️

**What you'll learn:** Programming, algorithms, software development, and problem-solving through code.

**Career paths:** Software Engineer, Web Developer, Data Scientist, AI Engineer, Cybersecurity Analyst

**Skills you'll develop:** Programming languages (Python, Java, C++), logical thinking, system design, and mathematical reasoning.

Would you like to know more about specific areas within tech, or are you curious about other majors too?"""
    
    elif any(word in message_lower for word in ["people", "help", "psychology", "mind", "behavior", "counseling", "therapy"]):
        return """It sounds like you're interested in understanding people! **Psychology** could be a great fit! 🧠

**What you'll study:** Human behavior, mental processes, research methods, and therapeutic techniques.

**Career paths:** Clinical Psychologist, Counselor, Research Psychologist, HR Specialist, Social Worker

**Skills you'll develop:** Empathy, active listening, research methods, statistical analysis, and communication.

Are you more interested in helping people directly through therapy, or would you prefer research and understanding behavior patterns?"""
    
    elif any(word in message_lower for word in ["business", "leadership", "money", "management", "entrepreneur", "startup", "marketing"]):
        return """Your interest in leadership suggests **Business Administration** might be perfect for you! 💼

**What you'll learn:** Management principles, financial analysis, marketing strategies, and entrepreneurship.

**Career paths:** Business Manager, Entrepreneur, Marketing Director, Financial Analyst, Consultant

**Skills you'll develop:** Leadership, strategic thinking, financial analysis, communication, and decision-making.

Are you more drawn to starting your own business, or would you prefer working in established companies?"""
    
    elif any(word in message_lower for word in ["art", "creative", "design", "draw", "paint", "visual", "artistic"]):
        return """Your creative interests point toward **Fine Arts**! 🎨

**What you'll explore:** Various artistic mediums, art history, color theory, and creative expression techniques.

**Career paths:** Graphic Designer, Art Teacher, Museum Curator, Freelance Artist, Art Director

**Skills you'll develop:** Creativity, visual design, artistic techniques, portfolio development, and self-expression.

What type of art interests you most - traditional (painting, drawing) or digital (graphic design, digital art)?"""
    
    elif any(word in message_lower for word in ["science", "research", "experiment", "biology", "chemistry", "lab", "medical"]):
        return """You seem drawn to scientific inquiry! **Biology** or **Chemistry** might be excellent choices! 🔬

**Biology focuses on:** Living organisms, genetics, ecology, and life processes.
**Chemistry focuses on:** Chemical reactions, molecular structures, and material properties.

**Career paths:** Research Scientist, Medical Doctor, Environmental Scientist, Biotechnologist, Laboratory Technician

**Skills you'll develop:** Scientific method, laboratory techniques, data analysis, and critical thinking.

Are you more interested in living systems (biology) or chemical processes (chemistry)?"""
    
    elif any(word in message_lower for word in ["math", "mathematics", "numbers", "statistics", "data", "analysis"]):
        return """Your interest in mathematics opens many doors! **Mathematics** or **Data Science** could be perfect! 📊

**What you'll study:** Advanced mathematics, statistics, data analysis, and mathematical modeling.

**Career paths:** Data Analyst, Statistician, Actuary, Research Scientist, Financial Analyst

**Skills you'll develop:** Logical reasoning, problem-solving, statistical analysis, and mathematical modeling.

Do you prefer pure mathematics and theory, or applying math to solve real-world problems?"""
    
    else:
        # Enhanced default response with more guidance
        available_majors = list(majors_data.keys()) if majors_data else [
            "Computer Science", "Psychology", "Business Administration", "Biology", "Fine Arts"
        ]
        majors_list = ", ".join(available_majors[:4])
        
        return f"""That's interesting! To help you find the perfect major, I'd love to learn more about you! 🎓

**Some popular majors to consider:** {majors_list}

**Tell me more about:**
• What subjects do you enjoy most in school?
• What activities make you lose track of time?
• Do you prefer working with people, data, or creative projects?
• What kind of impact do you want to make in the world?

The more you share, the better I can guide you toward majors that align with your interests and strengths!"""

def get_response(user_message: str) -> str:
    """
    Generate a response based on user message.
    Uses LLM if configured and available, otherwise falls back to static responses.
    """
    config = load_llm_config()
    
    # Try LLM first if enabled and configured
    if config.use_llm and config.api_key:
        try:
            logger.info("Attempting to generate LLM response")
            return generate_llm_response(user_message)
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            logger.info("Falling back to static response")
            # Fall through to static response
    
    # Use static response as fallback
    logger.info("Using static response generation")
    return get_static_response(user_message)
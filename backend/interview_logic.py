import openai
import os

# Set up OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_question(role, difficulty, topic, tone):
    """Generate an interview question based on the given parameters."""
    prompt = f"""
    You are an expert interviewer conducting a {tone.lower()} interview for a {role} position.
    Generate a {difficulty.lower()} level question about {topic}.
    
    The question should:
    - Be specific to the {role} role
    - Test {difficulty.lower()} level knowledge of {topic}
    - Be asked in a {tone.lower()} tone
    - Be clear and concise
    - Allow for a detailed technical response
    
    Return only the question, no additional text.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating question: {str(e)}"

def evaluate_answer(question, answer, role, difficulty, topic, tone):
    """Evaluate the candidate's answer and provide feedback."""
    prompt = f"""
    You are an expert interviewer evaluating a candidate's answer for a {role} position.
    
    Question: {question}
    Candidate's Answer: {answer}
    
    Please provide constructive feedback that:
    - Acknowledges what the candidate got right
    - Points out areas for improvement
    - Suggests specific technical details they could have mentioned
    - Maintains a {tone.lower()} tone
    - Is specific to the {role} role and {topic} domain
    - Considers this is a {difficulty.lower()} level question
    
    Keep the feedback concise but helpful (2-3 sentences).
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert technical interviewer providing constructive feedback."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error evaluating answer: {str(e)}"

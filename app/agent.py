import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("WARNING: Missing GEMINI_API_KEY or GOOGLE_API_KEY.")

class AgentWrapper:
    """
    Handles communication with the Gemini API and generates insights.
    """
    def __init__(self):
        self.chat_history = []      
        self.model_name = "gemini-2.5-flash"
        self.api_key = API_KEY

    # ------------------------ BUILD PAYLOAD -------------------------
    def _build_messages_payload(self, new_question: str):

        length_prompt = (
            "Give a clear, structured answer between 100 and 200 words. "
            "Make it meaningful, easy to read, and practically useful. "
            "Use short paragraphs or bullet points when helpful."
        )

        payload_contents = self.chat_history + [
            {"role": "user", "parts": [{"text": length_prompt + "\n\nQuestion: " + new_question}]}
        ]

        return {
            "contents": payload_contents,
            "generationConfig": { 
                "temperature": 0.5,
                "topK": 30,
            }
        }

    # ------------------------ CHATBOT RESPONSE -------------------------
    def ask(self, question: str) -> str:

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
            f"?key={self.api_key}"
        )
        
        payload = self._build_messages_payload(question)
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            answer = data['candidates'][0]['content']['parts'][0]['text']

        except Exception as e:
            return f"Error: {e}"

        # ✅ Store chat history
        self.chat_history.append({"role": "user", "parts": [{"text": question}]})
        self.chat_history.append({"role": "model", "parts": [{"text": answer}]})

        return answer

    # ------------------------ PARENT INSIGHTS -------------------------
    def generate_parent_insights(
        self,
        major: str,
        academic_strength: str,
        interest_area: str,
        investment: float,
        placement: float
    ) -> str:

        prompt = f"""
You are a Career Advisor helping parents understand the expected outcomes of a student's education.

Write a structured, professional, friendly insight between **150 to 300 words**.

Student Profile:
• Major: {major}
• Academic Strength: {academic_strength}
• Interest Area: {interest_area}
• Total Course Investment: ₹{investment}
• Placement Percentage: {placement}%

Include the following sections clearly:

1) **Career Role Opportunities**  
   Simple explanation of suitable roles.

2) **Job Market Demand (Next 5 Years, India)**  
   Realistic trends.

3) **Expected Starting Salary (INR LPA)**  
   Provide an approximate range.

4) **Internship & Placement Pathways**  
   Steps that improve chances of getting placed.

5) **Recommended Skills / Certifications**  
   Practical and job-focused.

6) **How Parents Can Support**  
   Clear, actionable suggestions.

7) **Return on Investment (ROI)**  
   • Formula: ROI = (Starting Salary × 12) / Investment × 100  
   • Breakeven time (months/years)  
   • Financial justification of the course  
   • Impact of {placement}% placement rate  

8) **Final Encouraging Summary**  
   Positive, motivating, and practical.

Write the answer in a warm, supportive tone but based on realistic Indian job market conditions.
"""

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
            f"?key={self.api_key}"
        )

        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": { "temperature": 0.5, "topK": 30 }
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            insight = data['candidates'][0]['content']['parts'][0]['text']

            return insight

        except Exception as e:
            return f"Error generating parent insights: {e}"

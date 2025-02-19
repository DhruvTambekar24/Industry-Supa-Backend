from typing import Dict, List
import google.generativeai as genai
from datetime import datetime
from app.config import settings

class IndustryMentorAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.mentors = {
            "software_engineering": {
                "name": "Dr. Dilip Borikar",
                "role": "Senior Software Engineer at Tech Giants",
                "expertise": ["System Design", "Algorithm Optimization", "Team Leadership"]
            },
            "data_science": {
                "name": "Dr. Preeti Voditel",
                "role": "Lead Data Scientist at AI Innovations",
                "expertise": ["Machine Learning", "Statistical Analysis", "Big Data"]
            },
            "product_management": {
                "name": "Hitesh Gehani",
                "role": "Product Director at StartupHub",
                "expertise": ["Product Strategy", "User Research", "Agile Management"]
            }
        }
        
    def _create_mentor_context(self, mentor_type: str) -> str:
        mentor = self.mentors[mentor_type]
        return f"""
        You are {mentor['name']}, {mentor['role']}. 
        Your expertise includes {', '.join(mentor['expertise'])}.
        Respond as if you are having a real conversation with a mentee.
        Keep responses practical, specific, and based on industry experience.
        Include specific examples and scenarios when relevant.
        """

    def get_mentor_response(self, mentor_type: str, user_query: str) -> Dict:
        context = self._create_mentor_context(mentor_type)
        prompt = f"{context}\n\nMentee: {user_query}"
        
        try:
            response = self.model.generate_content(prompt)
            
            # Process the response to extract actionable items
            follow_up_prompt = f"""
            Based on the previous response, please provide:
            1. 2-3 specific action items
            2. A relevant industry scenario
            3. A networking suggestion
            Format as JSON with keys: action_items, scenario, networking_tip
            """
            
            enrichment = self.model.generate_content(
                f"{prompt}\nMentor Response: {response.text}\n{follow_up_prompt}"
            )
            
            return {
                "mentor_name": self.mentors[mentor_type]["name"],
                "primary_response": response.text,
                "enrichment": enrichment.text
            }
        except Exception as e:
            return {"error": str(e)}

    def generate_scenario(self, mentor_type: str, difficulty: str) -> Dict:
        scenario_prompt = f"""
        As {self.mentors[mentor_type]['name']}, create a real-world {difficulty} 
        problem-solving scenario in your field. Include:
        1. Situation description
        2. Key challenges
        3. Success criteria
        4. Common pitfalls
        Format as JSON with these keys.
        """
        
        try:
            response = self.model.generate_content(scenario_prompt)
            return {"scenario": response.text}
        except Exception as e:
            return {"error": str(e)}

    def provide_feedback(self, mentor_type: str, scenario: str, solution: str) -> Dict:
        feedback_prompt = f"""
        As {self.mentors[mentor_type]['name']}, provide detailed feedback on this solution:
        Scenario: {scenario}
        Solution: {solution}
        
        Include:
        1. Strengths
        2. Areas for improvement
        3. Industry best practices
        4. Growth suggestions
        Format as JSON with these keys.
        """
        
        try:
            response = self.model.generate_content(feedback_prompt)
            return {"feedback": response.text}
        except Exception as e:
            return {"error": str(e)}

class MentorshipSession:
    def __init__(self, mentor_ai: IndustryMentorAI):
        self.mentor_ai = mentor_ai
        self.session_history = []
        
    def start_session(self, user_id: str, mentor_type: str):
        self.session_history.append({
            "timestamp": datetime.now(),
            "type": "session_start",
            "mentor": mentor_type
        })
        
    def add_interaction(self, query: str, response: Dict):
        self.session_history.append({
            "timestamp": datetime.now(),
            "type": "interaction",
            "query": query,
            "response": response
        })
        
    def get_session_summary(self) -> Dict:
        return {
            "total_interactions": len(self.session_history),
            "session_duration": (self.session_history[-1]["timestamp"] - 
                               self.session_history[0]["timestamp"]).total_seconds(),
            "key_topics": self._extract_key_topics()
        }
        
    def _extract_key_topics(self) -> List[str]:
        # Implementation to extract main topics from session
        pass
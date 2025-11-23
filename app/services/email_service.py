from typing import Optional
from app.core.llm_factory import get_llm_config
from pyagentspec import Agent
from wayflowcore.agentspec import AgentSpecLoader


class EmailService:
    """
    Service for generating and sending emails using LLM.
    """

    def __init__(self):
        self.llm_config = get_llm_config()

        # Create AgentSpec agent for email generation
        self.spec_agent = Agent(
            name="email_generator",
            system_prompt="You are a helpful professional assistant writing academic emails.",
            llm_config=self.llm_config
        )

        # Load with Wayflow
        self.agent = AgentSpecLoader().load_component(self.spec_agent)

    def generate_email(
        self, 
        email_type: str,
        professor_name: str,
        professor_context: str,
        cv_text: str,
        cv_concepts: list[str],
        student_name: Optional[str] = None,
        recipient_name: Optional[str] = None
    ) -> str:
        """
        Generate an email draft based on type and context.
        """
        recipient = recipient_name or professor_name
        
        # Prepare context string from CV
        concepts_str = ", ".join(cv_concepts)
        
        if email_type == "colab":
            signature = f"\n{student_name}" if student_name else "\nA prospective collaborator"
            prompt = f"""
Write a warm, personalized email from a motivated student to Professor {professor_name} asking about research collaboration opportunities.

STUDENT'S BACKGROUND (from their CV):
- Research interests and skills: {concepts_str}
- Brief experience: {cv_text[:500] if cv_text else "Early-career researcher"}

PROFESSOR'S WORK:
{professor_context}

INSTRUCTIONS:
- Start with a warm, genuine greeting (e.g., "Dear Professor {professor_name}")
- Express specific enthusiasm about their work based on the context provided
- Connect your background/interests to their research in a natural way
- Ask if they have any research opportunities or would be open to collaboration
- Keep it concise (3-4 short paragraphs)
- Use a friendly but professional tone - you're a motivated student, not overly formal
- DO NOT use placeholders like [Topic], [Your Name], or brackets
- End with a warm closing like "Best regards" or "Warm regards"
- Sign off with EXACTLY this signature: "{signature}"

Write the complete email now:
            """
        else: # reach_out
            signature = f"\n{student_name}" if student_name else "\nA curious student"
            prompt = f"""
Write a warm, friendly email from a curious student to Professor {professor_name} expressing interest in their work.

PROFESSOR'S WORK:
{professor_context}

STUDENT'S INTERESTS:
{concepts_str}

INSTRUCTIONS:
- Start with a warm greeting (e.g., "Dear Professor {professor_name}")
- Mention something specific from their work that caught your attention
- Ask thoughtful questions or request learning resources related to their research
- Show genuine curiosity and enthusiasm
- Keep it brief (2-3 short paragraphs)
- Tone should be friendly, curious, and respectful - like reaching out to learn from an expert
- DO NOT use placeholders like [Topic], [Your Name], or brackets
- End with a friendly closing
- Sign off with EXACTLY this signature: "{signature}"

Write the complete email now:
            """

        try:
            # Start conversation
            conv = self.agent.start_conversation()
            conv.append_user_message(prompt)

            # Execute
            conv.execute()

            # Get response
            messages = conv.get_messages()
            if not messages:
                raise ValueError("No response from agent")

            # Get last message
            last_message = messages[-1]
            return last_message.content.strip()

        except Exception as e:
            print(f"Error generating email: {e}")
            raise e

    def send_email(self, email_content: str, recipient_email: str) -> bool:
        """
        Send an email (Mock implementation).
        
        Args:
            email_content: The body of the email.
            recipient_email: The recipient's email address.
            
        Returns:
            True if sent successfully (mocked).
        """
        # TODO: Implement real email sending logic
        print(f"Sending email to {recipient_email}...")
        print(f"Content: {email_content[:50]}...")
        return True

# Global instance
email_service = EmailService()

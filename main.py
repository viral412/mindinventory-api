from message_intent_identifier import MessageIntentAnalyzer
from interest_link_analyzer import InterestLinkAnalyzer
from url_based_project_recommender import URLBasedProjectRecommender
from mail_generator import MailGenerator
from config import uri, username, password

class MindInventoryAutoMail:
    def __init__(self):
        """
        Initialize the components required for automated email generation.
        """
        # Initialize the message intent analyzer
        self.intent_analyzer = MessageIntentAnalyzer()
        # Initialize the interest link analyzer
        self.interest_link_analyzer = InterestLinkAnalyzer()
        # Initialize the URL-based project recommender with Neo4j credentials
        self.project_recommender = URLBasedProjectRecommender(uri, username, password)
        # Initialize the mail generator
        self.mail_generator = MailGenerator()

    def process_data(self, user_name: str, user_urls: list, user_message: str) -> str:
        """
        Process the user data to generate a customized email.

        Args:
            user_name (str): Name of the user (client or job seeker).
            user_urls (list): List of URLs provided by the user for analysis.
            user_message (str): The user's message indicating interest or requirements.

        Returns:
            str: The generated email content based on the identified intent and user interests.
        """

        # Identify the intent of the user's message (e.g., job seeker or client)
        intent, score = self.intent_analyzer.identify_message_intent(user_message)
        print(f"Identified Intent: {intent} (Score: {score})")

        # Analyze the user's message to find the most relevant URL based on interest
        interest_url = self.interest_link_analyzer.find_intrested_url(user_message, user_urls)
        print(f"Identified Interested URL: {interest_url}")

        # Retrieve projects related to the identified interest URL
        projects = self.project_recommender.get_projects_with_same_url_section(interest_url)
        print(f"Retrieved Projects: {projects}")

        # Get the top project suggestions based on the user's message
        top_suggestions = self.project_recommender.get_top_suggestions(user_message, projects)
        print(f"Top Project Suggestions: {top_suggestions}")

        # Generate the email content based on the identified intent and user input
        generated_mail = self.mail_generator.process_generate_mail(
            user_name, user_message, top_suggestions, interest_url, intent
        )

        print("Generated Email Content:\n", generated_mail)
        return generated_mail

if __name__ == "__main__":
    # Example input data for testing
    user_name = "Jane Smith"
    user_urls = [
        "https://www.mindinventory.com/golang-development.php",
        "https://www.mindinventory.com/hire-ai-developers.php"
    ]
    user_message = "I am looking to develop a website."


    # Initialize the MindInventoryAutoMail class
    mail_system = MindInventoryAutoMail()

    # Process the data and generate an email
    email_content = mail_system.process_data(user_name, user_urls, user_message)
    print("\nFinal Email Content:\n", email_content)
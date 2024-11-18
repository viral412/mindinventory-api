from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOllama
from langchain.chains import LLMChain

class MailGenerator():
    def __init__(self):

        """
        Initialize the ChatOllama model for generating emails.
        """

        # Initialize ChatOllama model
        self.ollama_model = ChatOllama(model_name="llama3", temprature=1.0) 

    # def mail_for_job_seeker(self, name, user_msg, url):

    #     """
    #     Generate an email response for a job seeker based on scraped job listings.

    #     Args:
    #         name (str): Name of the job seeker.
    #         user_msg (str): User's job requirements message.
    #         url (str): URL from which job listings need to be scraped.

    #     Returns:
    #         str: Generated email content for the job seeker.
    #     """

    #     # Scraping prompt template to extract job listings from a URL

    #     scrape_link_template = """
    #     You need to extract job opening listings from the given URL.
    #     URL: {url}
    #     Return the job titles and descriptions as a list.
    #     """

    #     # Prepare the scraper prompt
    #     scrapper_prompt = PromptTemplate(
    #                         input_variables=["url"],
    #                         template=scrape_link_template
    #                     )
    #     chain = LLMChain(llm=self.ollama_model, prompt=scrapper_prompt)
    #     list_of_job_opening = chain.run(url)

    #     print("Scraped Job Openings:", list_of_job_opening)

    #     # Generate Email Based on Job Matching
    #     job_seeker_email_template = """
    #     Generate an email response for a job seeker named {name} based on their message and job openings scraped from the URL.

    #     User Name: {name}
    #     User Message: {user_msg}
    #     Scraped Job Listings: {job_listings}

    #     If there are matches between the user's request and the job openings, mention them in the email.
    #     If no match is found, kindly inform the user about the current openings and suggest applying for any relevant ones.
    #     """
        
    #     # Create email generation prompt template
    #     job_seeker_prompt = PromptTemplate(
    #                         input_variables=["name", "user_msg", "job_listings"],
    #                         template=job_seeker_email_template
    #                     )

    #     # Initialize LLMChain for generating email content
    #     email_chain = LLMChain(llm=self.ollama_model, prompt=job_seeker_prompt)

    #     # Generate email content using the scraped job listings and user input
    #     email_content = email_chain.run({
    #         "name": name,
    #         "user_msg": user_msg,
    #         "job_listings": list_of_job_opening
    #     })

    #     return email_content

    def mail_for_job_seeker(self, name: str, user_msg: str, url: str) -> str:
        """
        Generate an email response for a job seeker based on their message and the given URL.

        Args:
            name (str): Name of the job seeker.
            user_msg (str): User's job requirements message.
            url (str): URL with job listings.

        Returns:
            str: Generated email content for the job seeker.
        """

        # Email template without scraping
        job_seeker_email_template = """
        Dear {name},

        Thank you for reaching out to us regarding your job search.

        We have noted your preferences: 
        "{user_msg}"

        You can explore current job openings using the following link:
        {url}

        Please review the listings, and if you find any roles that match your skills and preferences, feel free to apply directly or get back to us for further assistance.

        Best regards,
        MindInventory Team
        """

        # Format the email with the provided data
        email_content = job_seeker_email_template.format(name=name, user_msg=user_msg, url=url)

        return email_content


    def mail_for_client(self, name: str, usr_msg: str, similar_projects: list) -> str:

        """
        Generate a professional email for a client based on their interest and similar projects.

        Args:
            name (str): Name of the client.
            usr_msg (str): User message describing the client's interest.
            similar_projects (list): List of similar projects that align with the client's interest.

        Returns:
            str: Generated email content for the client.
        """

        prompt_template = """

        Write a concise and professional email to a client.

        Name: {name}
        User Message: {usr_msg}
        Similar Projects: {similar_projects}

        Acknowledge the client's interest and briefly highlight similar projects we've worked on. Offer services to meet their potential needs.
        Ensure the email is polite and encourages the client to get in touch.
        Company name: MindInventory.
        Best Regards: MindInventory Team
        
        """

        # Create prompt template for client email generation
        client_prompt = PromptTemplate(
            input_variables=["name", "usr_msg", "similar_projects"],
            template=prompt_template
        )

        # Initialize LLMChain for generating email content
        chain = LLMChain(llm=self.ollama_model, prompt=client_prompt)

        # Generate and return email content
        email = chain.run({
            "name": name,
            "usr_msg": usr_msg,
            "similar_projects": similar_projects
        })
        return email

    def process_generate_mail(self, name: str, user_msg: str, similar_projects: list, url: str, intent: str) -> str:

        """
        Process the generation of an email based on the user's intent (job seeker or client).

        Args:
            name (str): Name of the user (job seeker or client).
            user_msg (str): Message describing user's requirements or interests.
            similar_projects (list): List of similar projects (used for client emails).
            url (str): URL to scrape job listings (used for job seeker emails).
            intent (str): Intent of the email generation ("Job seeker Message" or "Client Message").

        Returns:
            str: Generated email content based on the intent.
        """

        # Determine email generation based on intent
        if intent == "Job Seeker Message":
            email_content = self.mail_for_job_seeker(name, user_msg, url)
            return email_content
        else:
            email_content = self.mail_for_client(name, user_msg, similar_projects)
            return email_content

if __name__ == "__main__":
    mail = MailGenerator()

    name, user_msg, similar_projects, url, intent = "Rohan", "i want to develope a web site in go lang.", ['Secure Payment Gateway for an Online Banking Application: Transaction processing time was reduced by 40%. PCI-DSS compliance was achieved, ensuring data protection and user trust. The transaction success rate improved by 20% during peak times.', 'Scalable Real-time Messaging Application for a Social Media Platform: The system handled over 5 million concurrent users without latency issues. Optimized use of server resources reduced infrastructure costs by 30%. With faster message delivery and lower response times, user engagement increased by 25%.', 'High-performance Microservices Architecture for an E-commerce Platform: The system was able to scale easily to handle 10x more traffic during peak sales, reduced API response times by 50%, and improved fault tolerance, cutting system downtime by 40%.'], "https://www.mindinventory.com/hire-ai-developers.php",  "Client Message"
    email_content = mail.process_generate_mail(name, user_msg, similar_projects, url, intent)
    print(email_content)

    pass
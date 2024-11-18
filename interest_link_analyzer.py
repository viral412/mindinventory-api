import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup

class InterestLinkAnalyzer():

    def __init__(self):
        """
        Initializes the InterestLinkAnalyzer class.
        This class helps identify the most relevant URL based on user message interest.
        """
        pass

    def extract_content_from_url(self, url: str) -> str:

        """
        Extracts the title and description content from a given URL using web scraping.

        Parameters:
        url (str): The URL to extract content from.

        Returns:
        str: Extracted text content including title and meta description. 
             Returns an empty string if content extraction fails.
        """
        
        try:

            # Fetch the webpage content
            response = requests.get(url)

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            title = soup.title.string if soup.title else ''

            # Extract meta description
            description = soup.find('meta', attrs={"name": "description"})
            description = description['content'] if description else ''

            # Combine title and description
            text = title + " " + description
            return text

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {url}. Error: {str(e)}")
            return ""
        
        except Exception as e:
            print(f"An error occurred while extracting content from URL: {str(e)}")
            return ""

    def preprocess_text(self, text: str) -> str:

        """
        Preprocesses the given text by converting it to lowercase, 
        removing short words and non-alphabetical characters.

        Parameters:
        text (str): The input text to preprocess.

        Returns:
        str: The cleaned and preprocessed text.
        """

        # Convert text to lowercase
        text = text.lower()
        text = re.sub(r'\b\w{1,2}\b', '', text)  # Remove short words
        text = re.sub(r'[^a-z\s]', '', text)  # Remove non-alphabetical characters
        return text

    def find_intrested_url(self, user_message: str, urls: list) -> str:

        """
        Identifies the most relevant URL based on the user's message.

        Parameters:
        user_message (str): The input message from the user.
        urls (List[str]): A list of URLs to check relevance against.

        Returns:
        str: The URL that matches the user's interest the most.
        """

        if not user_message or not urls:
            raise ValueError("User message and URLs must be non-empty.")

        # Extract content from URLs
        url_contents = [self.extract_content_from_url(url) for url in urls]

        # Preprocess user message and URL contents
        user_message_processed = self.preprocess_text(user_message)
        url_contents_processed = [self.preprocess_text(content) for content in url_contents]

        # Combine user message and URL contents for vectorization
        corpus = [user_message_processed] + url_contents_processed

        # Check if corpus is valid after preprocessing
        if not any(corpus):
            print("No valid text data to process.")
            return ""

        # Vectorize the text using TF-IDF
        vectorizer = TfidfVectorizer()

        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)

            # Calculate cosine similarity
            similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

            # Identify the URL with the highest similarity score
            interest_index = similarity_scores.argmax()
            interest_url = urls[interest_index]

            return interest_url
        
        except Exception as e:
            print(f"An error occurred during similarity calculation: {str(e)}")
            return ""

if __name__ == "__main__":


    # User message
    user_message = "I want to learn about cloud computing and its services."


    # URLs user visited
    urls = [
        "https://aws.amazon.com/what-is-cloud-computing/",
        "https://www.azure.microsoft.com/en-us/overview/what-is-cloud-computing/",
        "https://www.mindinventory.com/hire-android-developers.php"
    ]

    interest_url = InterestLinkAnalyzer().find_intrested_url(user_message, urls)
    print(interest_url)
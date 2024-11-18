from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class URLBasedProjectRecommender():
    def __init__(self,  uri, username, passcode):

        """
        Initialize the class with Neo4j database connection and the sentence transformer model.
        
        :param uri: str: Neo4j database URI
        :param username: str: Database username
        :param passcode: str: Database password
        """

        self.driver = GraphDatabase.driver(uri, auth=(username, passcode))
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def __del__(self):
        """ Destructor to ensure the Neo4j driver is closed properly. """
        if self.driver:
            self.driver.close()

    def get_user_message_embedding(self, user_message: str) -> np.ndarray:

        """
        Generate embedding for the user message using the sentence transformer model.
        
        :param user_message: str: The user input message
        :return: np.ndarray: Embedding vector for the user message
        """

        user_msg_embedding = self.model.encode(user_message)
        return user_msg_embedding

    def get_projects_with_same_url_section(self, url: list) -> str:

        """
        Fetch project details from Neo4j with the same URL section.
        
        :param url: str: The URL section to match in Neo4j
        :return: list[dict]: List of project details
        """

        projects = []
        with self.driver.session() as session:
            # Cypher query to find all projects with the same url_section and retrieve embeddings
            cypher_query = """
            MATCH (p:Project)
            WHERE p.url_section = $url
            RETURN p.url_section AS url_section,
                p.title AS title,
                p.client AS client,
                p.challenge AS challenge,
                p.solution AS solution,
                p.results AS results,
                p.tech_stack AS tech_stack,
                p.embedding AS embedding
            """
            # Execute the query and fetch results
            result = session.run(cypher_query, url=url)
            
            # Collect the results in a structured format (list of dictionaries)
            projects = [
                {
                    "url_section": record["url_section"],
                    "title": record["title"],
                    "client": record["client"],
                    "challenge": record["challenge"],
                    "solution": record["solution"],
                    "results": record["results"],
                    "tech_stack": record["tech_stack"],
                    "embedding": record["embedding"]  # Include embeddings
                }
                for record in result
            ]
            
        return projects

    def get_top_suggestions(self, user_message: str, projects: list, suggestion_num: int = 3) -> list:

        """
        Get top N project recommendations based on cosine similarity with user message.
        
        :param user_message: str: The user input message
        :param projects: list[dict]: List of projects with embeddings
        :param suggestion_num: int: Number of top suggestions to return
        :return: list[dict]: Top N recommended projects
        """

        # Step 1: Get the embedding of the user message
        user_message_embedding = self.get_user_message_embedding(user_message)
        
        # Step 3: Compute cosine similarity between the user message and each project
        similarities = []
        for project in projects:
            # Calculate cosine similarity between the user message and project embedding
            similarity = cosine_similarity([user_message_embedding], [project['embedding']])[0][0]
            similarities.append((project, similarity))
        
        # Step 4: Sort the projects based on similarity in descending order and get top 3
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 3 projects
        top_3_projects = [project for project, _ in similarities[:suggestion_num]]

        top_3 = [i["title"]+": "+ i["results"] for i in top_3_projects]

        
        return top_3

if __name__ == "__main__":
    # Initialize the Neo4j driver
    uri = "neo4j+s://b31eac3c.databases.neo4j.io"  # Replace with your Neo4j instance URI
    username = "neo4j"  # Replace with your username
    password = "XVgYO8b3cJcfQ_JjIlJbNbslriWJgfHnWZ9QPZHtPOE" 
    user_message = "i want to develope a web site in go lang."

    url_based_projects = URLBasedProjectRecommender(uri, username, password)
    projects = url_based_projects.get_projects_with_same_url_section("https://www.mindinventory.com/golang-development.php")
    top_3_projects = url_based_projects.get_top_suggestions(user_message, projects)

    print(top_3_projects)
    pass

        
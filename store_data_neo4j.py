from neo4j import GraphDatabase
import json
from sentence_transformers import SentenceTransformer
import numpy as np

class Neo4jDataStore():
    def __init__(self, uri, username, passcode):
        self.driver = GraphDatabase.driver(uri, auth=(username, passcode))
        print("connection done")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use another model if preferred

    # Function to create project nodes in Neo4j
    def create_project_node(self, tx, project, embedding):
        query = (
            "CREATE (p:Project {url_section: $url_section, title: $title, "
            "client: $client, challenge: $challenge, solution: $solution, "
            "results: $results, tech_stack: $tech_stack, embedding: $embedding})"
        )
        tx.run(query, url_section=project["url_section"],
            title=project["title"],
            client=project["client"],
            challenge=project["challenge"],
            solution=project["solution"],
            results=project["results"],
            tech_stack=project["tech_stack"],
            embedding=embedding.tolist())  # Convert to list for JSON storage

    # Function to insert data into Neo4j
    def insert_data(self, data):
        with self.driver.session() as session:

            for project in data['data']:
                # Combine relevant fields to generate a project description for embedding
                project_description = f"{project['title']} {project['client']} {project['challenge']} {project['solution']} {project['results']}"
                
                # Generate embedding for the project description
                embedding = self.model.encode(project_description)
                
                # Insert the data with embedding
                session.execute_write(self.create_project_node, project, embedding)

    def store_data_with_embeddings(self, json_file_path):

        with open(json_file_path, "r") as f:
            data = f.read()
            # Convert the JSON string to Python object
            data = json.loads(data)
            print(data)

            # Insert data into Neo4j
            self.insert_data(data)

            # Close the Neo4j driver connection
            self.driver.close()

if __name__ == "__main__":

    # Initialize the Neo4j driver
    uri = "neo4j+s://b31eac3c.databases.neo4j.io"  # Replace with your Neo4j instance URI
    username = "neo4j"  # Replace with your username
    password = "XVgYO8b3cJcfQ_JjIlJbNbslriWJgfHnWZ9QPZHtPOE"  # Replace with your password

    json_path = "data.json"

    neo_conn = Neo4jDataStore(uri, username, password)
    neo_conn.store_data_with_embeddings(json_path)
        

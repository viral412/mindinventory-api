from fastapi import FastAPI
from pydantic import BaseModel
from main import MindInventoryAutoMail

# Define the input data model using Pydantic
class UserInput(BaseModel):
    user_name: str
    user_urls: list[str]
    user_message: str

app = FastAPI()

# FastAPI GET endpoint to check the page load
@app.get("/")
def get_page_load_status():
    """
    Endpoint to check the page load status.

    Returns:
        str: A simple message indicating that the page has loaded successfully.
    """
    return {"message": "Page loaded successfully. Service is up and running!"}

# FastAPI endpoint to generate email
@app.post("/analyze-urls/")
def generate_email(user_input: UserInput):
    """
    Endpoint to generate an email based on user input.
    
    Args:
        user_input (UserInput): The user's details containing name, URLs, and message.
    
    Returns:
        str: Generated email content.
    """
    mail_system = MindInventoryAutoMail()
    
    # Process the input data to generate the email
    email_content = mail_system.process_data(
        user_input.user_name,
        user_input.user_urls,
        user_input.user_message
    )

    # Return the generated email content
    return email_content


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

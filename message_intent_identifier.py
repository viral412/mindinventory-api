from transformers import pipeline

class MessageIntentAnalyzer():

    def __init__(self):

        """
        Initialize the MessageIntentAnalyzer with a zero-shot-classification pipeline.

        This uses the Facebook BART large model trained on the MNLI dataset 
        for zero-shot classification to identify the intent of a given message.
        """

        try:
            # Load a zero-shot-classification pipeline
            self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        except Exception as e:
            raise RuntimeError(f"Error initializing the zero-shot-classification model: {str(e)}")

        # Define possible classes
        self.candidate_labels = ["client message", "job seeker"]

    
    def identify_message_intent(self, message: str) -> tuple:

        """
        Identify the intent of the given message.

        Parameters:
        message (str): The input message whose intent needs to be identified.

        Returns:
        Tuple[str, float]: A tuple containing the predicted intent (either "Client Message" 
                           or "Job Seeker Message") and the confidence score.

        Raises:
        ValueError: If the input message is empty or not a valid string.
        RuntimeError: If there is an error during classification.
        """

        if not message or not isinstance(message, str):
            raise ValueError("Input message must be a non-empty string.")

        try:
            # Perform zero-shot classification
            result = self.classifier(message, self.candidate_labels)
            
            # Extract the label with the highest score
            predicted_label = result['labels'][0]
            confidence_score = result['scores'][0]

            # Determine if the message is from a client or a job seeker
            if predicted_label == "client message":
                return "Client Message", confidence_score
            else:
                return "Job Seeker Message", confidence_score

        except Exception as e:
            raise RuntimeError(f"Error during message intent identification: {str(e)}")


if __name__ == "__main__":
    message =  "Hi, I just wanted to ask if you guys also handle computer repair or hardware installation services?"
    intent_analyzer = MessageIntentAnalyzer()
    intent, score = intent_analyzer.identify_message_intent(message)
    print(intent, score)
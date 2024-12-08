from openai import OpenAI

import os
import sys
import json
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OpenAI API key is not set. Please set it in the environment variable OPENAI_API_KEY.")
        sys.exit(1)

    # Ask for the job offer
    logging.info("Enter the job offer description, then press Enter:")
    job_offer = input().strip()
    if not job_offer:
        logging.error("No job offer provided. Exiting.")
        sys.exit(1)

    # Ask for the resume
    logging.info("Paste the candidate's resume below, then press Enter and Ctrl+D (EOF) to finish:")
    try:
        resume = sys.stdin.read().strip()
    except KeyboardInterrupt:
        logging.error("No resume provided. Exiting.")
        sys.exit(1)

    if not resume:
        logging.error("No resume content provided. Exiting.")
        sys.exit(1)

    # Add a separator for cleaner output
    logging.info("Processing the input... Here's the resume received:\n" + "=" * 40)
    print(resume + "\n" + "=" * 40)

    # Construct the prompt
    agent_role = """
    You are a recruitment assistant designed to evaluate candidate resumes for specific job roles. Your objective is to assess the candidate's suitability for a given role based on the relevant experience listed in their resume. You should provide a JSON output with the following fields:

    1. `experience_score`: A value between 0 and 100, calculated as follows:
       - Highly relevant experience in roles very similar to the offer contributes a lot. Experience in roles less similar to the job offer contributes less. Irrelevant roles do not contribute.
       - The duration of the experience (in months) significantly impacts the score. Short durations (less than a year) are less valuable than long durations.
       - Recency: Recent roles carry more weight; older roles contribute less.
       Scores of 75 and above indicate a strong match, and should not be given unless the candidate has a significant amount of highly relevant experience.

    2. `relevant_experience`: A list of relevant work experience entries, each containing the `role`, `company`, and `duration` fields (e.g., `{"role": "Software Engineer", "company": "TechCorp", "duration": "2 years"}`). Only include the most relevant entries.

    3. `experience_description`: A concise explanation of how the experience score was calculated, including relevance, duration, and recency of experience.

    If the job posting is in Spanish, your output must also be in Spanish. Ensure your analysis is objective and strictly based on the information provided.
    """

    prompt = f"""
    Job Role: {job_offer}
    Candidate Resume:
    {resume}
    Evaluate whether the candidate is a good fit for the specified role. Use the provided job role and resume to calculate the JSON fields as instructed in your role. Ensure that the `experience_score` reflects the relevance, duration, and recency of experience. If the job role is written in Spanish, respond in Spanish.
    """

    # Call the OpenAI API
    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": agent_role},
                {"role": "user", "content": prompt},
            ]
        )
        response = completion.choices[0].message.content
        #logging.info("Raw response from OpenAI:\n" + response)

        # Strip out any markdown code block delimiters
        if response.startswith("```json") and response.endswith("```"):
            response = response[7:-3].strip()

        # Parse and print the JSON output
        response_json = json.loads(response)
        print(json.dumps(response_json, indent=4, ensure_ascii=False))  # Nicely formatted JSON
    except json.JSONDecodeError as e:
        logging.error("Failed to parse JSON response from OpenAI: %s", e)
        logging.info("Raw response:\n" + response)
        sys.exit(1)
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
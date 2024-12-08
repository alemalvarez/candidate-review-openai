
# Resume Evaluation App

This application evaluates the suitability of a candidate's resume for a specific job role using OpenAI's GPT-4 model. It takes the job role and resume as inputs, processes them, and returns a structured JSON response with a calculated experience score, relevant experience, and an explanation of the score.

## Prerequisites

- Docker installed on your machine.
- OpenAI API Key (get one from [OpenAI API Key page](https://platform.openai.com/account/api-keys)).

## How to Build and Run the Docker Container

### Step 1: Build the Docker Container

1. Clone this repository or download the files.
2. Navigate to the project folder in your terminal.
3. Run the following command to build the Docker image:

   ```bash
   docker build -t resume-evaluation-app .

This will build the Docker container based on the Dockerfile in the repository.

### Step 2: Run the Docker Container

To run the app, pass your OpenAI API key as an environment variable via the docker run command. Replace <your-openai-api-key> with your actual OpenAI API key.

```bash
docker run -e OPENAI_API_KEY=<your-openai-api-key> -it resume-evaluation-app
```

## How to Input Data

**Job Role**

After running the app, it will first ask you to input the job role. Simply type the job description and press Enter.


**Resume**

After entering the job role, you will be prompted to input the resume. Paste the resume into the terminal.
> **Important:** After pasting the resume, press **Enter** followed by **Ctrl+D (EOF)** to finish the input.

### Example:

Enter the job offer description, then press Enter:
```Software Engineer at XYZ Corp```

Paste the candidate's resume below, then press Enter and Ctrl+D (EOF) to finish:
```
John Doe has been working as a software engineer at ABC Tech for 3 years...
(CTRL+D)
```

**Output**

Once the input is provided, the app will display a nicely formatted JSON output that includes:
- experience_score: A score between 0 and 100 that reflects the candidate’s suitability for the job.
- relevant_experience: A list of relevant work experiences, including role, company, and duration.
- experience_description: A brief explanation of how the experience score was calculated.

Example of output:

```json
{
    "experience_score": 75,
    "relevant_experience": [
        {
            "role": "Software Engineer",
            "company": "ABC Tech",
            "duration": "3 years"
        }
    ],
    "experience_description": "The candidate has 3 years of experience as a Software Engineer at ABC Tech, which is highly relevant for the job role."
}
```

Troubleshooting
- If you encounter issues with the OpenAI API response, ensure that your API key is valid and that you are passing it correctly in the docker run command.
- Make sure to enter the resume correctly. It’s important to press Enter followed by Ctrl+D to mark the end of the resume input.


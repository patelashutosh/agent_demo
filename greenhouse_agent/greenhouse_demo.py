"""
Greenhouse ATS Browser Agent Demo - Browser Agent with LangGraph

This demo shows the LangGraph-based browser agent automating job posting 
on Greenhouse ATS (Applicant Tracking System).

Task: Login to Greenhouse and create a sample job posting.
"""
import asyncio
import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import from simple_browser_agent
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir / 'simple_browser_agent'))

from agent import LangGraphBrowserAgent

# Load environment variables from .env file
# Look for .env in project root (parent directory)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)


async def main():
    """Run Greenhouse ATS job posting demo"""
    
    # Validate environment variables are set
    # (Agent will do this too, but check early for better error messages)
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY"
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please create a .env file with your Azure OpenAI credentials.\n"
            "See env.example for a template."
        )
    
    # Get configuration for display purposes only
    deployment_name = os.getenv(
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o-mini"
    )
    
    # ============================================================
    # TASK - Login to Greenhouse and Create Job Posting
    # ============================================================
    
    # Get Greenhouse credentials from environment variables
    greenhouse_email = os.getenv("GREENHOUSE_EMAIL")
    greenhouse_password = os.getenv("GREENHOUSE_PASSWORD")
    
    if not greenhouse_email or not greenhouse_password:
        raise ValueError(
            "Missing Greenhouse credentials!\n"
            "Please set GREENHOUSE_EMAIL and GREENHOUSE_PASSWORD in your .env file.\n"
            "See env.example for template."
        )
    
    task = f"""You are an autonomous recruiter assistant working with Greenhouse ATS.

YOUR MISSION:
Navigate to the applications page for a specific job posting.

CREDENTIALS:
- Login URL: https://app8.greenhouse.io/users/sign_in
- Email: {greenhouse_email}
- Password: {greenhouse_password}

TARGET JOB:
Search for "19Sep Part 2 Staff Engineer JobPosting" and access its applications.

HIGH-LEVEL WORKFLOW:
1. Authenticate into the system
2. Navigate to the Jobs section
3. Search for the target job posting
4. Open the job from search results
5. Access the applications review area

SUCCESS CRITERIA:
You've completed the task when you reach the page where you can view candidate applications for the job.

GUIDELINES:
- Take your time between actions to let pages load
- If something doesn't work, try alternative approaches
- Report success with the job name when you reach the applications page"""
    
    # ============================================================
    # AGENT SETUP
    # ============================================================
    
    print("\n" + "="*70)
    print("GREENHOUSE ATS JOB NAVIGATION AGENT DEMO (LangGraph)")
    print("="*70)
    print(f"\nTask: Login, search for a job, and navigate to applications")
    print(f"\nUsing: LangGraph + Azure OpenAI ({deployment_name})")
    print("="*70 + "\n")
    
    # Create the LangGraph agent (loads credentials from env internally)
    agent = LangGraphBrowserAgent(
        task=task,
        headless=False,  # Set to True to hide browser window
        max_steps=20  # Simplified workflow
    )
    
    # ============================================================
    # RUN THE AGENT
    # ============================================================
    
    try:
        result = await agent.run()
        
        print("\n" + "="*70)
        print("NAVIGATION COMPLETE!")
        print("="*70)
        print(f"\n{result}\n")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Run the Greenhouse job posting demo
    asyncio.run(main())



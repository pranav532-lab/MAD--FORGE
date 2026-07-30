from prompt_processor import process_prompt
from search_generator import generate_search_queries
from google_search import search_google
from scraper import scrape_website
from company_analyzer import analyze_company
from database import save_company, close_connection


def main():

    print("=" * 60)
    print("AI CLIENT ACQUISITION SYSTEM")
    print("=" * 60)

    user_prompt = input("\nDescribe your ideal client:\n\n")

    # Step 1 - Prompt Processing
    print("\n[1/6] Processing prompt...")
    prompt_data = process_prompt(user_prompt)

    # Step 2 - Search Query Generation
    print("[2/6] Generating Google searches...")
    search_queries = generate_search_queries(prompt_data)

    # Step 3 - Google Search
    print("[3/6] Searching Google...")
    websites = search_google(search_queries)

    print(f"Found {len(websites)} new websites.\n")

    if not websites:
        print("No new companies found.")
        close_connection()
        return

    # Our services (later these can come from prompt_data or a config file)
    our_services = [
        "AI Automation",
        "Workflow Automation",
        "Custom AI Solutions",
        "CRM Automation",
        "Document Processing",
        "Meeting Minutes Generator",
        "Internal AI Assistants",
        "Email Automation"
    ]

    # Step 4 onwards
    for i, website in enumerate(websites, start=1):

        print("-" * 60)
        print(f"Company {i}/{len(websites)}")
        print(website["website"])

        # Step 4 - Scrape
        print("Scraping website...")
        scraped_data = scrape_website(website["website"])

        # Step 5 - Analyze
        print("Analyzing company...")
        analysis = analyze_company(
            scraped_data,
            our_services
        )

        # Step 6 - Save
        save_company(
            website=website["website"],
            score=analysis["score"],
            selected=analysis["selected"]
        )

        print("\nRESULT")
        print(f"Company : {analysis['company_name']}")
        print(f"Score   : {analysis['score']}")
        print(f"Selected: {analysis['selected']}")
        print(f"Email   : {analysis['contact_email']}")
        print()

    close_connection()

    print("=" * 60)
    print("PROCESS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
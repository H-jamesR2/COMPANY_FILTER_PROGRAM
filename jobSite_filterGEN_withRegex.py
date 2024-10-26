import os
import re

def update_filter_index():
    # Ensure the filter index file exists
    if not os.path.exists('Job_Company_Filter_INDEX.txt'):
        with open('Job_Company_Filter_INDEX.txt', 'w') as file:
            file.write("Initial filter entry\n")
        print("Created new 'Job_Company_Filter_INDEX.txt'.")

    print("Updating 'Job_Company_Filter_INDEX.txt'...")

    # Read existing entries from the filter index file
    existing_entries = set()
    with open('Job_Company_Filter_INDEX.txt', 'r') as file:
        for line in file:
            existing_entries.add(line.strip().lower())  # Convert to lowercase and remove whitespace

    # Update the filter index file
    with open('Job_Company_Filter_INDEX.txt', 'a') as file:
        while True:
            company = input("Enter a company to add to the filter (or type 'done' to finish): ")
            if company.lower() == 'done':
                break
            # Remove extra whitespace from company name
            company = ' '.join(company.split())
            # Convert company name to lowercase for case-insensitive comparison
            company_lower = company.lower()
            if company_lower not in existing_entries:  # Check if company name already exists
                file.write(f"{company}\n")
                print(f"Added '{company}' to the filter list.")
                existing_entries.add(company_lower)  # Add lowercase version to existing entries
            else:
                print(f"Company '{company}' already exists in the filter list.")

def create_company_filter_list():
    # Ensure the filter index file exists
    if not os.path.exists('Job_Company_Filter_INDEX.txt'):
        print("No 'Job_Company_Filter_INDEX.txt' file found. Please update the filter index first.")
        return

    # Read existing entries from the filter index file
    with open('Job_Company_Filter_INDEX.txt', 'r') as file:
        companies = [line.strip() for line in file if line.strip()]

    if not companies:
        print("No companies found in 'Job_Company_Filter_INDEX.txt'. Please update the filter index first.")
        return

    print("Which Job Site are you trying to generate a company filter list for?")
    job_sites = ["Linkedin", "Indeed", "ZipRecruiter", "Glassdoor", "GoogleJobs"]
    for i, site in enumerate(job_sites, 1):
        print(f"({i}) {site}")

    while True:
        try:
            choice = (input("Enter the number corresponding to the job site (or type 'done' to finish): "))
            if choice.lower() == 'done':
                return
            # convert choice to INT and check if Valid
            choice = int(choice)
            if 1 <= choice <= len(job_sites):
                selected_site = job_sites[choice - 1]
                print(f"Generating company filter list for {selected_site}...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number OR done.")

    filters = {
        "Linkedin": [
            "! Linkedin Company Search Feed",
            'linkedin.com##li.reusable-search__result-container:has(div.entity-result__primary-subtitle:has-text(/({pattern})/i))',
            "",
            "! Linkedin Job Feed",
            'linkedin.com##li.ember-view.jobs-search-results__list-item:has(span.job-card-container__primary-description:has-text(/({pattern})/i))',
            "",
            "! Linkedin Filter-Out: Removed from job feed (Removed, Applied)",
            'linkedin.com##li.ember-view.jobs-search-results__list-item:has(div.artdeco-entity-lockup__caption:has(span:has-text(We won’t show you this job again)))',
            'linkedin.com##li.ember-view.jobs-search-results__list-item:has(ul.job-card-list__footer-wrapper:has(li.job-card-container__footer-job-state:has-text(Applied)))'
        ],
        "Indeed": [
            "! Indeed Job Search Feed",
            'indeed.com##li:has(span[data-testid="company-name"]:has-text(/({pattern})/i))',
            ""
            #'indeed.com##.company:has(a[href*="/{pattern}/"])'
        ],
        "ZipRecruiter": [
            'ziprecruiter.com##.job_content:has(a[href*="/{pattern}/"])',
            'ziprecruiter.com##.company:has(a[href*="/{pattern}/"])'
        ],
        "Glassdoor": [
            'glassdoor.com##.jobListing:has(a[href*="/{pattern}/"])',
            'glassdoor.com##.companyInfo:has(a[href*="/{pattern}/"])'
        ],
        "GoogleJobs":[
            '! Block job listings for multiple companies on Google Jobs',
            'google.com##li.iFjolb.gws-plugins-horizon-jobs__li-ed:has-text((/({pattern})/i))',
            ""
        ]
    }

    # Create a single regex pattern for the company names
    regex_pattern = '|'.join([re.escape(company) for company in companies])

    filter_list = []  # Store the filter entries

    for template in filters[selected_site]:
        # Replace {pattern} in the template with the regex pattern
        filter_entry = template.replace("{pattern}", regex_pattern)
        filter_list.append(filter_entry)

    if filter_list:
        # Save the filter list to a file
        with open(f'{selected_site}_Company_Filter_List.txt', 'w') as file:
            for filter_entry in filter_list:
                file.write(f"{filter_entry}\n")
        print(f"Company filter list for {selected_site} saved to '{selected_site}_Company_Filter_List.txt'.")
    else:
        print("No filters were created.")

def main():
    while True:
        print("\nChoose an option (or type ':q' to quit):")
        print("(1) Update 'Job Company Filter INDEX'")
        print("(2) Create a company filter list for Job Sites")

        choice = input("Enter the number corresponding to your choice: ").strip()
        if choice == ':q':
            print("Exiting program.")
            break
        try:
            option = int(choice)
            if option == 1:
                update_filter_index()
            elif option == 2:
                create_company_filter_list()
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number or ':q' to quit.")

if __name__ == "__main__":
    main()
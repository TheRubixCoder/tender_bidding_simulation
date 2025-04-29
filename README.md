# 🎮 Simple Tender Simulation Playground 🏆

This Streamlit application provides a hands-on simulation of different tender (auction) mechanisms. You can create new jobs (tenders), participate in them by submitting bids, simulate bids from AI "friends" using different strategies, and see the results.

## Features

* **Create New Tenders:** Define a job description and choose the type of tender rules you want to use. Currently supported types are:
    * **First Price Sealed Bid (Lowest Bid Wins):** The bidder with the lowest unique bid wins and pays their bid amount.
    * **Second Price Sealed Bid (Vickrey):** The bidder with the lowest unique bid wins but pays the amount of the second-lowest bid.
* **Participate in Open Jobs:** View a list of currently open tenders and submit your price offer (bid) for the job you choose. You'll need to provide your name/company and your bid amount.
* **Simulate AI Bids:** For a selected open tender, you can simulate bids from multiple AI "friends." You can configure:
    * **Number of AI bidders:** How many AI bids to generate.
    * **AI Bidding Strategy:**
        * **Cost Plus Markup:** AI bids are calculated based on a randomly generated secret cost (within a specified range) plus a percentage markup you define.
        * **Nash Equilibrium (Uniform Costs):** AI bids are generated based on a simplified Nash Equilibrium strategy assuming uniform cost distribution among bidders. You need to specify the total expected number of bidders for this strategy.
    * **AI Secret Cost Range:** The minimum and maximum possible secret costs for the AI bidders.
    * **AI Bid Markup % (for Cost Plus Markup):** The percentage markup the AI will add to its cost.
* **Close Bidding and Find Winner:** Once enough bids have been submitted (including yours and/or AI bids), you can close the bidding for a specific tender. The application will then determine the winner based on the selected tender rules and display the results, including the winner, their submitted bid, and the price they pay.
* **View Finished Jobs (Archive):** See a list of all the tenders for which bidding has closed. You can view the status, the winner, their original bid, and the final price paid. You also have the option to see all the bids submitted for a closed tender, sorted by price.

## How to Use

1.  **Create a New Tender:**
    * Enter a description for the job in the "Create a New Tender" section.
    * Choose the desired tender rules from the "Choose the Tender Rules:" dropdown.
    * Click the "Create This Job" button. A unique Secret ID for the job will be generated.
2.  **Participate in a Job:**
    * In the "Participate in a Job (Submit Your Bid)" section, if there are any open tenders, they will appear in the "Choose a Job:" dropdown.
    * Select the job you want to bid on.
    * Enter your name or company in the "Your Name or Company:" field.
    * Enter your price offer in the "Your Price Offer (₹):" field.
    * Click the "Submit My Price Offer" button.
3.  **Simulate AI Friends' Offers (Optional):**
    * After selecting an open job, in the "Simulate AI Friends' Offers" section:
        * Choose an AI bidding strategy.
        * Enter the number of AI bidders you want to simulate.
        * Define the range for the AI's secret costs.
        * If using "Cost Plus Markup," adjust the markup percentage using the slider. If using "Nash Equilibrium," ensure the "How many AI friends should make offers?" and the implicit number of your own bid are consistent with a reasonable "total expected bidders."
        * Click the "Simulate AI Friends' Offers" button.
4.  **Close Bidding and Find Winner:**
    * For the selected open job, click the "Close Bidding & Find Winner" button in the "🏆 Find the Winner!" section.
    * The application will determine and display the winner based on the tender rules and all the submitted bids. The job's status will be updated to "closed."
5.  **View Finished Jobs:**
    * In the "Archive: Finished Jobs" section, you'll see a list of all closed tenders.
    * For each finished job, you can see the description, status, winner information (if any), and an option to "Show all offers" submitted for that tender.

## Running the Application

To run this application, you need to have Python and Streamlit installed.

1.  **Install Streamlit:**
    ```bash
    pip install streamlit numpy pytz
    ```
2.  **Save the code:** Save the provided Python code as a `.py` file (e.g., `app.py`).
3.  **Run the application:** Open your terminal or command prompt, navigate to the directory where you saved the file, and run:
    ```bash
    streamlit run app.py
    ```

This will open the application in your web browser.

## Notes

* The application uses Streamlit's session state (`st.session_state`) to remember the created tenders and submitted bids across interactions.
* AI bidding strategies are simplified simulations and do not represent real-world AI bidding complexities.
* The Nash Equilibrium strategy implemented here assumes uniform cost distribution for simplicity.
* The user interface includes helpful messages and warnings to guide you through the simulation.
* Mathematical notations are not used in this README as it's a plain text format.

Have fun experimenting with different tender scenarios! 🚀

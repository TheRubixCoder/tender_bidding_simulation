import streamlit as st
import numpy as np
import uuid
from datetime import datetime
import pytz

# --- Now, the control panel starts! ---

if 'tenders' not in st.session_state:
    st.session_state.tenders = {} # The box for all the job details

if 'all_bids' not in st.session_state:
    st.session_state.all_bids = {} # The box for all the price offer lists

# Put a big title at the top of the control panel page
st.title("🎮 Simple Tender Simulation Playground 🏆") # Added some fun emojis!

# --- Section for Making New Jobs ---
st.header("➕ Create a New Tender") # A smaller title for this section

# A box where you can type the job description
tender_desc = st.text_input("What kind of job is this? (e.g., 'Paint the Fence', 'Build a Treehouse'):")

# *** ADD THIS NEW PART ***
# A box to choose the type of tender rules
tender_type = st.selectbox(
    "Choose the Tender Rules:",
    options=["First Price Sealed Bid (Lowest Bid Wins)", "Second Price Sealed Bid (Vickrey)"],
    key="new_tender_type_select" # Unique key
)
# ************************

# A button to click when you're ready to create the job
if st.button("Create This Job"):
    # When the button is clicked, do this:
    if tender_desc: # Check if you actually typed something
        # Use the 'create_tender' rule from our simulation brain!
        # The brain will give us back the secret ID name
        tender_id = str(uuid.uuid4()) # Generate a unique ID here in the UI now, simpler
        ist = pytz.timezone('Asia/Kolkata')
        st.session_state.tenders[tender_id] = {"description": tender_desc, "status": "open", "type": tender_type, "created_at": datetime.now(ist)}
        st.session_state.all_bids[tender_id] = [] # Initialize empty bid list
        st.success(f"🎉 Job '{tender_desc}' created! Secret ID: {tender_id}") # Show a happy message!
    else:
        st.warning("😅 Oops! Please type a job description first.") # Show a little warning

# --- Section for Playing in Open Jobs ---
st.header("✍️ Participate in a Job (Submit Your Bid)") # Another smaller title

# Find jobs that are still 'open' in our memory box
open_tenders = {tid: t['description'] for tid, t in st.session_state.tenders.items() if t['status'] == 'open'}

# Check if there are any open jobs
if not open_tenders:
    st.info("😴 No jobs are open right now. Create one above!") # Message if no jobs are open
else:
    # If there are open jobs, show a drop-down list to pick one
    selected_tender_id = st.selectbox(
        "Choose a Job:",
        options=list(open_tenders.keys()), # The secret IDs are the options
        format_func=lambda tid: open_tenders[tid] # Show the job description instead of the ID
    )

    # If a job is selected from the list, show the bidding form
    if selected_tender_id:
        st.subheader(f"Your Offer for: {open_tenders[selected_tender_id]}") # Title for the form

        # Box to type your name or company
        # The 'key' helps Streamlit remember what's typed even if you switch tenders
        bidder_name = st.text_input("Your Name or Company:", key=f"name_{selected_tender_id}")

        # Box to type your price offer (only allows numbers, minimum 0.01)
        bid_amount = st.number_input(
            "Your Price Offer (₹):",
            min_value=0.01,
            step=1.0,
            format="%.2f", # Show 2 decimal places like money
            key=f"bid_{selected_tender_id}" # Unique key
        )

        # Button to click to send your price offer
        if st.button("Submit My Price Offer", key=f"submit_{selected_tender_id}"):
            # When the button is clicked, do this:
            if bidder_name and bid_amount > 0: # Check if name is typed and bid is valid
                # Make a little note for your bid
                bid_data = {"bidder_name": bidder_name, "bid_amount": bid_amount}
                # Add your note to the list of bids for this job in our memory box
                st.session_state.all_bids[selected_tender_id].append(bid_data)
                st.success(f"✅ Your price offer was sent for {open_tenders[selected_tender_id]}!") # Success!
            else:
                st.warning("🧐 Please enter your name and a price offer greater than 0.") # Warning if something is missing

       # --- Section for Imaginary Friends (AI Bidding) ---
        st.subheader("🤖 Simulate AI Friends' Offers") # Another smaller title

        # *** ADD THIS PART ***
        # Select AI Strategy
        ai_strategy = st.selectbox(
            "Choose AI Bidding Strategy:",
            options=["Cost Plus Markup", "Nash Equilibrium (Uniform Costs)"],
            key=f"ai_strategy_{selected_tender_id}" # Unique key
        )
        # *********************

        # Box to choose how many AI friends to add
        num_ai = st.number_input(
            "How many AI friends should make offers?",
            min_value=0,
            value=3,
            step=1,
            key=f"ai_num_{selected_tender_id}"
        )

        total_expected_bidders = num_ai + 1

        # Boxes to guess the AI friends' secret costs (min and max)
        ai_min_cost = st.number_input(
            "AI friends' lowest possible secret cost ($):",
            min_value=1.0,
            value=1000.0,
            step=100.0,
            key=f"ai_min_{selected_tender_id}"
        )
        ai_max_cost = st.number_input(
            "AI friends' highest possible secret cost ($):",
            min_value=1.0,
            value=10000.0,
            step=100.0,
            key=f"ai_max_{selected_tender_id}"
        )

        # Slider for markup (only used if strategy is Cost Plus Markup)
        if ai_strategy == "Cost Plus Markup":
             ai_markup = st.slider(
                 "AI Bid Markup %:",
                 min_value=5,
                 max_value=100,
                 value=15,
                 step=1,
                 key=f"ai_markup_{selected_tender_id}"
             )


        # Button to click to make the AI friends make their offers
        if st.button("Simulate AI Friends' Offers", key=f"simulate_ai_{selected_tender_id}"):
            # When the button is clicked, do this:
            if ai_max_cost >= ai_min_cost and num_ai > 0: # Check if settings make sense and num_ai > 0
                # Check if inputs for selected strategy are valid
                if ai_strategy == "Nash Equilibrium (Uniform Costs)" and (total_expected_bidders is None or total_expected_bidders < num_ai):
                     st.warning("🤔 Please enter a valid total expected number of bidders for the Nash strategy (at least the number of AI being simulated).")
                else:
                    simulated_bids_info = [] # To show details later if needed
                    for i in range(num_ai):
                        # Guess the secret cost for this AI friend
                        ai_cost = np.random.uniform(ai_min_cost, ai_max_cost)
                        ai_name = f"AI Friend {i+1}"
                        ai_bid = 0 # Initialize bid

                        # Calculate bid based on selected strategy
                        if ai_strategy == "Cost Plus Markup":
                            # Basic AI simulation directly here
                            ai_bid = ai_cost * (1 + ai_markup / 100.0)
                            strategy_note = f"Cost: ${ai_cost:.2f}, Markup: {ai_markup}%"

                        elif ai_strategy == "Nash Equilibrium (Uniform Costs)":
                            # Apply Nash Equilibrium formula for uniform costs
                            N = total_expected_bidders # Use the user-provided total bidders
                            C_max = ai_max_cost
                            c = ai_cost

                            if N > 1:
                                ai_bid = C_max - ((N - 1) / N) * (C_max - c)
                            else: # If N=1, the bid is simply the cost to make profit (or max cost, depends on model)
                                # In a tender with 1 bidder, they could bid just below max cost.
                                # For simplicity here, let's say they bid their cost + a small amount or near max cost.
                                # Let's use a simple markup or near max_cost if N=1 in Nash context
                                ai_bid = ai_cost * 1.1 # Simple 10% markup if they are the only bidder in this model
                                # Or arguably, bid just below C_max? Depends on exact single-bidder assumption.
                                # Let's stick to a simple markup for N=1 to avoid overcomplication of Nash for 1 bidder.


                            # Ensure bid is not less than cost (unless Nash formula allows slight variance at edges)
                            # If C_max == c and N=1, formula is C_max - 0, so bid = C_max.
                            # If c == ai_min_cost and N>1, bid = C_max - (N-1)/N * (C_max - ai_min_cost).
                            # For robustness, maybe add a check:
                            ai_bid = max(ai_bid, ai_cost * 1.01) # Ensure bid is slightly above cost

                            strategy_note = f"Cost: ${ai_cost:.2f}, N: {N}, C_max: ${C_max:.2f}"


                        # Ensure bid is realistic (e.g., > 0)
                        ai_bid = max(0.01, ai_bid)

                        # Remember their bid details
                        bid_data = {"bidder_name": ai_name, "bid_amount": ai_bid}
                        # Add their bid to the list of bids for this job in our memory box
                        st.session_state.all_bids[selected_tender_id].append(bid_data)
                        # Optionally remember cost and strategy details for info
                        simulated_bids_info.append({"bidder_name": ai_name, "bid_amount": ai_bid, "ai_cost (hidden)": ai_cost, "strategy_info": strategy_note})


                    st.info(f"🤖 Simulated {num_ai} AI friends making offers using the '{ai_strategy}' strategy.") # Tell the user what happened
                    # You could uncomment the line below to see the AI's secret costs, bids, and strategy details!
                    # st.write("🤫 AI Friend details (for you):", simulated_bids_info)

            elif num_ai == 0:
                 st.info("😊 You chose to simulate 0 AI friends.")
            else:
                st.warning("🤔 The highest cost must be the same or greater than the lowest cost for AI simulation.") # Warning if min/max costs are wrong

        # --- Section to Find the Winner ---
        st.subheader("🏆 Find the Winner!") # Another smaller title

        # Button to close the job and find the winner
        if st.button("Close Bidding & Find Winner", key=f"close_{selected_tender_id}"):
            # When the button is clicked, do this:
            # Get all the bids for this job from our memory box
            bids_for_tender = st.session_state.all_bids[selected_tender_id]

            if not bids_for_tender: # Check if anyone made an offer
                st.warning("😔 Nobody made an offer for this job yet.") # Message if no bids
            else:
                # Get the type of tender from our memory box
                tender_info = st.session_state.tenders[selected_tender_id]
                tender_type = tender_info['type'] # *** GET THE STORED TYPE ***

                # To find the second lowest bid, we need to sort the bids
                sorted_bids = sorted(bids_for_tender, key=lambda bid_note: bid_note['bid_amount'])

                # First, find the lowest bid - this bidder is always the winner in these types
                winner_bid_info = sorted_bids[0]
                winner_name = winner_bid_info['bidder_name']
                lowest_bid_amount = winner_bid_info['bid_amount']

                winning_price_paid = 0 # Variable to store the final price paid

                if tender_type == "First Price Sealed Bid (Lowest Bid Wins)":
                    winning_price_paid = lowest_bid_amount
                    winner_info_display = f"**Winner:** {winner_name} with the lowest bid of ${lowest_bid_amount:.2f}. **They pay their bid amount.**"
                    result_message = "First Price Auction Results:"

                elif tender_type == "Second Price Sealed Bid (Vickrey)":
                    if len(sorted_bids) > 1:
                        # The winner is the lowest bidder, but they pay the second lowest bid amount
                        second_lowest_bid_amount = sorted_bids[1]['bid_amount'] # The second item after sorting is the second lowest
                        winning_price_paid = second_lowest_bid_amount
                        winner_info_display = f"**Winner:** {winner_name} with the lowest bid of ${lowest_bid_amount:.2f}. They pay the amount of the second lowest bid: ${second_lowest_bid_amount:.2f}."
                        result_message = "Second Price (Vickrey) Auction Results:"
                    else:
                        # If only one bid, the winner pays their own bid (standard for single bids in Vickrey)
                         winning_price_paid = lowest_bid_amount
                         winner_info_display = f"**Winner:** {winner_name} with the only bid of ${lowest_bid_amount:.2f}. They pay their bid amount.(Only one bid submitted)"
                         result_message = "Second Price (Vickrey) Auction Results:"

                # Mark the job as 'closed' in our tenders memory box
                st.session_state.tenders[selected_tender_id]['status'] = 'closed'
                # Store winner details and the price paid
                st.session_state.tenders[selected_tender_id]['winner'] = {
                    "bidder_name": winner_name,
                    "bid_amount_submitted": lowest_bid_amount, # Keep track of their actual bid
                    "price_paid": winning_price_paid # Store the amount they actually pay
                }


                st.success(f"🥳 Bidding is CLOSED for: {tender_info['description']} ({tender_type})!") # Celebration message!
                st.subheader(result_message) # Results title

                # Show the winner!
                st.write(winner_info_display)

                # Show a table of all the offers made
                st.write("**All Offers Submitted:**")
                # You might want to show the actual bid amount here, not the price paid
                st.dataframe(sorted_bids) # Show all bids in a nice table

# --- Section to See Finished Jobs ---
st.header("Archive: Finished Jobs") # Another smaller title

# Find jobs that are 'closed' in our memory box
closed_tenders = {tid: t for tid, t in st.session_state.tenders.items() if t['status'].startswith('closed')} # Check for 'closed' or 'closed (no bids)'

if not closed_tenders:
    st.info("📂 No jobs have finished yet.") # Message if no closed jobs
else:
    # Show a list of finished jobs
    st.write("Here are the jobs that are finished:")
    for tender_id, tender_info in closed_tenders.items():
        st.subheader(f"Job: {tender_info['description']}")
        st.write(f"Status: **{tender_info['status']}**")
        if 'winner' in tender_info: # Check if there was a winner stored
            st.write(f"Winner: **{tender_info['winner']['bidder_name']}** with a bidded amount of **₹{tender_info['winner']['bid_amount_submitted']:.2f}** and paid **₹{tender_info['winner']['price_paid']:.2f}**")

        # Option to view all bids for a closed tender
        if st.button(f"Show all offers for {tender_info['description']}", key=f"show_bids_{tender_id}"):
             if tender_id in st.session_state.all_bids and st.session_state.all_bids[tender_id]:
                # Show a table of all the offers made in ascending order of bid amount
                st.write("**All Offers Submitted (Sorted by Price):**")
                # Sort bids_for_tender by bid_amount in ascending order
                sorted_bids = sorted(st.session_state.all_bids[tender_id], key=lambda bid: bid['bid_amount'])
                st.dataframe(sorted_bids) # Show all bids in a nice table, sorted from lowest to highest
             else:
                st.info("No offers were submitted for this job.")
'''
This file is not useful in anyway for this project.
The code in this file is represents the brain of this project and answers questions like how this project thinks? etc..
'''

import numpy as np
import uuid
from datetime import datetime
import pytz

print("From Simulation: Simulation brain is ready!")

all_tenders = {}  # Box for all jobs, labeled by their secret name (ID)
all_bids = {} # Box for lists of prices, also labeled by the job's secret name (ID)

# Rule block for making a new job
def create_tender(description):
    print(f"From Simulation: Someone wants to make a new job: {description}")
    # 1. Get a unique secret name
    tender_id = str(uuid.uuid4()) # Makes a complicated unique name like "123-abc-456"
    print(f"From Simulation: We'll call this job secretly: {tender_id}")

    # 2. Put job info in the 'all_tenders' box
    ist = pytz.timezone('Asia/Kolkata')
    all_tenders[tender_id] = {"description": description, "status": "open", "created_at": datetime.now(ist)}
    print(f"From Simulation: Job '{description}' is now in the tenders box and is open!")

    # 3. Make an empty list ready for prices in the 'all_bids' box
    all_bids[tender_id] = []
    print(f"From Simulation: Made an empty price list ready for job {tender_id}")

    # 4. Tell them the secret name
    return tender_id

# Rule block for adding a price offer
def add_bid(tender_id, bidder_name, bid_amount):
    print(f"From Simulation: {bidder_name} wants to offer ${bid_amount} for job {tender_id}")
    # 1. Make the little note
    bid_note = {"bidder_name": bidder_name, "bid_amount": bid_amount}
    print(f"From Simulation: Made a note: {bid_note}")

    # 2. Find the right list in the 'all_bids' box
    # 3. Add the note to that list
    if tender_id in all_bids: # Safety check: Does this job exist in our bids box?
        all_bids[tender_id].append(bid_note)
        print(f"From Simulation: Added the note to the price list for job {tender_id}")
    else:
        print(f"From Simulation: Uh oh! Cannot find a price list for job {tender_id}")

# Rule block for imaginary friends offering prices
def simulate_ai_bidders(tender_id, num_ai, min_cost, max_cost, markup_percent):
    print(f"From Simulation: Let's make {num_ai} imaginary friends offer prices for job {tender_id}")
    print(f"From Simulation: Their secret costs will be between {min_cost} and {max_cost}.")
    print(f"From Simulation: They will add {markup_percent}% extra to their cost for their price.")

    for i in range(num_ai): # Do this 'num_ai' times
        # 1. Guess the secret cost
        ai_cost = np.random.uniform(min_cost, max_cost)
        print(f"From Simulation: Friend {i+1}'s secret cost is {ai_cost:.2f}") # .2f means show 2 decimal places

        # 2. Calculate their price (cost + markup)
        ai_bid = ai_cost * (1 + markup_percent / 100.0)
        print(f"From Simulation: Friend {i+1}'s price offer is {ai_bid:.2f}")

        # 3. Give them a name
        ai_name = f"AI Friend {i + 1}"

        # 4. Use the add_bid rule to add their offer
        add_bid(tender_id, ai_name, ai_bid)

# Rule block for finding the winner
def determine_winner(tender_id):
    print(f"From Simulation: Okay, time to find the winner for job {tender_id}!")
    # 1. Get the list of prices for this job
    if tender_id not in all_bids:
        print(f"From Simulation: Uh oh! Cannot find any price list for job {tender_id}")
        return None, [] # Return nothing found

    bids_for_this_tender = all_bids[tender_id]
    print(f"From Simulation: Found {len(bids_for_this_tender)} price offers for this job.")

    # 2. Check if anyone offered a price
    if not bids_for_this_tender: # Checks if the list is empty
        print("From Simulation: Oops! Nobody offered a price for this job.")
        # Still mark the tender as closed if desired
        if tender_id in all_tenders:
             all_tenders[tender_id]["status"] = "closed (no bids)"
        return None, [] # Return no winner, empty list

    # 3. Find the note with the smallest price
    winner_note = min(bids_for_this_tender, key=lambda note: note['bid_amount'])
    print(f"From Simulation: Found the smallest price offer! It's: {winner_note}")

    # 4. Remember the winner (already done by finding 'winner_note')

    # 5. Mark the job as closed in the 'all_tenders' box
    if tender_id in all_tenders:
        all_tenders[tender_id]["status"] = "closed"
        all_tenders[tender_id]["winner_info"] = winner_note # Store winner info too!
        print(f"From Simulation: Marked job {tender_id} as closed.")

    # 6. Tell everyone the results!
    print(f"From Simulation: *** The winner is {winner_note['bidder_name']} with a price of ${winner_note['bid_amount']:.2f}! ***")
    return winner_note, bids_for_this_tender # Return winner note and the full list

# Turn-Based Character Duel Simulator

This is a Python project that simulates a duel between two characters.

## What it does

- Generates two random characters
- Assigns each character attack, defense, health, and a special ability
- Runs a turn-based fight until one character loses all health
- Runs 1000 simulations to estimate win rates
- Includes a Streamlit interface for interactive testing

## Design choice

I modeled abilities as separate classes instead of simple strings.  
This makes the code easier to extend because new abilities can be added without changing the main duel logic.

I also added a minimum damage of 1 to make sure every duel eventually ends.

## How to run

```bash
streamlit run app.py

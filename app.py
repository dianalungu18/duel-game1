import random
import streamlit as st


# ================== ABILITIES ==================

class Ability:
    def modify_attack(self, attacker, defender, damage):
        return damage

    def modify_defense(self, attacker, defender, damage):
        return damage

    def after_damage(self, defender, previous_health):
        pass


class DamageReduction(Ability):
    def modify_defense(self, attacker, defender, damage):
        if random.random() < 0.25:
            return max(1, damage // 2)
        return damage


class PowerStrike(Ability):
    def modify_attack(self, attacker, defender, damage):
        if random.random() < 0.25:
            return int(damage * 1.5)
        return damage


class SecondWind(Ability):
    def after_damage(self, defender, previous_health):
        if (
            random.random() < 0.25
            and previous_health >= 30
            and defender.health < 30
            and defender.health > 0
        ):
            defender.health += 5


# ================== CHARACTER ==================

class Character:
    def __init__(self, name_id):
        self.name = f"Character {name_id}"
        self.max_health = 100
        self.health = 100
        self.attack_power = random.randint(15, 20)
        self.defense_power = random.randint(10, 15)

        self.ability = random.choice([
            DamageReduction(),
            PowerStrike(),
            SecondWind()
        ])

    def reset(self):
        self.health = self.max_health


# ================== DUEL ==================

def simulate_duel(char1, char2):
    char1.reset()
    char2.reset()

    players = [char1, char2]
    random.shuffle(players)
    attacker, defender = players

    while char1.health > 0 and char2.health > 0:

        damage = attacker.attack_power - defender.defense_power
        damage = max(1, damage)

        damage = attacker.ability.modify_attack(attacker, defender, damage)
        damage = defender.ability.modify_defense(attacker, defender, damage)

        previous_health = defender.health
        defender.health -= damage

        defender.ability.after_damage(defender, previous_health)

        if defender.health <= 0:
            return attacker.name

        attacker, defender = defender, attacker


# ================== UI ==================

st.title("⚔️ Python Battle Arena")

st.write("Simulare de duel între două personaje cu abilități speciale.")

# ---- SINGLE DUEL ----
if st.button("Start Duel"):
    p1 = Character(1)
    p2 = Character(2)

    winner = simulate_duel(p1, p2)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(p1.name)
        st.write(f"Health: {p1.max_health}")   
        st.write(f"Attack: {p1.attack_power}")
        st.write(f"Defense: {p1.defense_power}")
        st.write(f"Ability: {p1.ability.__class__.__name__}")

    with col2:
        st.subheader(p2.name)
        st.write(f"Health: {p2.max_health}")   
        st.write(f"Attack: {p2.attack_power}")
        st.write(f"Defense: {p2.defense_power}")
        st.write(f"Ability: {p2.ability.__class__.__name__}")

    st.success(f"🏆 Winner: {winner}")


# ---- 1000 SIMULATIONS ----
if st.button("Run 1000 Simulations"):
    p1 = Character(1)
    p2 = Character(2)

    victories = {p1.name: 0, p2.name: 0}

    for _ in range(1000):
        winner = simulate_duel(p1, p2)
        victories[winner] += 1

    total = victories[p1.name] + victories[p2.name]

    st.subheader("Results after 1000 duels")

    st.write(f"{p1.name}: {victories[p1.name]} wins ({victories[p1.name]/total*100:.1f}%)")
    st.write(f"{p2.name}: {victories[p2.name]} wins ({victories[p2.name]/total*100:.1f}%)")

    st.bar_chart(victories)

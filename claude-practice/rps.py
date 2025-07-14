import random

def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def get_user_choice():
    while True:
        choice = input("Enter your choice (rock/paper/scissors) or 'quit' to exit: ").lower().strip()
        if choice in ['rock', 'paper', 'scissors', 'quit']:
            return choice
        print("Invalid choice. Please enter rock, paper, scissors, or quit.")

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return "user"
    else:
        return "computer"

def play_game():
    print("Welcome to Rock Paper Scissors!")
    print("=" * 30)
    
    user_score = 0
    computer_score = 0
    
    while True:
        user_choice = get_user_choice()
        
        if user_choice == 'quit':
            break
        
        computer_choice = get_computer_choice()
        
        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")
        
        winner = determine_winner(user_choice, computer_choice)
        
        if winner == "tie":
            print("It's a tie!")
        elif winner == "user":
            print("You win this round!")
            user_score += 1
        else:
            print("Computer wins this round!")
            computer_score += 1
        
        print(f"\nScore - You: {user_score}, Computer: {computer_score}")
        print("-" * 30)
    
    print(f"\nFinal Score - You: {user_score}, Computer: {computer_score}")
    
    if user_score > computer_score:
        print("Congratulations! You won overall!")
    elif computer_score > user_score:
        print("Computer wins overall! Better luck next time!")
    else:
        print("It's a tie overall!")
    
    print("Thanks for playing!")

if __name__ == "__main__":
    play_game()
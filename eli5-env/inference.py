import os
from models import ELI5Action
from server.environment import ELI5Environment

# If you want to use a real LLM later, you'd import OpenAI/Anthropic here
# For now, this script acts as a manual tester or a simple "Mock Agent"

def run_inference():
    # 1. Initialize the environment
    # In a real hackathon setup, you'd use ELI5Env(base_url="...") 
    # to connect to a running server, but we can test the logic directly:
    env = ELI5Environment()
    
    print("🚀 Starting ELI5 Inference Test...")
    print("-" * 30)

    # 2. Reset the environment to get the first task
    result = env.reset()
    concept = result["observation"]["concept"]
    print(f"Target Concept: {concept}")
    print(f"Initial Feedback: {result['observation']['feedback']}")

    done = False
    step_count = 0

    while not done:
        step_count += 1
        print(f"\n--- Step {step_count} ---")
        
        # 3. The "Agent" logic 
        # In the real hackathon, this is where you call Llama-3 or GPT-4
        # "Hey LLM, explain {concept} to a 5-year-old."
        
        user_input = input(f"Enter explanation for '{concept}': ")
        
        # 4. Wrap the response in your Action model
        action = {"explanation": user_input}
        
        # 5. Step the environment
        result = env.step(action)
        
        obs = result["observation"]
        done = result["done"]
        reward = result["reward"]

        print(f"Feedback: {obs['feedback']}")
        print(f"Current Score: {obs['score']}")
        
        if done:
            print("-" * 30)
            if reward >= 0.8:
                print(f"✅ SUCCESS! Final Reward: {reward}")
            else:
                print(f"❌ FAILED! Final Reward: {reward}")

if __name__ == "__main__":
    run_inference()
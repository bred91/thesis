from online_pipeline_models.pipeline_factory import get_chat_pipeline

HELP = " - \033[1;3m/exit\033[0m to exit \n - \033[1;3m/reset\033[0m to clear memory"

MODEL_CHOICES = ["simple", "multi_query", "chain_agent_react", "graph_agent_react_vanilla", "graph_agent_react"]

def interactive_cli(model_name: str):
    pipe = get_chat_pipeline(model_name)
    print(f"\n\n[{model_name}] ready \n{HELP}\n")
    while True:
        msg = input("\nYou: ")
        cmd = msg.strip().lower()
        if cmd == "/exit":
            print("Bye!")
            break
        if cmd == "/reset":
            pipe.reset()
            print("(memory cleared)")
            continue
        print("Assistant:", pipe.ask(msg))

def select_model():
    print("Select a model:")
    for idx, name in enumerate(MODEL_CHOICES, 1):
        print(f"{idx}. {name}")
    print("\n0. Exit\n")

    while True:
        choice = input("Enter the number of the model: ")
        if choice.isdigit() and 1 <= int(choice) <= len(MODEL_CHOICES):
            return MODEL_CHOICES[int(choice) - 1]
        elif choice == "0":
            print("Exiting...")
            exit(0)

        print("Invalid selection. Try again.")


def main():
    model = select_model()
    interactive_cli(model)

if __name__ == "__main__":
    main()
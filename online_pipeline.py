import argparse

from online_pipeline_models.pipeline_factory import get_chat_pipeline

HELP = """/exit to exit – /reset to clear memory"""

MODEL_CHOICES = ["simple", "multi_query", "chain_agent_react", "graph_agent_react"]

def interactive_cli(model_name: str):
    pipe = get_chat_pipeline(model_name)
    print(f"[{model_name}] ready. {HELP}\n")
    while True:
        msg = input("You: ")
        cmd = msg.strip().lower()
        if cmd == "/exit":
            print("Bye!")
            break
        if cmd == "/reset":
            pipe.reset()
            print("(memory cleared)")
            continue
        print("Assistant:", pipe.ask(msg))


def run_pipeline(model_name: str, user_message: str, new_session=False):
    if new_session:
        pipe = get_chat_pipeline(model_name)
    else:
        if not hasattr(run_pipeline, "cache"):
            run_pipeline.cache = {}
        pipe = run_pipeline.cache.setdefault(model_name, get_chat_pipeline(model_name))
    return pipe.ask(user_message)


def main():
    ap = argparse.ArgumentParser(description="Multi Model Chat Pipeline CLI")
    ap.add_argument("--model", required=True, choices=MODEL_CHOICES)
    args = ap.parse_args()
    interactive_cli(args.model)

if __name__ == "__main__":
    main()
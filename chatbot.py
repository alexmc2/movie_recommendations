import argparse

import openai
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]


def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    return bold_start + text + bold_end


def blue(text):
    blue_start = "\033[34m"
    blue_end = "\033[0m"
    return blue_start + text + blue_end


def red(text):
    red_start = "\033[31m"
    red_end = "\033[0m"
    return red_start + text + red_end


def main():
    parser = argparse.ArgumentParser(
        description="Simple command line chatbot with GPT-4"
    )

    parser.add_argument(
        "--personality",
        type=str,
        help="A brief summary of the chatbot's personality",
        default="friendly and helpful",
    )
    args = parser.parse_args()

    initial_prompt = (
        f"You are a conversational chatbot. Your personality is: {args.personality}"
    )
    messages = [{"role": "system", "content": initial_prompt}]

    while True:
        try:
            user_msg = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_msg})

            streamed_responses = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages, stream=True
            )

            # loop through streamed responses
            for res in streamed_responses:
                chunk = res["choices"][0]["delta"]
                if "role" in chunk and "content" in chunk:
                    messages.append(chunk)

                # print each chunk as it's received
                if "content" in res["choices"][0]["delta"]:
                    print(res["choices"][0]["delta"]["content"], end="", flush=True)

            print()  # newline

        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()

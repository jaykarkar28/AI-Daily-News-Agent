from config.settings import GROQ_API_KEYS


print(
    f"Number of Groq keys loaded: "
    f"{len(GROQ_API_KEYS)}"
)

for index, key in enumerate(
    GROQ_API_KEYS,
    start=1,
):
    print(
        f"Key {index} loaded: "
        f"{bool(key)}"
    )
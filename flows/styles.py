from prompt_toolkit.styles import Style


style = Style.from_dict(
    {
        # Default style.
        # "": "#ff0066",
        # Prompt.
        "highlighted-text": "#006400 bold",
        "selected-text": "reverse underline",
    }
)

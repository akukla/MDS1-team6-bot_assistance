from prompt_toolkit.styles import Style


style = Style.from_dict(
    {
        # Default style.
        # "": "#ff0066",
        # Prompt.
        "highlighted-text": "#006400 bold",
        # Make a selection reverse/underlined.
        # (Use Control-Space to select.)
        "selected-text": "reverse underline",
    }
)

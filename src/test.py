def str_to_ascii(s: str) -> str:
    """
    Function converts string to ascii characters

    :param s: String to convert
    :return: Converted string
    """

    return "".join(i if ord(i) < 128 else "?" for i in s)


print(
    str_to_ascii(
        "𝚐𝚊𝚕𝚊𝚝 𝚔𝚢𝚊 𝚜𝚊𝚑𝚒 𝚔𝚢𝚊 𝚖𝚞𝚓𝚑𝚎 𝚗𝚊 𝚙𝚊𝚝𝚊 𝚑𝚊𝚒 𝚜𝚝𝚊𝚝𝚞𝚜 || 𝚊𝚗𝚒𝚖𝚊𝚕 || 🥀𝚜𝚝𝚊𝚝𝚞𝚜518 || 𝚑𝚎𝚊𝚛𝚝 𝚝𝚘𝚞𝚌𝚑𝚒𝚗𝚐 𝚜𝚝𝚊𝚝𝚞𝚜 || 🥀🤞🌎"
    )
)

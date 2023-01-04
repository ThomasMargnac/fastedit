def rgb_to_bgr(
    hexa
):
    # Getting length
    hexa_len = len(hexa)
    if hexa_len == 7:
        final = "&H" + hexa[5:7] + hexa[3:5] + hexa[1:3]
        return final
    elif hexa_len == 9:
        final = "&H" + hexa[7:9] + hexa[5:7] + hexa[5:7] + hexa[3:5]
        return final
    else:
        raise ValueError("Hexadecimal color code is incorect")
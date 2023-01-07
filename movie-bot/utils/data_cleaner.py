def is_num(st: str) -> bool:
    try:
        int(st)
        return True
    except Exception:
        return False


def clean_inp(st: str) -> str:
    try:
        sp_chars = ["?", "!", ".", ","]
        for e in sp_chars:
            if e in st:
                st.replace(e, "")
        return st.lower()
    except Exception:
        return st

from datetime import datetime

def unique_customer() -> dict[str, str]:
    stamp = datetime.utcnow().strftime("%H%M%S%f")
    return {
        "first_name": f"Auto{stamp[-6:]}",
        "last_name": f"User{stamp[-4:]}",
        "post_code": stamp[-6:],
    }


def full_name(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name}"

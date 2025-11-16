import uuid


def get_authorization_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def get_image(name: str) -> tuple:
    image_content = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\x0f'
        b'\x00\x01\x01\x01\x00\x18\xdd\x8b\xf0\x00\x00\x00\x00IEND\xaeB`\x82'
    )

    return f"{str(uuid.uuid4())}-{name}.png", image_content, "image/png"

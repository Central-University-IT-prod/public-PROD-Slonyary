def authorize_url() -> str:
    client_id_admin = 6121396
    redirect_uri = "https://oauth.vk.com/blank.html"
    display = "popup"
    response_type = "token"
    scope = 8192 + 65536 + 262144

    return (
        f"https://oauth.vk.com/authorize"
        f"?client_id={client_id_admin}"
        f"&scope={scope}"
        f"&redirect_uri={redirect_uri}"
        f"&display={display}"
        f"&response_type={response_type}"
        f"&revoke=1"
    )

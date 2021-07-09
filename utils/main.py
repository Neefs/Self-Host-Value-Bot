import mystbin

async def post_code(code, lang=None) -> str:
    if not lang:
        lang='python'
    client = mystbin.Client()
    return await client.post(code, lang)
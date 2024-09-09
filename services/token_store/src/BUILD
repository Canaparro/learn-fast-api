python_sources(
    dependencies=[
        "services/token_store:poetry_token_store",
    ],
)

pex_binary(
    name="runnable_token_store",
    entry_point="app.py",
    output_path="token_store.pex",
)

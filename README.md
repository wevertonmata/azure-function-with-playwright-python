# Playwright in Python Azure Functions

1. Ensure `playwright` is in requirements.txt.

1. Deploy to Azure Functions v4 consumption plan using remote build (this is the default).

1. The app won't work because chromium is not installed. Add 2 app settings:
    - `PLAYWRIGHT_BROWSERS_PATH`: `/home/site/wwwroot`
        - This tells Playwright to install and use chromium from `/home/site/wwwroot`
    - `POST_BUILD_COMMAND`: `PYTHONPATH=/tmp/zipdeploy/extracted/.python_packages/lib/site-packages /tmp/oryx/platforms/python/3.10/bin/python3.10 -m playwright install chromium`
        - This is hacky and brittle because the Python version is bound to change. But it works for now. What this does is to run `playwright install chromium` in the Python version that was used to build the app. It'll install it to `/home/site/wwwroot` because of the previous app setting0.

1. Deploy again, this time the post build command will run and hopefully it works."# azure-function-with-playwright-python" 


### Reference links

[YAML Python Function](https://github.com/Azure/actions-workflow-samples/blob/master/FunctionApp/linux-python-functionapp-on-azure.yml)

[Entrega contínua usando GitHub Actions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions?tabs=linux%2Cpython&pivots=method-template#prerequisites)

[Usando segredos em GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions?tool=webui)

[Unable to install Playwright on an Azure Function using Python](https://stackoverflow.com/questions/76314433/unable-to-install-playwright-on-an-azure-function-using-python)
# GirlsDay 2026 – Setup Guide

The setup script requires a Windows machine. In principle, everything we built also works on Linux or macOS – there is just no automated setup for those platforms. The script installs **Visual Studio Code** and **Python**, and downloads the source files from [https://github.com/bluehands/GirlsDay2026](https://github.com/bluehands/GirlsDay2026) to `C:\GirlsDay2026`.

## Windows (Automatic Setup)

- You need someone with administrator rights on your machine. Open a terminal as administrator: press the Windows key, type **Terminal**, right-click it and select **Run as administrator**.

- Paste the following command:
  ```powershell
  irm https://raw.githubusercontent.com/bluehands/GirlsDay2026/main/setup.ps1 | iex
  ```

- If the script stops and says something about PowerShell 7, you need to install it first. Open the **Microsoft Store**, search for **PowerShell**, install it, then start over.

- During installation you will be asked for API keys for **OpenAI** and **Serper**:

  - **OpenAI** – Create an account at [platform.openai.com/login](https://platform.openai.com/login). You can then create an API key which, at least in our experience, works for a number of requests even without adding credit. You need an OpenAI key for all samples. During the entire GirlsDay including preparation we spent just under $3 with the configured models, so you can get quite far with a small amount of credit.

  - **Serper** – This is the Google Search API and you only need it for Sample 2. You can create a free account and get 2,500 free requests at [serper.dev](https://serper.dev/).

- Open **Visual Studio Code** and use **Open Folder** to open `C:\GirlsDay2026`. In the file explorer on the left you will find the file **crewai_samples.ipynb** – open it and you are right where the GirlsDay started. If Visual Studio Code wants to install extensions, go ahead and do that.

- You are now on the version with the TODOs. If you want to see the solutions – including the image generation feature we added spontaneously – click on **main** in the very bottom-left corner of Visual Studio Code, then select **imageGeneration** from the list at the top. After switching branches, close the notebook **crewai_samples.ipynb** and reopen it.

Have fun! 🎉

## macOS / Linux (Manual Setup)

Please install the following tools manually:

- [Python 3.11+](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/)

Then clone the repository and install the dependencies:

```bash
git clone https://github.com/bluehands/GirlsDay2026
cd GirlsDay2026
pip install -r requirements.txt
```

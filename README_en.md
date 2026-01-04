

# Cursor-Token-Saver-and-Optimizer

[Youtube Video Demo](https://www.google.com/search?q=placeholder-link) | [中文版本](https://github.com/Bob8259/Cursor-Token-Saver-and-Optimizer)

**Cursor-Token-Saver-and-Optimizer** is a middleware solution designed for developers who want full control over their Cursor AI experience.

Cursor is designed to be accessible for beginners, which often results in "bloated" system prompts that consume unnecessary tokens. Furthermore, Cursor's default system prompts restrict certain CLI commands (like `echo` or `cat`) and can encounter formatting issues with specific models like Gemini. This project gives you **full control** over the prompt, allowing for cleaner prompts, custom rules, and up to **50% token savings**.
### 🌟 Key Features

* **Token Optimization:** Strips redundant system prompts to save costs and reduce latency.
* **Command Liberation:** Removes restrictions on system-level commands like `echo` or `cat`.
* **Model Compatibility:** Fixes escape character handling issues, making models like **Gemini** and **Grok** fully compatible with Cursor.
* **Usage Monitoring:** A built-in dashboard to track token consumption per model.
---
## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Bob8259/Cursor-Token-Saver-and-Optimizer.git
cd Cursor-Token-Saver-and-Optimizer

```

### 2. Environment Setup

It is recommended to use **Conda** for environment management:

```bash
conda create -n CursorTokenSaver python=3.12
conda activate CursorTokenSaver
pip install -r requirements.txt

```

### 3. Run the Proxy

```bash
python forward.py

```

### 4. Deployment

To use this with the Cursor Desktop client, the proxy must be accessible via HTTPS:

* **Option A (Server):** Deploy to a VPS with a domain and SSL.
* **Option B (Recommended):** Use [ngrok](https://ngrok.com/) or a similar NAT traversal tool to generate a public URL.

### 5. Configure Cursor

1. Open Cursor Settings.
2. Navigate to **Models** > **OpenAI API Key** (or the relevant provider).
3. Override the **Base URL** with your new domain (e.g., `https://your-domain.com/v1`).

---

## 📊 Usage Monitor

You can monitor your real-time token usage and model performance via the web dashboard.

* **Local:** `http://localhost:5000`
* **Remote:** `https://your-domain.com`

---

## 🧪 Testing Performance

I have included a `test_prompt.txt` in the repository to benchmark the performance.

1. Visit `http://localhost:5000/test` to view the test commands.
2. Run the commands in Cursor to compare performance and token usage.
3. **Note:** Ensure you remove `templates/answer.html` before testing to prevent the model from "cheating" by reading existing results.
4. The answer is written by Gemini-3-pro-preview
---
## 📊 Performance & Cost Comparison

The following table demonstrates the optimization results across different models. By intercepting and refining the prompts, you can achieve an average cost reduction of **49%**. To provide a clear baseline, all costs below are calculated using a unified pricing standard: $0.50 per 1M Input Tokens and $3.00 per 1M Output Tokens.

| Model | My Cost ($) | My Input Tokens | My Output Tokens | My Time (s) | Cursor Cost ($) | Cursor Input Tokens | Cursor Output Tokens | Cursor Time (s) | Cost Savings | Input Token Savings | Output Token Savings | Time Savings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini-3-Flash-Preview | 0.193 | 39,378 | 5,023 | 69.93 | 0.436 | 118,490 | 5,360 | 81.33 | **55.6%** | 66.8% | 6.3% | 14.0% |
| Gemini-3-Pro-Preview | 0.384 | 59,887 | 13,607 | 214.21 | 0.854 | 209,500 | 15,008 | 227.33 | **55.0%** | 71.4% | 9.3% | 5.8% |
| Claude-Opus-4.5* | 0.190 | 35,572 | 5,560 | 86.41 | 0.412 | 104,542 | 6,568 | 108.46 | **53.9%** | 66.0% | 15.3% | 20.3% |
| Claude-Sonnet-4.5* | 0.190 | 35,572 | 5,560 | 86.41 | 0.285 | 69,587 | 5,057 | 81.47 | **33.2%** | 48.9% | -9.9% | -6.1% |
| **Average** | - | - | - | - | - | - | - | - | **49.0%** | **63.3%** | **5.3%** | **8.5%** |

---
## ⚠️ Important Notices

* **Agent Mode Only:** This tool is strictly optimized for **Agent** mode **ONLY**. Using it in other modes may cause unexpected behavior.
* **Model Recommendations:** 
* *Best:* Claude models.
* *Good:* Gemini / Grok models.
* *Avoid:* GPT models (often struggles with using tools).
* **Customization:** Cursor may behave slightly differently than the "official" version because the system prompt has been modified. You can adjust these settings in the source code to fit your personal coding style.
* **Model Inconsistency:** LLM outputs are probabilistic. You may not see the exact same token savings or performance results on every run. Please try to run tests multiple times and calculate the average to get an accurate representation of the optimization.



### 🤝 Contributing

Feel free to open issues or submit pull requests if you find ways to further optimize the prompts or support more models!


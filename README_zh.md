
# Cursor-Token-Saver-and-Optimizer 
[Youtube 视频演示](https://www.google.com/search?q=placeholder-link) | [English Version](https://www.google.com/search?q=placeholder-link)

**Cursor-Token-Saver-and-Optimizer** 是一个专为希望完全掌控 Cursor AI 体验的开发者设计的中间件解决方案。

Cursor 的设计初衷是照顾初学者，这往往导致其系统提示词（System Prompts）过于“臃肿”，消耗了不必要的 Token。此外，Cursor 默认的系统提示词限制了某些 CLI 命令（如 `echo` 或 `cat`），并且在与 Gemini 等特定模型配合时可能会遇到转义符格式化问题。本项目让你拥有对提示词的**完全控制权**，实现更精简的提示词、自定义规则，并最高可**节省 50% 的 Token 消耗**。

### 🌟 核心特性

* **Token 优化：** 剔除冗余的系统提示词，降低成本并减少延迟。
* **命令释放：** 解除对 `echo` 或 `cat` 等系统级命令的限制。
* **模型兼容性：** 修复了转义字符处理问题，使 **Gemini** 和 **Grok** 等模型能与 Cursor 完美兼容。
* **用量监控：** 内置仪表盘，用于追踪每个模型的 Token 消耗情况。

---

## 🛠️ 安装与设置

### 1. 克隆仓库

```bash
git clone https://github.com/Bob8259/Cursor-Token-Saver-and-Optimizer.git
cd Cursor-Token-Saver-and-Optimizer

```

### 2. 环境配置

建议使用 **Conda** 进行环境管理：

```bash
conda create -n CursorTokenSaver python=3.12
conda activate CursorTokenSaver
pip install -r requirements.txt

```

### 3. 运行代理服务

```bash
python forward.py

```

### 4. 部署

若要在 Cursor 桌面客户端中使用，代理服务必须通过 HTTPS 访问：

* **选项 A（服务器）：** 部署到拥有域名和 SSL 证书的 VPS 上。
* **选项 B（推荐）：** 使用 [ngrok](https://ngrok.com/) 或类似的内网穿透工具生成公网 URL。

### 5. 配置 Cursor

1. 打开 Cursor 设置（Settings）。
2. 导航至 **Models** > **OpenAI API Key**（或相关的提供商）。
3. 将 **Base URL** 修改为你的新域名（例如：`https://your-domain.com/v1`）。

---

## 📊 用量监控

你可以通过 Web 仪表盘实时监控 Token 使用情况和模型性能。

* **本地地址：** `http://localhost:5000`
* **远程地址：** `https://your-domain.com`

---

## 🧪 性能测试

仓库中包含了一个 `test_prompt.txt` 文件用于性能基准测试。

1. 访问 `http://localhost:5000/test` 查看测试命令。
2. 在 Cursor 中运行这些命令，对比性能和 Token 使用情况。
3. **注意：** 测试前请确保删除 `templates/answer.html`，以防止模型通过读取现有结果来“作弊”。

---

## ⚠️ 重要提示

* **仅限 Agent 模式：** 此工具**仅**针对 **Agent** 模式进行了严格优化。在其他模式下使用可能会导致不可预知的行为。
* **模型推荐：** 
* *最佳：* Claude 系列模型。
* *良好：* Gemini / Grok 系列模型。
* *不佳：* GPT 系列模型（通常在调用工具方面表现不佳）。
* **自定义化：** 由于系统提示词已被修改，Cursor 的表现可能与“官方”版本略有不同。你可以根据自己的编程习惯在源码中调整这些设置。
* **模型不确定性：** LLM 的输出具有概率性。你可能不会在每次运行时都看到完全相同的 Token 节省量或结果。请尝试多次运行测试并计算平均值，以获得准确的优化参考。

### 🤝 参与贡献

如果你发现了进一步优化提示词或支持更多模型的方法，欢迎提交 Issue 或 Pull Request！

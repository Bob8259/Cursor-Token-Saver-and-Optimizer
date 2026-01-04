import os
import json
import requests
import datetime
import glob
import time
from flask import Flask, request, Response, stream_with_context, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
# Added a check to prevent the TypeError you saw earlier
BASE_URL = os.getenv("BASE_URL")
if BASE_URL is None:
    raise ValueError("TARGET_URL not found in .env file")
TARGET_URL = BASE_URL + "/chat/completions"

NEW_TOOLS_FILE = "optimized_tools_new.json"
OLD_TOOLS_FILE = "optimized_tools_old.json"

app = Flask(__name__)

def log_transaction(request_body, raw_chunks, start_time, end_time):
    """Saves the request and all raw chunks received from the model."""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp_str = datetime.datetime.fromtimestamp(start_time).strftime("%Y%m%d-%H%M%S")
    filepath = os.path.join("logs", f"log_{timestamp_str}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            {
                "start_time": datetime.datetime.fromtimestamp(start_time).isoformat(),
                "end_time": datetime.datetime.fromtimestamp(end_time).isoformat(),
                "start_time_raw": start_time,
                "end_time_raw": end_time,
                "request_body": request_body,
                "raw_chunks": raw_chunks  # This stores the exact data received
            },
            f,
            indent=4,
            ensure_ascii=False
        )

def get_optimized_tools(tools_file):
    try:
        print("Tools file version: ", tools_file)
        if tools_file == "new":
            with open(NEW_TOOLS_FILE, "r", encoding="utf-8") as f:
                content = json.load(f)
                return content.get("tools", content) if isinstance(content, dict) else content
        elif tools_file == "old":
            with open(OLD_TOOLS_FILE, "r", encoding="utf-8") as f:
                content = json.load(f)
                return content.get("tools", content) if isinstance(content, dict) else content
    except FileNotFoundError:
        return None

@app.route("/")
def index():
    log_files = glob.glob("logs/log_*.json")
    log_files.sort(reverse=True)
    
    usage_history = []
    for filepath in log_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                log_data = json.load(f)
                
            filename = os.path.basename(filepath)
            start_time = log_data.get("start_time", "")
            end_time = log_data.get("end_time", "")
            request_body = log_data.get("request_body", {})
            model = request_body.get("model", "unknown")
            
            # Extract usage from raw_chunks
            usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            raw_chunks = log_data.get("raw_chunks", [])
            for chunk in reversed(raw_chunks):
                if chunk.startswith("data: ") and not chunk.strip() == "data: [DONE]":
                    try:
                        chunk_json = json.loads(chunk[6:])
                        if "usage" in chunk_json and chunk_json["usage"]:
                            usage = chunk_json["usage"]
                            break
                    except:
                        continue
            
            # Use raw times for duration if available, else try to parse ISO strings
            start_raw = log_data.get("start_time_raw")
            end_raw = log_data.get("end_time_raw")
            
            if start_raw and end_raw:
                duration = round(end_raw - start_raw, 2)
            else:
                # Fallback for old logs or if raw times are missing
                try:
                    s = datetime.datetime.fromisoformat(start_time)
                    e = datetime.datetime.fromisoformat(end_time)
                    duration = round((e - s).total_seconds(), 2)
                except:
                    duration = 0

            usage_history.append({
                "filename": filename,
                "start_time": start_time,
                "end_time": end_time,
                "model": model,
                "input": usage.get("prompt_tokens") or usage.get("input_tokens") or 0,
                "output": usage.get("completion_tokens") or usage.get("output_tokens") or 0,
                "total": usage.get("total_tokens") or (usage.get("input_tokens", 0) + usage.get("output_tokens", 0)) or 0,
                "duration": duration
            })
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")

    return render_template("index.html", history=usage_history)
    
@app.route("/test")
def test_page():
    # Complex logic to demonstrate coding ability
    import math
    import random
    
    # Generate some synthetic data for a complex visualization
    data_points = []
    for i in range(100):
        x = i / 10.0
        # A complex wave function
        y = math.sin(x) * math.cos(x * 0.5) + math.log(x + 1) * 0.5 + random.uniform(-0.1, 0.1)
        data_points.append({"x": round(x, 2), "y": round(y, 4)})
        
    # Some recursive calculation
    def fibonacci(n):
        if n <= 1: return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    fib_sequence = [fibonacci(i) for i in range(10)]
    
    return render_template("test.html", 
                           data_points=data_points, 
                           fib_sequence=fib_sequence,
                           server_time=datetime.datetime.now().isoformat())

@app.route("/answer")
def answer_page():
    # Complex logic to demonstrate coding ability
    import math
    import random
    
    # Generate some synthetic data for a complex visualization
    data_points = []
    for i in range(100):
        x = i / 10.0
        # A complex wave function
        y = math.sin(x) * math.cos(x * 0.5) + math.log(x + 1) * 0.5 + random.uniform(-0.1, 0.1)
        data_points.append({"x": round(x, 2), "y": round(y, 4)})
        
    # Some recursive calculation
    def fibonacci(n):
        if n <= 1: return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    fib_sequence = [fibonacci(i) for i in range(10)]
    
    return render_template("answer.html", 
                           data_points=data_points, 
                           fib_sequence=fib_sequence,
                           server_time=datetime.datetime.now().isoformat())

@app.route("/log/<filename>")
def get_log_detail(filename):
    filepath = os.path.join("logs", filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    
    with open(filepath, "r", encoding="utf-8") as f:
        log_data = json.load(f)
    
    request_messages = log_data.get("request_body", {}).get("messages", [])
    
    # Reconstruct response content from chunks
    response_content = ""
    for chunk in log_data.get("raw_chunks", []):
        if chunk.startswith("data: ") and not chunk.strip() == "data: [DONE]":
            try:
                chunk_json = json.loads(chunk[6:])
                choices = chunk_json.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {})
                    if "content" in delta and delta["content"]:
                        response_content += delta["content"]
            except:
                continue
                
    return jsonify({
        "request_messages": request_messages,
        "response_content": response_content
    })

@app.route("/v1/chat/completions", methods=["POST"])
def proxy_chat():
    data = request.json
    messages = data.get("messages", [])
    print(f"Debug: Received a request to /v1/chat/completions with {len(messages)} messages")

    if not messages:
        return {"error": "No messages provided"}, 400

    # 1. System Prompt & Cleaning logic (Kept from your original)
    for msg in messages:
        if msg.get("role") == "system":
            msg["content"] = (
                """
                You are an AI Coding Assistant. Follow `<user_query>` strictly.
                Read only one file (if needed) per turn. Use only ONE tool call per turn. No parallel tool usage. 
                Use dedicated tools first. Use Shell only if no other tool can fulfill the requirement.
                Always use paths with forward slashes (e.g., `d:/Folder/test.py`).
                Aim to keep files under 600 lines; create new files for overflow if necessary.

                ### CRITICAL TOOL CALL ESCAPING:
                The 'Read' tool shows code after one layer of decoding. 'StrReplace' requires arguments to be double-encoded. 
                Follow this mapping strictly:
                1. ACTUAL NEWLINE: If you see a physical line break in 'Read', use 4 backslashes ("\\\\n") in 'StrReplace'.
                2. LITERAL "\\n": If you see 4 backslashes ("\\n") in 'Read', you MUST use 8 backslashes ("\\\\\\\\n") in 'StrReplace'.
                3. Always DOUBLE the number of backslashes you see in the 'Read' output when writing the 'StrReplace' arguments. Using 8 backslashes with an 'n' in the JSON is interpreted as a backslash followed by 'n'. Meanwhile, 4 backslashes with an 'n' in the JSON represents a newline character.
                """
            )
            break

    if len(messages) > 1:
        messages.pop(1)

    # 2. Swap Tools
    # Normalize the data: ensure we are working with a list
    tools_to_check = []
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass

    if isinstance(data, list):
        tools_to_check = data
    elif isinstance(data, dict):
        # If the data is a dict, it might have a 'tools' or 'functions' key
        tools_to_check = data.get("tools", data.get("functions", []))

    # Robust check for the function name
    has_terminal_cmd = any(
        isinstance(tool, dict) and tool.get("function", {}).get("name") == "search_replace"
        for tool in tools_to_check
    )

    # Call the appropriate optimizer
    optimized_tools = get_optimized_tools("old" if has_terminal_cmd else "new")
    if optimized_tools is not None:
        data["tools"] = optimized_tools

    # 3. SETTINGS FOR TOKEN TRACKING
    data["stream"] = True
    data["temperature"] = 0.5
    data["model"] = "claude-sonnet-4-5-20250929-thinking" #Change the model if needed
    data["stream_options"] = {"include_usage": True}

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    def generate():
        max_retries = 10
        retry_count = 0
        start_time = time.time()
        
        while retry_count < max_retries:
            try:
                print(f"Debug: Attempt {retry_count + 1} to start streaming from {TARGET_URL}...")
                # timeout=30 here applies to both connection and read (silence between chunks)
                response = requests.post(TARGET_URL, headers=headers, json=data, stream=True, timeout=30)
                response.raise_for_status()

                captured_chunks = []
                chunk_count = 0

                # response.iter_lines() will raise requests.exceptions.Timeout if 30s passes without data
                for chunk in response.iter_lines():
                    if not chunk:
                        continue

                    decoded_chunk = chunk.decode("utf-8")
                    yield decoded_chunk + "\n"

                    # Store the raw chunk string (e.g., "data: {...}")
                    captured_chunks.append(decoded_chunk)
                    chunk_count += 1
                    
                    if chunk_count % 10 == 0:
                        print(f"Debug: Sent {chunk_count} chunks...")

                    # Check for the end of the stream to trigger logging
                    if "data: [DONE]" in decoded_chunk:
                        end_time = time.time()
                        print(f"Debug: Streaming finished. Total chunks: {chunk_count}")
                        log_transaction(data, captured_chunks, start_time, end_time)
                        return

                # If the loop finishes without [DONE], it might be an incomplete stream
                raise Exception("Stream ended unexpectedly without [DONE]")

            except Exception as e:
                retry_count += 1
                print(f"Error: Attempt {retry_count}/{max_retries} failed: {e}")
                if retry_count >= max_retries:
                    error_msg = f"Failed after {max_retries} attempts: {str(e)}"
                    yield f'data: {{"error": "{error_msg}"}}\n\ndata: [DONE]\n'
                    return
                time.sleep(1)

    return Response(stream_with_context(generate()), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(port=5000)
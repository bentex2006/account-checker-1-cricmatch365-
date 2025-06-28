# 🛠 How CricMatch Checker Works

This explains **how my tool works step by step** for my own learning and for others.

---

## 1. CSRF Token Extraction

- First, it visits the homepage of CricMatch365 to extract the CSRF token.
- Uses regex to parse the token from HTML meta tags or hidden input fields.
- This token is needed to **bypass security and authenticate requests**.

---

## 2. Login

- Uses a POST request to send username and password with the CSRF token.
- Checks the response for success or failure patterns in JSON or HTML.

---

## 3. Fetch Balance

- If login is successful, sends another POST request to the `getBalance` API endpoint.
- Cleans up the returned balance string to ensure it is numeric and valid.

---

## 4. Multithreading

- Uses Python’s `ThreadPoolExecutor` to check multiple accounts simultaneously.
- Updates stats live in the console.

---

## 5. Saving Results

- All successful hits are saved to a timestamped file with user:pass and balance.

---

## 🚀 **Why I built this**

I wanted to learn:

- How websites use tokens for protection
- How APIs return data in JSON format
- How to use multithreading for faster results
- How to structure a real Python project

---

### 💡 **What I can improve next**

- Using config.json dynamically
- Adding proxy support
- Better error handling and retry logic
- Making it into a CLI tool with `argparse`

---

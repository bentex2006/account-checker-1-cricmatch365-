


<div align="center">

# 🎯 CricMatch365 Account Checker  [edu]

<img src="https://raw.githubusercontent.com/bentex2006/cricmatch-checker/main/docs/images/banner.png" alt="Project Banner" width="80%"/>

A **multithreaded Python tool** to check CricMatch365 accounts, log in, and fetch balances efficiently.

</div>

---

## ✨ Features

✅ CSRF token extraction  
✅ Secure login and session handling  
✅ Fetch account balance from API  
✅ Multi-threaded for fast combo processing  
✅ Colorful and clean CLI output  
✅ Saves successful hits to a separate file

---


## ⚠️ Disclaimer

🔴 **For educational purposes only.**  
Use responsibly and ethically under your local laws.  
The author is not responsible for any misuse.

---

## 🛠 Installation

1. **Clone the repository**

```bash
git clone https://github.com/bentex2006/account-checker#1(cricmatch365).git
cd cricmatch-checker
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Prepare your **combo file** in `username:password` format, one per line.
2. Run:

```bash
python main.py
```

3. Enter the requested inputs:

* Combo file name (e.g. `combos.txt`)
* Number of threads (e.g. `100`)

4. **Results**

* Successful logins with balances are saved in a file named like `success_xxxxxx.txt`.

---

## ⚙️ Configuration

Edit `config.json` to modify:

```json
{
  "base_url": "https://cricmatch365.com",
  "timeout": 10,
  "max_threads": 400
}
```

*(currently used as a placeholder for future dynamic configs)*

---

## 🧠 Learning Outcomes

✔️ Understanding CSRF token usage
✔️ API POST requests with sessions
✔️ Regex parsing for HTML and JSON
✔️ Multi-threading with ThreadPoolExecutor
✔️ Clean code and project structuring for GitHub

---

## 👤 Author

<div align="center">

**Skittle (b3nt3x)**
Learning Python, automation, and cybersecurity.
Telegram: [@cracker666user](linktr.ee/mrbentex)

</div>

---

## 📄 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

---

## ⭐ Support

If you find this project useful for your learning journey, give it a ⭐ on GitHub to motivate continued public educational releases.

---

```

---


### ✅ **Done.**

Let me know if you want:
  
- This README converted to your GitHub Pages site  
- A pinned repository message for your profile to showcase professionalism
```
# account-checker-1-cricmatch365-

# 🔎 Advanced OSINT

**Advanced OSINT** is a Python-based Open Source Intelligence (OSINT) tool designed to collect and analyze publicly available information related to a target domain.

The tool performs **multi-source OSINT reconnaissance** to discover publicly exposed email addresses, usernames, website information, documents, and other domain-related intelligence while maintaining **source attribution** for discovered results.

The project is inspired by the concept of tools such as **theHarvester**, with a focus on combining multiple OSINT sources into a single automated and easy-to-use tool.

---

## 🚀 Features

* 🔍 Multi-source OSINT scanning
* 📧 Email address discovery
* 👤 Username discovery
* 🌐 Website reconnaissance
* 📄 PDF/document scanning
* ⚡ Threaded/concurrent scanning for faster results
* 🔎 Search engine-based reconnaissance
* 🕵️ GitHub-based information gathering

---

## 🛰️ Supported OSINT Sources

The project contains separate modules for different information sources:

| Source          | Purpose                                          |
| --------------- | ------------------------------------------------ |
| Bing            | Search-engine based OSINT                        |
| GitHub          | Public repositories and account information      |
| Hunter          | Email discovery                                  |
| IntelX          | Intelligence and data discovery                  |
| LinkedIn        | Public professional information                  |
| Common Crawl    | Historical web data                              |
| crt.sh          | Certificate Transparency information             |
| Wayback Machine | Historical website information                   |
| Website Scanner | Domain website analysis                          |
| PDF Scanner     | Information extraction from public PDF documents |

Additional sources can be integrated through the modular `sources/` architecture.

---

## 📋 Requirements

* Python 3.x
* Required Python packages
* API credentials for sources that require authentication

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/AqsaIftikhar88/Advnace-OSINT.git
```

### 2. Navigate to the project directory

```bash
cd Advnace-OSINT
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

To scan a target domain using all available sources:

```bash
python main.py --domain example.com --all
```

Replace `example.com` with the domain you are authorized to investigate.

---

## 📊 Example Output

<img width="1209" height="874" alt="image" src="https://github.com/user-attachments/assets/49cdb1d3-fc9a-4233-af9b-2bc095c2fb79" />

<img width="1081" height="477" alt="image" src="https://github.com/user-attachments/assets/77ba9e31-636b-44dc-b2fe-e7040e187a12" />

```

The tool associates discovered information with its corresponding source to make the results easier to analyze.

---

## 🧩 Modular Architecture

Each OSINT source is implemented as an independent Python module inside the `sources/` directory.

This makes the project easier to:

* Add new OSINT sources
* Modify individual scanners
* Debug source-specific issues
* Maintain the project
* Extend the tool with additional intelligence capabilities

---

## ⚡ Performance

The tool supports **concurrent/threaded scanning**, allowing multiple OSINT sources to be processed without waiting for every source to complete sequentially.

This improves scanning efficiency when multiple sources are being queried.

---

## 🔐 Ethical & Legal Use

This project is developed for:

* Cybersecurity education
* Authorized penetration testing
* Security research
* OSINT investigations
* Reconnaissance of systems you are authorized to assess

**Only use this tool against domains, organizations, and resources where you have explicit permission or where the information is intended to be publicly researched.**

The developer is not responsible for misuse of this tool.

---

## 👩‍💻 Author

**Engr. Aqsa Iftikhar**

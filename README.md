<div align="center">

# 🚀 JobSender Pro v2.7
### The Ultimate Corporate Email Automation Suite

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-000000?style=for-the-badge&logo=flask&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)

<p align="center">
  <strong>Streamline your job application process with enterprise-grade email automation.</strong><br>
  Built for speed, security, and high deliverability.
</p>

[View Projects](https://jobsender.vercel.app) · [Report Bug](https://github.com/oziy-id/mail-toolsV2/issues) · [Request Feature](https://github.com/oziy-id/mail-toolsV2/issues)

</div>


---

## 📝 About The Project

**JobSender Pro** is a sophisticated full-stack web application designed to revolutionize how professionals apply for jobs. Unlike standard email clients, JobSender Pro is engineered to send **high-priority, corporate-formatted emails** to multiple HR departments simultaneously while maintaining a personalized touch.

It solves the problem of repetitive manual emailing by automating the attachment handling, subject line formatting, and SMTP handshakes, ensuring your application lands in the "Priority" inbox, not spam.

---

## ✨ Key Features

### 🚀 Core Functionality
* **Multi-Target Dispatch Engine**: Send customized applications to 3 different companies in a single execution cycle.
* **Dynamic Role Injection**: Specify different job titles for each target company (e.g., *Frontend Dev* for Company A, *Fullstack* for Company B).
* **Smart PDF Validation**: Integrated client-side and server-side validation to ensure only PDF documents are transmitted (Auto-rejects JPG, DOCX, etc.).

### 🛡️ Security & Privacy
* **Stateless Architecture**: Zero-persistence data handling. Your files and personal data strictly exist in volatile memory (RAM) during transit and are instantly purged post-transmission.
* **TLS 1.3 Encryption**: All SMTP communications are secured with industry-standard Transport Layer Security.

### 📧 Email Deliverability
* **Anti-Spam Headers**: Automatically injects `X-Priority: 1` and `Importance: High` headers.
* **Multipart/Alternative MIME**: Sends both `text/plain` and `text/html` versions to satisfy strict corporate email firewalls.

### 🎨 User Experience
* **Modern Corporate UI**: Built with Tailwind CSS for a clean, distraction-free interface.
* **Interactive 3D Elements**: Features engaging CSS-based 3D animations for a premium look and feel.

---

## 🛠 Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core logic and SMTP handling. |
| **Web Framework** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | Lightweight WSGI web application framework. |
| **Frontend** | ![Tailwind](https://img.shields.io/badge/Tailwind-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) | Utility-first CSS framework for rapid UI development. |
| **Environment** | ![Dotenv](https://img.shields.io/badge/.ENV-ECD53F?style=flat-square&logo=dotenv&logoColor=white) | Secure environment variable management. |
| **Deployment** | ![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white) | Serverless edge deployment platform. |

---

## 🚀 Getting Started

Follow these steps to set up the project locally on your machine.

### Prerequisites

* **Python 3.8+** installed.
* **Git** installed.
* A **Gmail** account with *App Password* enabled (for SMTP).

### Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/oziy-id/mail-toolsV2.git](https://github.com/oziy-id/mail-toolsV2.git)
    cd mail-toolsV2
    ```

2.  **Create Virtual Environment (Recommended)**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a `.env` file in the root directory.
2.  Add your credentials (do NOT share this file):

    ```env
    # Flask Security
    SECRET_KEY=your_super_secret_random_string_here

    # SMTP Configuration (Google App Password)
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASS=your_16_digit_app_password
    ```

---

## 💻 Usage

1.  **Run the Application**
    ```bash
    python app.py
    ```
2.  Open your browser and navigate to:
    ```
    [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```
3.  Fill in the target details, upload your CV (PDF only), and hit **Send**.

---

## 🌐 Deployment

This project is optimized for **Vercel** deployment.

1.  Push your code to GitHub.
2.  Import the repository in Vercel.
3.  In Vercel **Settings > Environment Variables**, add:
    * `EMAIL_USER`
    * `EMAIL_PASS`
    * `SECRET_KEY`
4.  Deploy! Vercel will automatically detect `vercel.json` and build the Python environment.

---

## 📂 Project Structure

```bash
mail-toolsV2/
├── static/
│   └── img/            # Static assets (favicons, previews)
├── templates/
│   ├── base.html       # Master layout (Navbar, Footer)
│   ├── index.html      # Main application interface
│   ├── about.html      # Information page
│   ├── email_template.html   # HTML Email Template
│   └── email_template_2.html # Alternate Email Template
├── .gitignore          # Git exclusion rules
├── app.py              # Application entry point
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel build configuration
└── README.md           # Project documentation

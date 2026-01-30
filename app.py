from flask import Flask, render_template, request, flash, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid # Tambahan untuk header profesional
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Pastikan secret key ini kuat
app.secret_key = os.getenv('SECRET_KEY', 'rahasia_ozi_super_secure_v2')

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/send', methods=['POST'])
def send_email():
    if request.method == 'POST':
        server = None # Inisialisasi variabel server
        try:
            # --- 1. AMBIL DATA ---
            template_choice = request.form.get('template_choice', '1')
            applicant_name = request.form['applicant_name']
            applicant_email = request.form['applicant_email']
            whatsapp = request.form['whatsapp']
            main_position = request.form['position_name']
            
            if whatsapp.startswith('0'): whatsapp = '62' + whatsapp[1:]
            
            instagram = request.form.get('instagram', '').strip()
            tiktok = request.form.get('tiktok', '').strip()
            facebook = request.form.get('facebook', '').strip()
            github = request.form.get('github', '').strip()

            # --- 2. VALIDASI PDF ---
            if 'cv_file' not in request.files or request.files['cv_file'].filename == '':
                flash('❌ Wajib upload CV!', 'error')
                return redirect(url_for('home'))
            
            cv_file = request.files['cv_file']
            if not cv_file.filename.lower().endswith('.pdf'):
                flash('⚠️ Format ditolak! Harap upload file PDF.', 'error')
                return redirect(url_for('home'))

            # Baca file ke memori (Cepat)
            cv_data = cv_file.read()
            cv_filename = cv_file.filename

            # --- 3. LIST TARGET ---
            targets = []
            # Target 1
            targets.append({
                'company': request.form['company_name'],
                'email': request.form['hr_email'],
                'position': main_position
            })
            # Target 2 & 3
            for i in range(2, 4):
                comp = request.form.get(f'company_name_{i}', '').strip()
                mail = request.form.get(f'hr_email_{i}', '').strip()
                pos = request.form.get(f'position_name_{i}', '').strip() or main_position
                if comp and mail:
                    targets.append({'company': comp, 'email': mail, 'position': pos})

            # --- 4. KONEKSI SMTP (SATU KALI UNTUK SEMUA) ---
            # Kita lakukan koneksi DI LUAR loop agar hemat waktu (Speed Optimization)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls() # Enkripsi TLS
            server.login(EMAIL_USER, EMAIL_PASS)

            sent_count = 0
            template_file = 'email_template_2.html' if template_choice == '2' else 'email_template.html'

            for target in targets:
                # A. Render Versi HTML
                html_content = render_template(template_file, 
                                             company=target['company'],
                                             position=target['position'],
                                             applicant_name=applicant_name,
                                             whatsapp=whatsapp,
                                             applicant_email=applicant_email,
                                             instagram=instagram,
                                             tiktok=tiktok,
                                             facebook=facebook,
                                             github=github)

                # B. Buat Versi TEXT (Anti-Spam WAJIB)
                # Ini adalah versi polos untuk mesin pembaca email agar tidak dianggap spam
                text_content = f"""
                Yth. HRD {target['company']},
                
                Saya {applicant_name}, bermaksud melamar posisi {target['position']}.
                Saya melampirkan CV dalam format PDF.
                
                Kontak:
                WA: https://wa.me/{whatsapp}
                Email: {applicant_email}
                
                Terima kasih.
                """

                # C. Setup Email Structure (Mixed -> Alternative -> Text/HTML)
                msg = MIMEMultipart("mixed")
                msg['Subject'] = f"Lamaran Kerja: {target['position']} - {applicant_name}"
                msg['From'] = f"{applicant_name} <{EMAIL_USER}>"
                msg['To'] = target['email']
                msg['Cc'] = applicant_email 
                msg['Reply-To'] = applicant_email
                
                # --- HEADERS PRIORITAS (SUPAYA MUNCUL DI ATAS) ---
                msg['Date'] = formatdate(localtime=True)
                msg['Message-ID'] = make_msgid()
                msg['X-Priority'] = '1' # 1 = High Priority
                msg['X-MSMail-Priority'] = 'High'
                msg['Importance'] = 'High'

                # Attach Body (Alternative: Text & HTML)
                msg_body = MIMEMultipart("alternative")
                msg_body.attach(MIMEText(text_content, "plain")) # Versi Teks
                msg_body.attach(MIMEText(html_content, "html"))  # Versi Cantik
                msg.attach(msg_body)

                # Attach PDF
                part_file = MIMEApplication(cv_data, Name=cv_filename)
                part_file['Content-Disposition'] = f'attachment; filename="{cv_filename}"'
                msg.attach(part_file)

                # D. Kirim!
                recipients = [target['email'], applicant_email]
                server.sendmail(EMAIL_USER, recipients, msg.as_string())
                sent_count += 1

            # Tutup koneksi setelah semua selesai
            server.quit()

            flash(f'🚀 SUKSES! Lamaran PRIORITAS TINGGI terkirim ke {sent_count} perusahaan.', 'success')
        
        except Exception as e:
            print(f"Error: {e}")
            flash(f'Gagal kirim. Pastikan koneksi internet stabil. Error: {str(e)}', 'error')
            # Coba tutup server jika error di tengah jalan
            if server:
                try: server.quit()
                except: pass

        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

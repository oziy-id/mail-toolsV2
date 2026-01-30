from flask import Flask, render_template, request, flash, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Ganti dengan key rahasia yang acak
app.secret_key = os.getenv('SECRET_KEY', 'rahasia_ozi_super_secure')

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
        try:
            # --- 1. AMBIL DATA UTAMA ---
            applicant_name = request.form['applicant_name']
            applicant_email = request.form['applicant_email']
            whatsapp = request.form['whatsapp']
            main_position = request.form['position_name'] # Posisi Utama
            
            # Format WA
            if whatsapp.startswith('0'): whatsapp = '62' + whatsapp[1:]
            
            # Sosmed
            instagram = request.form.get('instagram', '').strip()
            tiktok = request.form.get('tiktok', '').strip()
            facebook = request.form.get('facebook', '').strip()
            github = request.form.get('github', '').strip()

            # --- 2. VALIDASI PDF ---
            if 'cv_file' not in request.files:
                flash('❌ File CV wajib ada!', 'error')
                return redirect(url_for('home'))
            
            cv_file = request.files['cv_file']
            
            if cv_file.filename == '':
                flash('❌ Belum memilih file CV!', 'error')
                return redirect(url_for('home'))

            if not cv_file.filename.lower().endswith('.pdf'):
                flash('⚠️ Format ditolak! Harap upload file PDF.', 'error')
                return redirect(url_for('home'))

            # Baca file sekali untuk dikirim berulang
            cv_data = cv_file.read()
            cv_filename = cv_file.filename

            # --- 3. SIAPKAN DAFTAR TUJUAN (LOGIKA BARU) ---
            targets = []
            
            # Target 1 (Utama)
            targets.append({
                'company': request.form['company_name'],
                'email': request.form['hr_email'],
                'position': main_position
            })
            
            # Target Tambahan (2 & 3)
            for i in range(2, 4): # Loop cek input ke-2 dan ke-3
                comp = request.form.get(f'company_name_{i}', '').strip()
                mail = request.form.get(f'hr_email_{i}', '').strip()
                # Ambil posisi khusus, kalau kosong pakai posisi utama
                pos = request.form.get(f'position_name_{i}', '').strip() or main_position
                
                if comp and mail:
                    targets.append({
                        'company': comp, 
                        'email': mail,
                        'position': pos
                    })

            # --- 4. EKSEKUSI PENGIRIMAN ---
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)

            sent_count = 0

            for target in targets:
                # Render Template dengan Data Spesifik Perusahaan Tersebut
                html_content = render_template('email_template.html', 
                                             company=target['company'],
                                             position=target['position'], # Posisi dinamis sesuai input
                                             applicant_name=applicant_name,
                                             whatsapp=whatsapp,
                                             applicant_email=applicant_email,
                                             instagram=instagram,
                                             tiktok=tiktok,
                                             facebook=facebook,
                                             github=github)

                # Setup Email
                msg = MIMEMultipart("mixed")
                msg['Subject'] = f"Lamaran Kerja: {target['position']} - {applicant_name}"
                msg['From'] = f"{applicant_name} via JobSender <{EMAIL_USER}>"
                msg['To'] = target['email']
                msg['Cc'] = applicant_email 
                msg['Reply-To'] = applicant_email 

                msg.attach(MIMEText(html_content, "html"))

                # Attach PDF
                part_file = MIMEApplication(cv_data, Name=cv_filename)
                part_file['Content-Disposition'] = f'attachment; filename="{cv_filename}"'
                msg.attach(part_file)

                # Kirim
                recipients = [target['email'], applicant_email]
                server.sendmail(EMAIL_USER, recipients, msg.as_string())
                sent_count += 1

            server.quit()

            # --- PESAN NOTIFIKASI BARU ---
            flash(f'✅ Berhasil! Email lamaran Anda telah terkirim ke {sent_count} perusahaan dan sedang dalam proses peninjauan oleh HRD. Cek folder Terkirim/Spam untuk memastikan.', 'success')
        
        except Exception as e:
            print(f"Error: {e}")
            flash(f'Gagal kirim: {str(e)}', 'error')

        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
